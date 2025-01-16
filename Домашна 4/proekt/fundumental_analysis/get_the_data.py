import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import PyPDF2
from PIL import Image
import pytesseract
import mammoth
import subprocess
import shutil
from pdf2image import convert_from_path
import time


# Utility Functions

def setup_driver(download_dir):
    """Sets up the Selenium WebDriver with a custom download directory."""
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=chrome_options)


def save_text_to_file(folder_path, file_name, content):
    """Saves the given content to a .txt file in the specified folder."""
    file_path = os.path.join(folder_path, f"{file_name}.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Saved text to: {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")


def extract_pdf_text(pdf_path):
    """Extracts text from a single-page PDF if it contains selectable text."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) > 1:
                print(f"Skipping {pdf_path}: More than one page.")
                return None
            text = ''.join(page.extract_text() for page in reader.pages)
            if text.strip():
                print(f"Extracted text from {pdf_path}")
                return text.strip()
            print(f"Skipping {pdf_path}: No text found.")
            return None
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


def extract_image_text(image_path):
    """Extracts text from an image using OCR."""
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang="eng").strip()
    except Exception as e:
        print(f"Error extracting text from {image_path}: {e}")
        return None


def extract_docx_text(docx_path):
    """Extracts text from a .docx file using Mammoth."""
    try:
        with open(docx_path, "rb") as file:
            return mammoth.extract_raw_text(file).value.strip()
    except Exception as e:
        print(f"Error extracting text from {docx_path}: {e}")
        return None


def extract_doc_text(doc_path):
    """Converts .doc to .docx and extracts text."""
    try:
        converted_path = doc_path.replace(".doc", ".docx")
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "docx", doc_path, "--outdir", os.path.dirname(doc_path)],
            check=True,
        )
        return extract_docx_text(converted_path)
    except Exception as e:
        print(f"Error converting {doc_path} to .docx: {e}")
        return None


def process_files_in_folder(folder_path):
    """Processes all files in a folder and extracts text based on file type."""
    combined_text = set()

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".pdf"):
            text = extract_pdf_text(file_path)
        elif file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            text = extract_image_text(file_path)
        elif file_name.endswith(".docx"):
            text = extract_docx_text(file_path)
        elif file_name.endswith(".doc"):
            text = extract_doc_text(file_path)
        else:
            print(f"Skipping unsupported file: {file_name}")
            continue
        if text:
            combined_text.add(text)

    if combined_text:
        save_text_to_file(folder_path, "combined_text", "\n\n".join(sorted(combined_text)))


# Selenium Workflow

def get_codes_from_dropdown():
    """Extracts issuer codes and names from a dropdown menu on the target website."""
    driver = webdriver.Chrome()
    url = "https://seinet.com.mk/search"
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "formIssuerId")))
    raw_html = driver.page_source
    soup = BeautifulSoup(raw_html, "html.parser")
    select_element = soup.select_one("#formIssuerId")
    driver.quit()

    if select_element:
        return {
            int(option["data-key"]): option.text.strip()
            for option in select_element.find_all("option")
            if "data-key" in option.attrs and option["data-key"] != "0"
        }
    print("No dropdown found.")
    return {}


def process_issuer_files(driver, base_url, issuer_id, issuer_name, root_download_dir):
    """Processes files for a specific issuer by downloading and extracting text."""
    issuer_folder = os.path.join(root_download_dir, issuer_name)
    os.makedirs(issuer_folder, exist_ok=True)
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": issuer_folder})

    driver.get(f"{base_url}{issuer_id}")
    print(f"Visiting {base_url}{issuer_id}")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-hover tbody tr")))
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-hover tbody tr")

        for index, row in enumerate(rows[:3]):
            print(f"Processing row {index + 1} for {issuer_name}")
            row.click()
            time.sleep(3)

            try:
                download_links = driver.find_elements(By.CSS_SELECTOR, "div[title]")
                for link in download_links:
                    file_title = link.get_attribute("title").lower()
                    if file_title.endswith((".pdf", ".docx", ".doc")):
                        link.click()
                        time.sleep(5)
            except Exception as e:
                print(f"Error downloading files for {issuer_name}: {e}")

            driver.back()
            time.sleep(3)

        process_files_in_folder(issuer_folder)

    except Exception as e:
        print(f"Error processing {issuer_name}: {e}")


def main():
    root_download_dir = os.path.abspath("pdf_downloads")
    os.makedirs(root_download_dir, exist_ok=True)

    base_url = "https://seinet.com.mk/search/"
    codes = get_codes_from_dropdown()

    driver = setup_driver(root_download_dir)
    for issuer_id, issuer_name in codes.items():
        print(f"Processing issuer: {issuer_name} ({issuer_id})")
        process_issuer_files(driver, base_url, issuer_id, issuer_name, root_download_dir)
    driver.quit()


if __name__ == "__main__":
    main()
