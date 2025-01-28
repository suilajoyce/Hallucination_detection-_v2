import json

def json_to_jsonl(json_file, jsonl_file):
    # Open the input JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)  # Load the JSON content into a Python object

    # Open the output JSONL file for writing
    with open(jsonl_file, 'w') as f:
        if isinstance(data, list):  # If the JSON is a list of objects
            for obj in data:
                json.dump(obj, f)  # Write each object to the file
                f.write('\n')  # Add a newline character after each JSON object
        else:  # If the JSON is a single object, write it as a single line
            json.dump(data, f)
            f.write('\n')

# Example usage:
json_to_jsonl('/home/chinjoyce/Downloads/train/Extras/mushroom.en-val.v2.json', '/home/chinjoyce/Downloads/train/Extras/test.jsonl')
