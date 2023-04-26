import os, re
import csv
from google.cloud import texttospeech
from google.oauth2 import service_account

# Load the credentials from the credentials.json file
credentials = service_account.Credentials.from_service_account_file('credentials.json')

# Create a TextToSpeechClient with the loaded credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Build the voice request, select the language code ("he-IL") and the ssml gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="he-IL", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

"""Generate TTS audio for a word and save it to a file using Google TTS."""
def get_sound(word, meaning, file, index):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=word)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(os.path.join(file, f"{index}-{word}.mp3"), "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)

    print(f"Generated TTS audio for: {word}, {meaning} using Google TTS")


# Read the CSV file as a list of dictionaries
csv_file = 'words.csv'
with open(csv_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

categories = {}

# Group words by category
for item in data:
    if item['Title'] not in categories:
        categories[item['Title']] = []
    categories[item['Title']].append([item['Word'], item['Meaning']])

# Loop through categories and create output folders
for index, category in enumerate(categories):
    output_folder = 'storage/' + str(index) + ' - ' + category
    os.makedirs(output_folder, exist_ok=True)

    # Write category data to CSV
    with open(output_folder + '/' + category + '.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['Word', 'Meaning'])
        csv_out.writerows(categories[category])

    # Generate TTS audio for each word in the category
    for index, word in enumerate(categories[category]):
        simplified_word = re.sub("[\(\[].*?[\)\]]", "", word[0]).strip()
        meaning = re.sub("[\(\[].*?[\)\]]", "", word[1]).strip()
        output_file = os.path.join(output_folder, f"{index}-{simplified_word}.mp3")
        if not os.path.exists(output_file):
            get_sound(simplified_word, meaning, output_folder, index)