import json
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ScrapeTrips import scrape_past_trips, scrape_active_trips

# Load environment variables from .env file
load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

if not email or not password:
    print("Email or password is missing in the .env file!")
    exit(1)


def init_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)  # Set an implicit wait time for elements to load
    return driver


def login(driver, email, password):
    try:
        # Open the TripCase login page
        driver.get("https://www.tripcase.com/login")
        time.sleep(2)  # Wait for the page to load

        # Find the email and password fields and fill them in
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(email)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        # Find and click the sign-in button
        sign_in_button = driver.find_element(By.ID, "sign-in-submit")
        sign_in_button.click()

        # Wait for the login process to complete
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "active-trip-list-wrapper"))
        )
        print("Login successful!")
    except Exception as e:
        print(f"Error during login: {e}")
        driver.quit()
        exit(1)


def close_driver(driver):
    driver.quit()





# Main function to control the script's flow
def main():
    driver = init_driver()
    login(driver, email, password)

    scrape_past_trips(driver, 10)
    print("done Scraping the past")
    scrape_active_trips(driver)
    close_driver(driver)


if __name__ == "__main__":
    main()
