import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import PyPDF2
from PIL import Image
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mammoth  # For handling .docx files
import subprocess
import os
import shutil
from pdf2image import convert_from_path

def get_codes_from_dropdown():
    driver = webdriver.Chrome()
    url = "https://seinet.com.mk/search"
    dictionary = {}
    driver.get(url)
    time.sleep(5)
    raw_html = driver.page_source
    soup = BeautifulSoup(raw_html, "html.parser")
    select_element = soup.select("#formIssuerId")
    if select_element:
        options = select_element[0].find_all("option")
        dictionary = {
            int(option['data-key']): option.text.strip()
            for option in options
            if 'data-key' in option.attrs and option['data-key'] != "0"
        }
    else:
        print("No <select> element found.")
    driver.quit()
    return dictionary

def setup_driver(download_dir):
    """Sets up the Selenium WebDriver with a custom download directory."""
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,  # Open PDFs externally instead of browser viewer
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def extract_pdf_text(pdf_path):
    """Extracts text from a PDF file if it meets conditions: single-page, non-scanned, pure PDF."""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            # Condition 1: Skip if the PDF has more than one page
            if len(reader.pages) > 1:
                print(f"Skipping PDF {pdf_path}: More than one page.")
                return None

            # Try extracting text
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()

            # Condition 2: Skip if no text is extracted (likely a scanned document)
            if not pdf_text.strip():
                print(f"Skipping PDF {pdf_path}: Likely a scanned document (no text extracted).")
                return None

            # If text is extracted, return it
            print(f"Extracted text from PDF: {pdf_path}")
            return pdf_text.strip()

    except Exception as e:
        print(f"Error extracting text with PyPDF2 from {pdf_path}: {e}")
        return None  # Return None if an error occurs

def extract_image_text(image_path):
    """Extracts text from an image file using OCR."""
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang="eng")
        return text.strip()
    except Exception as e:
        return f"Error extracting image text: {e}"

def save_extracted_text(folder_path, file_name, extracted_text):
    """Saves extracted text to a .txt file in the specified folder."""
    txt_file_path = os.path.join(folder_path, f"{file_name}.txt")
    try:
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"Saved extracted text to: {txt_file_path}")
    except Exception as e:
        print(f"Error saving text to file {txt_file_path}: {e}")

def delete_unwanted_files(folder_path):
    """Deletes all .xlsx and .docx files from the specified folder."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xlsx") or file_name.endswith(".xls") or file_name.endswith(".docx"):
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted unwanted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def extract_docx_text(docx_path):
    """Extracts text from a .docx file using the mammoth library."""
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.extract_raw_text(docx_file)
            text = result.value.strip()
            if text:
                return text
            else:
                return "No text extracted from .docx file."
    except Exception as e:
        print(f"Error extracting text from .docx file {docx_path}: {e}")
        return f"Error extracting text from .docx: {e}"

def extract_doc_text(doc_path):
    """Extracts text from a .doc file using LibreOffice command-line conversion."""
    try:
        # Convert .doc to .docx using LibreOffice
        converted_path = doc_path.replace(".doc", ".docx")
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "docx", doc_path, "--outdir", os.path.dirname(doc_path)],
            check=True,
        )
        # Extract text from the converted .docx file
        return extract_docx_text(converted_path)
    except Exception as e:
        print(f"Error converting or extracting text from .doc file {doc_path}: {e}")
        return f"Error extracting text from .doc: {e}"


def process_downloaded_files(folder_path):
    """
    Processes all files in the issuer's folder (PDFs, images, .docx, and .doc) and combines text.
    Checks for duplication in the combined text file.
    """
    combined_text = set()  # Use a set to store unique extracted text sections

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        extracted_text = ""

        # Extract text based on file type
        if file_name.endswith(".pdf"):
            print(f"Processing PDF: {file_path}")
            extracted_text = extract_pdf_text(file_path)
        elif file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"Extracting text from Image: {file_path}")
            extracted_text = extract_image_text(file_path)
        elif file_name.lower().endswith(".docx"):
            print(f"Extracting text from .docx: {file_path}")
            extracted_text = extract_docx_text(file_path)
        elif file_name.lower().endswith(".doc"):
            print(f"Extracting text from .doc: {file_path}")
            extracted_text = extract_doc_text(file_path)
        else:
            print(f"Skipping unsupported file type: {file_name}")
            continue

        # Add unique extracted text to the set
        if extracted_text and extracted_text.strip():
            combined_text.add(extracted_text.strip())

    # Save the combined text to a single .txt file
    if combined_text:
        combined_text_str = "\n\n".join(sorted(combined_text))  # Combine and sort for consistency
        save_extracted_text(folder_path, "combined_text", combined_text_str)


def save_extracted_text(folder_path, file_name, extracted_text):
    """
    Saves extracted text to a .txt file in the specified folder.
    """
    txt_file_path = os.path.join(folder_path, f"{file_name}.txt")
    try:
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        print(f"Saved extracted text to: {txt_file_path}")
    except Exception as e:
        print(f"Error saving text to file {txt_file_path}: {e}")


def process_issuer_files(driver, base_url, issuer_id, issuer_name, root_download_dir):
    """Processes and downloads files for a specific issuer."""
    # Create a folder for this issuer
    issuer_folder = os.path.join(root_download_dir, issuer_name)
    os.makedirs(issuer_folder, exist_ok=True)

    # Set download directory dynamically
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": issuer_folder}
    )

    # Visit the issuer's URL
    url = f"{base_url}{issuer_id}"
    driver.get(url)
    print(f"Visiting URL: {url}")

    try:
        # Wait for the table or log an appropriate message if it doesn't exist
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-hover tbody tr"))
        )
        print(f"Table found for Issuer: {issuer_name}")

        all_text_content = ""

        for index in range(3):  # Attempt to process up to 3 rows
            # Fetch rows again after each navigation
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table-hover tbody tr")
            if index >= len(rows):
                print(f"No more rows to process for Issuer: {issuer_name}")
                break

            # Select the row based on the index
            row = rows[index]
            print(f"Processing row {index + 1} for Issuer: {issuer_name}")
            row.click()  # Click on the row to open details
            time.sleep(5)  # Allow time for the page to load

            # Initialize a flag to check if attachments are found
            attachments_found = False

            # Locate and process attachments or visible text
            try:
                # Check for attachments
                download_links = driver.find_elements(By.CSS_SELECTOR, "div[title]")
                if download_links:
                    attachments_found = True
                    for link in download_links:
                        file_title = link.get_attribute("title").lower()
                        print(f"Found file: {file_title}")

                        # Check if it's a downloadable file
                        if file_title.endswith((".pdf", ".docx", ".doc")):
                            print(f"Clicking to download: {file_title}")
                            link.click()  # Directly click on the link
                            time.sleep(5)  # Wait for the file to download

                            # Process the downloaded files
                            process_downloaded_files(issuer_folder)

                            # Extract text content from the folder and append it
                            for file_name in os.listdir(issuer_folder):
                                file_path = os.path.join(issuer_folder, file_name)
                                if file_name.endswith(".txt"):  # Ensure only text files are read
                                    with open(file_path, "r", encoding="utf-8") as f:
                                        all_text_content += f.read() + "\n\n"

                # If no attachments are found, extract visible text from the page
                if not attachments_found:
                    print(f"No attachments found for Issuer: {issuer_name}. Extracting visible text.")
                    try:
                        # Locate the visible text container
                        visible_text_element = driver.find_element(By.CSS_SELECTOR, "div.text-left.ml-auto")
                        visible_text = visible_text_element.text
                        if visible_text.strip():
                            print(f"Extracted visible text for Issuer: {issuer_name}")
                            all_text_content += visible_text + "\n\n"  # Append to the combined text
                    except Exception as text_error:
                        print(f"Error extracting visible text for Issuer {issuer_name}: {text_error}")
            except Exception as e:
                print(f"Error locating or downloading files for Issuer {issuer_name}: {e}")

            # Navigate back to the main table
            driver.back()
            time.sleep(5)  # Allow time for the page to reload

        # Save the combined text into a single file
        if all_text_content.strip():
            save_extracted_text(issuer_folder, f"{issuer_name}_combined", all_text_content)

    except Exception as e:
        print(f"Error processing files for Issuer {issuer_name}: {e}")


def change_urls_in_browser():
    root_download_dir = os.path.abspath("pdf_downloads")  # Root folder for all downloads
    os.makedirs(root_download_dir, exist_ok=True)  # Ensure the directory exists

    base_url = "https://seinet.com.mk/search/"
    codes_dict = get_codes_from_dropdown()  # Get the issuer codes and names

    driver = setup_driver(root_download_dir)  # Initialize WebDriver

    for issuer_id, issuer_name in codes_dict.items():
        print(f"Processing Issuer: {issuer_name} (ID: {issuer_id})")
        process_issuer_files(driver, base_url, issuer_id, issuer_name, root_download_dir)

    driver.quit()

def clean_up_test_folders(root_folder, issuer_keys):
    """
    Cleans up the folders for specific issuers under the root folder:
    1. Deletes empty folders.
    2. Deletes folders containing only files (e.g., PDFs) without a combined_text.txt file.
    3. In folders with combined_text.txt, keeps only the file named after the folder with "_combined.txt".

    :param root_folder: Root folder containing issuer folders.
    :param issuer_keys: List of issuer keys to test (e.g., ['10', '122']).
    """
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)

        # Only process folders for the specified issuers
        if folder_name not in issuer_keys:
            print(f"Skipping folder: {folder_name}")
            continue

        if not os.path.isdir(folder_path):
            continue  # Skip if not a directory

        # Check folder contents
        files = os.listdir(folder_path)
        if not files:
            # Delete empty folders
            print(f"Deleting empty folder: {folder_path}")
            os.rmdir(folder_path)
            continue

        # Check if folder contains only files, but combined_text.txt is not one of them
        if "combined_text.txt" not in files and all(os.path.isfile(os.path.join(folder_path, f)) for f in files):
            print(f"Deleting folder without combined_text.txt and containing only files: {folder_path}")
            shutil.rmtree(folder_path)
            continue

        # Check if folder contains a combined_text.txt file
        if "combined_text.txt" in files:
            print(f"Cleaning folder and keeping only the folder-specific combined file in: {folder_path}")
            folder_specific_combined_file = f"{folder_name}_combined.txt"
            for file in files:
                file_path = os.path.join(folder_path, file)
                # Keep only the specific combined file
                if file != folder_specific_combined_file:
                    print(f"Deleting file: {file_path}")
                    os.remove(file_path)

if __name__ == '__main__':
        # # Step 1: Define the root download directory
        # root_download_dir = os.path.abspath("pdf_downloads")
        #
        # # Step 2: Perform the file downloads and processing
        # print("Starting the download and processing of issuer files...")
        # change_urls_in_browser()
        #
        # # Step 3: Define the list of issuer keys or folder names to clean up
        # # Replace this with the actual folder names you want to clean
        # test_keys = [folder_name for folder_name in
        #              os.listdir(root_download_dir)]  # Clean all folders in `pdf_downloads`
        #
        # # Step 4: Clean up the folders
        # print("Cleaning up the folders...")
        # clean_up_test_folders(root_download_dir, test_keys)
        #
        # print("Folder cleanup completed!")
        codes = get_codes_from_dropdown()
        print(codes)



