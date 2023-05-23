# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the webpage
url = "https://liuch.github.io/duolingo_courses_overview/html/tree_he_en_084.html"

# Define the list of new skill names
new_skill_names = [
    "Letters 1", "Letters 2", "Letters 3", "Common Phrases", "Basics", "There is/To Have", 
    "Introduction to adjectives", "Food 1", "Animals", "Plurals", "Possessives 1", 
    "Adjectives 1 - Basics", "Direct Object", "Food 2", "Clothing", "Verbs: Present - Pa'al", 
    "Colors", "Prepositions 1", "Numbers 1", "Questions", "Determiners", "Occupations", 
    "Conjunctions", "Prepositions 2", "Possessives 2", "Verbs: Present - Pi'el", "Dates and Time", 
    "Adjectives 2", "Adverbs", "Family", "Home Sweet Home", "Construct State 1", "Infinitives 1", 
    "Weather", "Places", "Verbs: Present - Hiph'il", "People", "Numbers 2", "Modals", "Education", 
    "Travel", "Verbs: Past Active 1", "Comparison", "Objects", "Verbs: Present Reflexive - Hitpa'el", 
    "Adjectives 3", "Abstract Objects 1", "Imperative 1", "Languages", "Emergency!", 
    "Verbs: Future Active 1", "Passive: Pa'ul, Pu'al and Huf'al", "Pronouns: Reflexive", 
    "Nif'al Construction", "Nature", "Discussions and decisions", "Imperative 2", 
    "Verbs: Past Active 2", "Past Nif'al", "Feelings", "Geometry", "Abstract Objects 2", 
    "Infinitives 2", "Construct State 2", "The Conditional", "Medical", "Future 2", "Religion", 
    "Arts", "Negative Imperatives", "Technology and Communication", "Verbal Nouns", "Science", 
    "Music", "Sports", "Politics", "Diminutives", "Legends", "Future Nif'al", "Formal", "Business", 
    "Outer Space", "Jewish Festivals", "Welcome To Israel"
]

# Send a GET request to the webpage and get the content
response = requests.get(url)
content = response.content

# Parse the content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Open a new CSV file to write the data
with open('Source_Liuch.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Skill", "Word"])  # Write the header

    # Find all h3 elements (the skills)
    skills = soup.find_all('h3')

    # For each skill
    for i, skill in enumerate(skills):
        # Replace the skill name with the corresponding name from the new list
        skill_name = new_skill_names[i]

        # Find the next sibling element that contains the words
        words_container = skill.find_next_sibling('ul')

        # If the words container exists
        if words_container:
            # Find all li elements in the words container
            li_elements = words_container.find_all('li')

            # If there are at least 3 li elements
            if len(li_elements) >= 3:
                # Get the text of the 3rd li element
                words_text = li_elements[2].text

                # Find the text after 'Words:' and split it into individual words
                words = words_text.split('Words: ')[-1].split(', ')

                # For each word
                for word in words:
                    # Write the skill name and word to the CSV file
                    writer.writerow([skill_name, word])