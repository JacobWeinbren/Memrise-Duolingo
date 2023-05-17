from selenium import webdriver as driver
from selenium.webdriver.common.by import By
import credentials
import time
import csv

# Log in to the Memrise website
def login(browser):
    browser.get("https://app.memrise.com/signin")

    # Enter username and password
    browser.find_element(By.ID, "username").send_keys(credentials.username)
    browser.find_element(By.ID, "password").send_keys(credentials.password)

    # Submit the login form
    browser.find_element(By.XPATH, '//form[@method="post"]').submit()
    time.sleep(3)

    # Return True if logged in, otherwise return False
    return browser.current_url == "https://app.memrise.com/dashboard"

# Extract data from the Memrise course
def extract_data(browser, links):
    data = []
    for link in links:
        browser.get(link)

        # Get the title of the current level
        title = browser.find_element(By.CSS_SELECTOR, ".progress-box-title").text

        # Get the words and meanings for the current level
        words = [word.text for word in browser.find_elements(By.CSS_SELECTOR, ".col_a.col.text")]
        meanings = [word.text for word in browser.find_elements(By.CSS_SELECTOR, ".col_b.col.text")]

        # Combine the title, word, and meaning into a single data entry
        for index, word in enumerate(words):
            data.append({
                "title": title,
                "word": word,
                "meaning": meanings[index]
            })
    return data

# Save the extracted data to a CSV file
def save_data_to_csv(data, file_name='data.csv'):
    keys = data[0].keys()

    with open(file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    browser = driver.Chrome()

    # Log in to Memrise and print the result
    if login(browser):
        print("Logged in")
    else:
        print("Login failed")
        browser.quit()
        return

    # Navigate to the Hebrew Duolingo course and extract level links
    #browser.get("https://app.memrise.com/course/1031737/hebrew-duolingo/")
    browser.get("https://app.memrise.com/course/1508230/duolingo-hebrew-the-missing-words/")
    levels = browser.find_elements(By.CSS_SELECTOR, ".level")
    links = [level.get_attribute("href") for level in levels]

    # Extract data from each level
    data = extract_data(browser, links)

    # Save the extracted data to a CSV file
    #save_data_to_csv(data, file_name="main.csv")
    save_data_to_csv(data, file_name="secondary.csv")

    # Close the browser
    browser.quit()

if __name__ == "__main__":
    main()