import requests
import ujson

 # API endpoint
url = 'https://api.rosette.com/rest/v1/name-translation'

# Headers for the API request
headers = {
    "X-RosetteAPI-Key": ""
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}

def transliterate(word):
    """
    This function takes a Hebrew word as input and returns its English transliteration
    using the Rosette API.
    """

    # Data for the API request
    data = {
        "name": word, 
        "sourceScript": "Hebr",
        "sourceLanguageOfOrigin": "heb",
        "sourceLanguageOfUse": "heb",
        "targetLanguage": "eng", 
        "targetScript": "Latn",
        "targetScheme": "ISO259_2_1994"
    }

    # Send the API request
    r = requests.post(url, data=ujson.dumps(data), headers=headers)
    print(r.text)
    # Parse the response and return the translation
    return ujson.loads(r.text)['translation'].lower()

def transliterate_file(input_file, output_file):
    """
    This function takes an input file containing Hebrew words, transliterates them to English,
    and writes the output to another file.
    """
    # Open the input file and read the words
    with open(input_file, 'r') as f:
        words = f.read().splitlines()

    # Open the output file to write the transliterations
    with open(output_file, 'w') as f:
        # Loop through words in batches of 15
        for i in range(0, len(words), 15):
            # Join 15 words with the Hebrew delimiter 'בבב'
            words_joined = ' בבב '.join(words[i:i+15])

            # Transliterate the joined words
            transliteration = transliterate(words_joined)
            print(transliteration)

            # Split the transliteration using the English delimiter 'Bevev'
            transliterations_split = transliteration.split('bbb')

            # Write the split transliterations
            for word in transliterations_split:
                f.write(word.strip() + '\n')  # strip() is used to remove leading and trailing whitespaces
                print(word.strip() + '\n')

# Call the transliterate_file function
transliterate_file('rosette_input.txt', 'rosette_output.txt')