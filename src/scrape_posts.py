from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime

# Replace with your X.com login credentials
EMAIL = ""
USERNAME = ""
PASSWORD = ""

# Initialize the WebDriver
driver = webdriver.Chrome()  
driver.get("https://x.com/login")
time.sleep(2)  # Wait for the page to load completely

# Step 1: Look for Email and enter
username_input = driver.find_element(By.NAME, "text")
username_input.send_keys(EMAIL)
username_input.send_keys(Keys.RETURN)
time.sleep(2) 

# Look for username if asking to enter
username_input = driver.find_element(By.NAME, "text")
username_input.send_keys(USERNAME)
username_input.send_keys(Keys.RETURN)
time.sleep(2) 

# Step 2: Wait and check for password field
try:
    password_input = driver.find_element(By.NAME, "password")  # Find password input
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
except Exception:
    print("Password field not found. The login process may require an extra step.")

time.sleep(2) 

# Step 3: Navigate to the target user's profile
driver.get(f"https://x.com/jimcramer")
time.sleep(2)  # Wait for the profile page to load

# Scroll and load tweets
tweet_data = []
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    tweets = driver.find_elements(By.CSS_SELECTOR, "article")
    
    for tweet in tweets:
        try:
            text = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
            timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            tweet_data.append({"text": text, "timestamp": timestamp})
        except Exception:
            continue

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new tweets to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break
    last_height = new_height

# Save tweets to CSV file
csv_filename = "tweets.csv"
keys = ["timestamp", "text"]

with open(f'{csv_filename}', "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(tweet_data)

driver.quit()

print(f"Tweets saved to {csv_filename}")
