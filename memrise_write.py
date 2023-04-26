from selenium import webdriver as driver
from selenium.webdriver.common.by import By
import credentials
import time
import os

# Function to check if an element exists in the browser
def check_exists(browser, searchable_type, path):
    try:
        browser.find_element(searchable_type, path)
    except:
        return False
    return True

# Function to log in to the Memrise website
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

# Function to add words and audio files to the Memrise course
def addWords(browser):
    exists = check_exists(browser, By.CSS_SELECTOR, ".pool-name")

    if exists:
        title = browser.find_element(By.CSS_SELECTOR, ".pool-name").text

        # Locate the directory containing the title
        for root, dirs, files in os.walk('storage'):
            for name in dirs:
                if title == name.split('-')[1]:
                    loc = os.path.join(root, name)
        
        # Read the CSV file with words
        with open(os.path.join(loc, title + '.csv')) as f:
            lines = f.read().replace("Word,Meaning\n", "")

        # Add words from CSV file to Memrise
        browser.find_element(By.XPATH, '//button[@data-role="pool-bulk-add"]').click()
        time.sleep(3)
        browser.execute_script("""$("input[value='comma']").prop("checked", true);""")
        browser.execute_script('$("textarea").get(0).value += `' + lines + '`;')
        browser.execute_script('$("textarea").get(0).value += `\n`;')
        browser.find_element(By.XPATH, '//a[@tabindex=4]').click()
        time.sleep(3)

        # Add "Sound" column to Memrise
        browser.find_element(By.XPATH, '//button[@data-role="pool-column-add"]').click()
        time.sleep(3)
        browser.execute_script("""$("input[name='name']").val("Sound")""")
        browser.execute_script("""$("input[value='audio']").prop("checked", true);""")
        browser.find_element(By.XPATH, '//a[@tabindex=4]').click()
        time.sleep(3)

        # Get list of MP3 files in the directory
        files = []
        total = 0
        for file in os.listdir(loc):
            if file.endswith('.mp3'):
                total += 1

        for i in range(0, total):
            for file in os.listdir(loc):
                if file.endswith('.mp3') and str(i) == file.split("-")[0]:
                    files.append('/' + os.path.join(loc, file))

        # Upload MP3 files to Memrise
        current_file_count = 0
        while current_file_count <= len(files):
            file_uploaders = browser.find_elements(By.CSS_SELECTOR, '.add_thing_file')

            for file_uploader in file_uploaders:
                if current_file_count <= len(files):
                    print(current_file_count, 'uploading')
                    file_uploader.send_keys(os.getcwd() + files[current_file_count])
                    current_file_count += 1
                else:
                    break

            next_page_element = check_exists(browser, By.XPATH, u'//a[contains(text(), "Next")]')
            if next_page_element:
                browser.get(browser.find_element(By.XPATH, u'//a[contains(text(), "Next")]').get_attribute('href'))
                time.sleep(3)
            else:
                break

        time.sleep(3)

# Main function
def main():
    browser = driver.Chrome()

    # Log in to Memrise and print the result
    if login(browser):
        print("Logged in")
    else:
        print("Login failed")
        browser.quit()
        return
    
    # Navigate to the Memrise course and add words
    for i in range(0, 100):
        browser.get('https://app.memrise.com/course/6403867/duolingo-hebrew-revised/edit/database/' + str(7456220 + i))
        time.sleep(3)
        addWords(browser)

# Entry point
if __name__ == "__main__":
    main()