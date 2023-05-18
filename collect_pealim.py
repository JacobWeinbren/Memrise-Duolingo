# Importing the required libraries
import requests
import json
from bs4 import BeautifulSoup


def scrape_and_save_to_file():
    """Function to scrape the website and save data to a json file."""

    # Empty dictionary to store the data
    data_dict = {}

    # Iterate over each page of the website
    for page_num in range(1, 606):

        print(page_num)

        # Construct the URL for the current page
        page_url = f"https://www.pealim.com/dict/?page={page_num}"

        # Make a GET request to fetch the raw HTML content
        page_response = requests.get(page_url)

        # Parse the page content
        soup = BeautifulSoup(page_response.text, 'html.parser')

        # Find all 'menukad' and 'dict-transcription' elements on the page
        menukad_elements = soup.find_all('span', class_='menukad')
        transcription_elements = soup.find_all(
            'span', class_='dict-transcription')

        # Iterate over each 'menukad' and 'dict-transcription' pair
        for menukad, transcription in zip(menukad_elements, transcription_elements):

            # Extract text from the elements and strip any leading/trailing whitespaces
            menukad_text = menukad.get_text(strip=True)
            transcription_text = transcription.get_text(strip=True)

            # Store the extracted text into the dictionary
            data_dict[menukad_text] = transcription_text

    # Save the collected data into a json file
    with open('data.json', 'w', encoding='utf-8') as file_obj:
        json.dump(data_dict, file_obj, ensure_ascii=False, indent=4)


# Call the function
scrape_and_save_to_file()
