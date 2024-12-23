from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import os
import json
import datetime

class WebScraper:
    def __init__(self, driver_path='../chromedriver.exe'):
        """Initialize the browser with Selenium."""
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def open_website(self, url):
        """Open the URL in the browser."""
        self.driver.get(url)

    def extract_all_text(self):
        """Extract all visible text from the webpage."""
        elements = self.driver.find_elements(By.XPATH, "//*[not(self::script) and not(self::style)]")
        text_content = [element.text.strip() for element in elements if element.text.strip()]
        return "\n".join(text_content)

    def find_and_download_files(self, download_dir='downloads'):
        """Find and download files linked on the webpage."""
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        links = self.driver.find_elements(By.TAG_NAME, "a")
        file_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        downloaded_files = []
        for link in file_links:
            if any(link.endswith(ext) for ext in ['.pdf', '.docx', '.doc', '.xlsx']):
                try:
                    response = requests.get(link, stream=True)
                    if response.status_code == 200:
                        file_name = os.path.join(download_dir, os.path.basename(link))
                        with open(file_name, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=1024):
                                file.write(chunk)
                        downloaded_files.append(file_name)
                        print(f"Downloaded: {file_name}")
                except Exception as e:
                    print(f"Failed to download {link}: {e}")

        return downloaded_files

    def save_data_to_json(self, data):
        """Save scraped data to a JSON file."""
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(data_dir, f"scraped_data_{timestamp}.json")

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Data saved to {file_path}")

    def close_browser(self):
        """Close the browser."""
        self.driver.quit()
