import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def extract_pdf_text(pdf_path):
    """Extracts text from PDF files."""
    try:
        pages = convert_from_path(pdf_path)
        text = ""
        for page in pages:
            temp_image = "temp_image.png"
            page.save(temp_image, "PNG")
            text += pytesseract.image_to_string(Image.open(temp_image), lang="eng")
            os.remove(temp_image)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


def extract_html_text(raw_html):
    """Extracts text from HTML using BeautifulSoup."""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(strip=True)


def get_issuer_codes():
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
            option.get("data-key"): option.text.strip()
            for option in select_element.find_all("option")
            if option.get("data-key") and option.get("data-key") != "0"
        }
    return {}