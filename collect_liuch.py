import requests
from bs4 import BeautifulSoup

response = requests.get('https://liuch.github.io/duolingo_courses_overview/html/tree_he_en_084.html')
soup = BeautifulSoup(response.content, "html.parser")
translations = {}

word_blocs = soup.find_all("li")
data = []
for bloc in word_blocs:
    if 'Words:' in bloc.text:
        words = bloc.text.replace('Words: ','').split(",")
        data += words

with open('liuch.txt', 'w') as f:
    for line in data:
        f.write(f"{line}\n")