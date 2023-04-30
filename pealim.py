import csv

csv_file = 'words.csv'
with open(csv_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

categories = {}

# Group words by category
for item in data:
    if item['Title'] not in categories:
        categories[item['Title']] = []
    categories[item['Title']].append({
        'word': item['Word'],
        'meaning': item['Meaning'], 
        'niqqud': item['Niqqud']
        })


with open('revised.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Word', 'Meaning'])
        
        out.flush()