# Importing necessary libraries
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

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

model_name = "sentence-transformers/paraphrase-distilroberta-base-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

import unicodedata

def strip_vowels(hebrew_text):
    return ''.join(c for c in unicodedata.normalize('NFD', hebrew_text) if unicodedata.category(c) != 'Mn')

def searchWord(hebrew, initial_translation):

  try:
      # Sending a get request to the pealim.com with the search word
      response = requests.get(f'https://www.pealim.com/search/?q={hebrew}')

      # Parsing the response text
      soup = BeautifulSoup(response.text, 'html.parser')

      # Extracting the page header text
      page_title = soup.find('h3', class_='page-header').get_text()

      # Finding all divs containing verb search results
      search_results = soup.find_all('div', class_='verb-search-result')

      # List to store query results
      query_results = []

      # Iterating over each verb in the search results
      translations = {}
      for verb in search_results:

          link = verb.find('div', class_='verb-search-lemma').find('a').get('href')
          translation = verb.find('div', class_='vf-search-tpgn-and-meaning').get_text().split(":")[1]

          translations[translation] = link

      max_similarity = 0
      similarity = 0

      for translation in translations.keys():
          similarity = semantic_similarity(initial_translation, translation, model, tokenizer)
          if similarity > max_similarity:
              max_similarity = similarity
              most_similar_word = translation

      print(most_similar_word)

      link = translations[most_similar_word]

      response = requests.get(f'https://www.pealim.com{link}')
      soup = BeautifulSoup(response.text, 'html.parser')

      # Extracting the conjugation table rows
      table_rows = soup.find('table').find('tbody').find_all('tr')

      correct_row = False

      # Iterating over each row in the conjugation table
      for a, row in enumerate(table_rows):
          # Extracting details from each column in the row
          columns = row.find_all('td')
          for b, column in enumerate(columns):   
            word = strip_vowels(column.find('span', class_='menukad').get_text())
            if word == hebrew:
                correct_row = a

      for a, row in enumerate(table_rows):
        if a == correct_row:
          for b, column in enumerate(columns):   
            column_details = {
                'word': column.find('span', class_='menukad').get_text(),
                'transcription': column.find('div', class_='transcription').get_text(),
                'meaning': column.find('div', class_='meaning').get_text(),
            }
            print(column_details)

  # Handling any exceptions during the process
  except AssertionError as error:
      print('There was an error')

searchWord("להראות", "to show")