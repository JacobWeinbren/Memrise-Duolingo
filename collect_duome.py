import ujson, csv

data = []
with open('Source_Duome.json') as f:
    words = ujson.load(f)
    for word in words['vocab_overview']:
        data.append([word['skill'], word['word_string']])

with open('Source_Duome.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['Skill', 'Word'])
    for word in data:
        csv_out.writerow([word[0], word[1]])
