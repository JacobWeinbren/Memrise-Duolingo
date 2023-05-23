import requests
import re
from bs4 import BeautifulSoup
import csv

# Define the url to be scraped
base_url = 'https://duolingo.fandom.com'

def get_skill_links(url, skills):
    """
    Function to get links for each skill
    """
    # Send a GET request to the url
    response = requests.get(url)
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a dictionary to store the skill links
    skill_links = {}

    # Iterate over the skills
    for skill in skills:
        # Find the anchor tag with the title matching the skill
        link = soup.find('a', title='Hebrew Skill:'+skill)

        # If a link was found
        if link:
            # Store the href attribute of the link in the dictionary
            skill_links[skill] = link['href']

    return skill_links

def get_words_from_lessons(url):
    """
    Function to get words from the lessons of a skill
    """
    # Send a GET request to the url
    response = requests.get(url)
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all h3 elements on the page
    lessons = soup.find_all('h3')

    # Initialize a list to store the words
    words = []

    # Iterate over the lessons
    for lesson in lessons:
        # Get the text content of the lesson, removing leading/trailing whitespace
        lesson_title = lesson.text.strip()

        # If the lesson title contains "Lesson"
        if 'Lesson' in lesson_title:

            # Find the next sibling element that is a ul
            ul = lesson.find_next_sibling('ul')

            # If a ul was found
            if ul:
                # Iterate over all li elements inside the ul
                for li in ul.find_all('li'):
                    # Split the text content of the li on the equals sign and get the first part, removing leading/trailing whitespace
                    word = li.text.split('=')[0].strip()

                    # Remove non-Hebrew characters
                    word = re.sub('[^א-ת ]', '', word)
                    words.append(word)

    return words

# List of skills to be scraped
skills = ['Letters 1', 'Letters 2', 'Letters 3', 'Phrases', 'Basics', 'There is', 'Adjectives: Intro', 'Food 1', 'Animals', 'Plurals', 'Possessives 1', 'Adjectives 1', 'Direct Object', 'Food 2', 'Clothing', 'Verbs: Present 1', 'Colors', 'Prepositions 1', 'Numbers 1', 'Questions', 'Determiners', 'Occupation', 'Conjunctions', 'Prepositions 2', 'Possessives 2', 'Verbs: Present 2', 'Time', 'Adjectives 2', 'Adverbs', 'Family', 'Home', 'Construct State 1', 'Verbs: Infinitive 1', 'Weather', 'Places', 'Verbs: Present 3', 'People', 'Numbers 2', 'Verbs: Modals', 'Education', 'Travel', 'Verbs: Past', 'Comparison', 'Objects', 'Verbs: Present Reflexive', 'Adjectives 3', 'Abstract Objects 1', 'Imperative 1', 'Languages', 'Emergency!', 'Verbs: Future 1', 'Passive', 'Reflexive Pronouns', 'Nif\'al', 'Nature', 'Decisions', 'Imperative 2', 'Verbs: Past Actions 2', 'Verbs: Past Nif\'al', 'Feelings', 'Geometry', 'Abstract Objects 2', 'Verbs: Infinitive 2', 'Construct State 2', 'Verbs: Conditional', 'Medical', 'Verbs: Future 2', 'Religion', 'Arts', 'Negative Imperative', 'Technology', 'Verbal Nouns', 'Science', 'Music', 'Sports', 'Politics', 'Diminutive', 'Legends', 'Future Nif\'al', 'Formal', 'Business', 'Space', 'Festivals', 'Israel']

# Get the links for the skills
skill_links = get_skill_links(base_url + '/wiki/Hebrew', skills)

# Open a CSV file in write mode
with open('Source_Wiki.csv', 'w', newline='', encoding='utf-8') as file:
    # Initialize a CSV writer
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Skill', 'Word'])

    # Iterate over the skill links
    for skill, link in skill_links.items():
        print(skill)
        # Concatenate the base_url with the link to form the full url
        url = base_url + link

        # Get the words from the lessons of the skill
        words = get_words_from_lessons(url)

        # Iterate over the words
        for word in words:
            # Write a row to the CSV file with the skill and the word
            writer.writerow([skill, word])
