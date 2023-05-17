## IMPORTS
import requests
from bs4 import BeautifulSoup
import sys
import json

## GET WORD TO SEARCH
query = input('Word to search: ')

## GET PEALIM
## TODO: Make json and save it in MongoDb
try:
  r = requests.get('https://www.pealim.com/search/?q=' + query)
  soup = BeautifulSoup(r.text, 'html.parser')
  title = soup.find('h3', class_='page-header').get_text()
  result = soup.find_all('div', class_='verb-search-result')
  queryResult = list()
  for verb in result:
    ## HEADER
    idWord = verb.find('div', class_='verb-search-lemma').find('a').get('href').split('-')[0][6:10]
    link = verb.find('div', class_='verb-search-lemma').find('a').get('href')
    word = verb.find('span', class_='menukad').get_text()
    form = verb.find('div', class_='vf-search-hebrew').find('span', class_='menukad').get_text()
    formTranscription = verb.find('div', class_='vf-search-hebrew').find('span', class_='transcription').get_text()
    translation = verb.find('div', class_='vf-search-tpgn-and-meaning').get_text()

    ## CONJUGATION
    r = requests.get('https://www.pealim.com' + link)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table').find('tbody').find_all('tr')

    columnsList = list()
    conjugation = list()
    verbForm = {}

    for row in table:
      verbFormTitle = ''
      if len(row.find_all('th')) > 0:
        verbFormTitle = row.find_all('th')[0].get_text()
      columns = row.find_all('td')
      for column in columns:
        columnDetails = {
          'word': column.find('span', class_='menukad').get_text(),
          'transcription': column.find('div', class_='transcription').get_text(),
          'meaning': column.find('div', class_='meaning').get_text(),
        }
        columnsList.append(columnDetails)
      verbForm = {
        'title': verbFormTitle,
        'forms': columnsList,
      }
      conjugation.append(verbForm)

      

    header = {
      'id': idWord,
      'link': 'https://www.pealim.com' + link,
      'word': word,
      'form': form,
      'transcription': formTranscription,
      'translation': translation,
    }

    data = {
      'header': header,
      'conjugation': conjugation,
    }

    queryResult.append(data)

  resultJson = {
    'query': title,
    'results': queryResult,
  }

  print(resultJson)

except AssertionError as error:
  print('There was an error')