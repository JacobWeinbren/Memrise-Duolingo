# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
import unicodedata

# Function to get SBERT embeddings for given sentences
def get_sbert_embeddings(model, tokenizer, sentences):
    inputs = tokenizer(sentences, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.pooler_output
    return embeddings

# Function to compute semantic similarity between two sentences
def semantic_similarity(sentence1, sentence2, model, tokenizer):
    embeddings = get_sbert_embeddings(model, tokenizer, [sentence1, sentence2])
    similarity_score = 1 - cosine(embeddings[0], embeddings[1])
    return similarity_score

# Function to remove Hebrew vowels
def strip_vowels(hebrew_text):
    return ''.join(c for c in unicodedata.normalize('NFD', hebrew_text) if unicodedata.category(c) != 'Mn')

# Load SBERT model and tokenizer
model_name = "sentence-transformers/paraphrase-distilroberta-base-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def searchWord(hebrew, initial_translation):
    try:
        # Request to get verb search results for the given Hebrew word
        response = requests.get(f'https://www.pealim.com/search/?q={hebrew}')
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='verb-search-result')

        # Store the translation and link of each search result
        translations = {result.find('div', class_='vf-search-tpgn-and-meaning').get_text().split(":")[1]: result.find('div', class_='verb-search-lemma').find('a').get('href') for result in search_results}

        # Find the translation with the highest semantic similarity to the initial translation
        most_similar_word = max(translations, key=lambda translation: semantic_similarity(initial_translation, translation, model, tokenizer))

        # Request to get the conjugation table of the most similar word
        response = requests.get(f'https://www.pealim.com{translations[most_similar_word]}')
        soup = BeautifulSoup(response.text, 'html.parser')
        table_rows = soup.find('table').find('tbody').find_all('tr')

        # Find the row that contains the given Hebrew word
        correct_row = next((i for i, row in enumerate(table_rows) if strip_vowels(row.find('span', class_='menukad').get_text()) == hebrew), None)

        # If the Hebrew word was found in the conjugation table, print the details of the row
        if correct_row is not None:
            columns = table_rows[correct_row].find_all('td')
            for column in columns:   
                column_details = {
                    'word': column.find('span', class_='menukad').get_text(),
                    'transcription': column.find('div', class_='transcription').get_text(),
                    'meaning': column.find('div', class_='meaning').get_text(),
                }
                print(column_details)
        else:
            print('Hebrew word not found in the conjugation table of the most similar word.')
    except Exception as error:
        print('There was an error:', error)

searchWord("להראות", "to show")