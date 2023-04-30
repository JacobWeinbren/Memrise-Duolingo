from anki import Collection

# Replace 'path/to/your/collection.anki2' with the actual path to your .anki2 file
collection = Collection("typing/collection.anki2")

# Get the notes DataFrame
notes = collection.decks

print(notes)