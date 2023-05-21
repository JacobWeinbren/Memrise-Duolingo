import json

# Open and load the json file
with open('data.json', 'r') as f:
    data = json.load(f)

# Convert data to the new format
new_data = [{'prompt': k, 'completion': v} for k, v in data.items()]

# Save the new json data to a file
with open('output.json', 'w') as f:
    for line in new_data:
        json.dump(line, f)
        f.write('\n')  # Write each dictionary in new line