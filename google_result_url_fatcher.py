from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv

input_user = input("Write your Query :  ")


# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('start-maximized')  # Start maximized
# Commenting out headless mode for debugging
# options.add_argument('--headless')  # Run in headless mode

driver = webdriver.Chrome(options=options)

try:
    # Open Google
    print("Opening Google...")
    driver.get('https://www.google.com')

    # Wait for the search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    print("Entering search query...")
    search_query = input_user
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Function to get URLs from the current page
    def get_urls():
        print("Getting URLs from the current page...")
        urls = []
        try:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'cite.qLRx3b.tjvcx.GvPZzd.cHaqb'))
            )
            for result in results:
                full_url = result.get_attribute('textContent')
                # Extract only the main part of the URL
                main_url = re.search(r'https?://[^ ]+', full_url).group(0)
                urls.append(main_url)
        except Exception as e:
            print(f"Error getting URLs: {e}")
        return urls

    # Get URLs from all pages
    all_urls = []

    while True:
        time.sleep(2)  # Wait for the page to load
        current_urls = get_urls()
        all_urls.extend(current_urls)
        print(f"Collected {len(current_urls)} URLs from this page.")

        try:
            # Check if there is a next page button
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'pnnext'))
            )
            print("Clicking next button...")
            next_button.click()
        except Exception as e:
            # If no next button, break the loop
            print(f"No more next button or error: {e}. Exiting loop.")
            break

finally:
    # Close the driver
    print("Closing the driver...")
    driver.quit()

# Print all collected URLs
print("Collected URLs:")
with open('serp_sites.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for url in all_urls:
        writer.writerow([url])