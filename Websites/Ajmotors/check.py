from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Function to scrape vehicle data using Selenium
def scrape_vehicle_data(url):
    try:
        driver.get(url)  # Load the page

        # Wait for content to load (adjust the time or use WebDriverWait)
        time.sleep(3)

        # Extract data using XPaths (Modify XPaths according to the website structure)
        title = driver.find_element(By.XPATH, '//h1[@class="vehicle-title"]/text()').text
        price = driver.find_element(By.XPATH, '//span[@class="vehicle-price"]/text()').text
        description = driver.find_element(By.XPATH, '//div[@class="vehicle-description"]/p').text

        # Clean the extracted data
        title = title.strip() if title else 'N/A'
        price = price.strip() if price else 'N/A'
        description = description.strip() if description else 'N/A'

        # Print or store the scraped data
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Description: {description}")
        print('-' * 50)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Loop through each URL and scrape the data
urls = ['https://www.ajmotors.co.nz/vehicles']
for url in urls:
    print(f"Scraping {url}...")
    scrape_vehicle_data(url)

# Close the driver after scraping
driver.quit()
