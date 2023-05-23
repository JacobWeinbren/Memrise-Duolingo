import requests
from bs4 import BeautifulSoup
import json

# Function to get the transcriptions for a word
def get_transcriptions(word):
    # Request the search page for the given word
    r = requests.get(f'https://www.pealim.com/search/?q={word}')
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all search results
    results = soup.find_all('div', class_='verb-search-result')

    words_transcriptions = {}

    try:
        for verb in results:
            # Extract needed data from the search result
            link = verb.find('div', class_='verb-search-lemma').find('a')['href']
            word = verb.find('span', class_='menukad').text
            form_transcription = verb.find('div', class_='vf-search-hebrew').find('span', class_='transcription').text

            # Clean up and add word and transcription to the dictionary
            cleaned_word = word.replace('־', '').replace('(', '').replace(')', '').replace('\u200f', '').replace('!','')
            cleaned_transcription = form_transcription.replace('-', '').replace('(', '').replace(')', '').replace('!','')
            words_transcriptions[cleaned_word] = cleaned_transcription

            # Request the conjugation page
            r = requests.get(f'https://www.pealim.com{link}')
            soup = BeautifulSoup(r.text, 'html.parser')

            if soup != None and soup.find('table') != None:
                # Extract data from the conjugation page
                table_rows = soup.find('table').find('tbody').find_all('tr')
                for row in table_rows:
                    columns = row.find_all('td')
                    for column in columns:
                        word = column.find('span', class_='menukad').text
                        transcription = column.find('div', class_='transcription').text

                        # Clean up and add conjugation and transcription to the dictionary
                        cleaned_word = word.replace('־', '').replace('(', '').replace(')', '').replace('\u200f', '').replace('!','')
                        cleaned_transcription = transcription.replace('-', '').replace('(', '').replace(')', '').replace('!','')
                        words_transcriptions[cleaned_word] = cleaned_transcription

        return words_transcriptions
    except:
        return words_transcriptions

# Load initial data from data.json
with open('data.json', 'r') as f:
    data = json.load(f)

# Get the list of keys (words) from the data
keys = list(data.keys())

count = 0
# Continuously update the dictionary and the JSON file with new transcriptions
while keys:
    count += 1
    key = keys.pop(0)  # Get the first word from the list
    new_data = get_transcriptions(key)  # Get new transcriptions
    data.update(new_data)  # Update the dictionary with new transcriptions

    print(key, count)

    # Write updated data to the JSON file
    with open('pealim-transliterations.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.flush()