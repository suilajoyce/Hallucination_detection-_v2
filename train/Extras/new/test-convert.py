import json

# Load your JSON file
with open('mushroom.en-val.v2.json', 'r') as infile:
    data = json.load(infile)

# Write to a new JSONL file
with open('test.jsonl', 'w') as outfile:
    for entry in data:
        # Write each JSON object on a new line
        json.dump(entry, outfile)
        outfile.write('\n')
