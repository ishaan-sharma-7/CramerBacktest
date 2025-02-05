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
csv_filename = 'jim_cramer_tweets.csv'

# Initialize the WebDriver
driver = webdriver.Chrome()  
driver.get("https://x.com/login")
time.sleep(2)  # Wait for the page to load completely

# Look for Email and enter
username_input = driver.find_element(By.NAME, "text")
username_input.send_keys(EMAIL)
username_input.send_keys(Keys.RETURN)
time.sleep(2) 

# Look for username if asking to enter
username_input = driver.find_element(By.NAME, "text")
username_input.send_keys(USERNAME)
username_input.send_keys(Keys.RETURN)
time.sleep(2) 

# Look for password field
try:
    password_input = driver.find_element(By.NAME, "password")  # Find password input
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
except Exception:
    print("Password field not found. The login process may require an extra step.")

time.sleep(2) 

# Step 3: Navigate to the Jim Cramer profile
driver.get(f"https://x.com/jimcramer/with_replies")
time.sleep(2)  

csv_filename = "jim_cramer_tweets.csv"
keys = ["timestamp", "text"]
with open(f'{csv_filename}', "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()

# Start time counter to stop after 20 seconds
max_scrolls = 2  # Set a higher max scroll limit to increase the tweet count
scroll_count = 0
last_height = driver.execute_script("return document.body.scrollHeight")

while scroll_count < max_scrolls:

    tweets = driver.find_elements(By.CSS_SELECTOR, "article")
    
    for tweet in tweets:
        try:
            text = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
            timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            
            # Write tweet to CSV file
            with open(f'{csv_filename}', "a", newline="", encoding="utf-8") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writerow({"timestamp": timestamp, "text": text})
        
        except Exception:
            continue

    # Scroll down by executing JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new tweets to load, increase wait time for more tweets
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        scroll_count += 1  # Increment scroll count if no new tweets are loaded
    else:
        last_height = new_height
        scroll_count = 0  # Reset scroll count if new tweets are loaded

driver.quit()

print(f"Tweets saved to {csv_filename}")