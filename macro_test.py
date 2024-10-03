from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

from pilot_processing import chat_history


# Initialize the WebDriver (adjust the path to your WebDriver)
driver = webdriver.Chrome()

# Navigate to your chat application's URL
driver.get('http://localhost:3000')

# Perform any necessary login steps
# Example:
username_input = driver.find_element(By.CLASS_NAME, 'login-input')
# password_input = driver.find_element(By.ID, 'password')
login_button = driver.find_element(By.CLASS_NAME, 'login-button')
username_input.send_keys('jake')
# password_input.send_keys('your_password')
login_button.click()

# Wait for the chat interface to load
time.sleep(2)  # Adjust as needed


# Store the start time
start_time = datetime.now()

for message in chat_history:
    # Calculate the delay based on message timestamps
    message_delay = (message.sent_time - message.first_message_time).total_seconds()
    elapsed_time = (datetime.now() - start_time).total_seconds()
    sleep_time = message_delay - elapsed_time
    if sleep_time > 0:
        time.sleep(sleep_time)

    # Find the chat input element (adjust the selector as needed)
    chat_input = driver.find_element(By.CLASS_NAME, 'cs-message-input__content-editor')  # Replace with your input's ID or other selector

    # Send the message
    chat_input.send_keys(message.message)
    chat_input.send_keys(Keys.RETURN)  # Press Enter to send

    # Optionally, wait for the message to appear in the chat window
    # time.sleep(1)  # Adjust as needed

# Close the WebDriver after sending all messages
driver.quit()
