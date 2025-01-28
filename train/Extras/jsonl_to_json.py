import json

def jsonl_to_json(input_path, output_path):
    # Open the JSONL file and read line by line
    with open(input_path, 'r') as infile:
        data = [json.loads(line) for line in infile]
    
    # Write the list of JSON objects into a JSON file
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)

# Example usage
input_file =  "/home/chinjoyce/Downloads/val/mushroom.en-val.v2.jsonl" # Replace with your input JSONL file path
output_file = "/home/chinjoyce/Downloads/train/Extras/mushroom.en-val.v2.json" # Replace with your output JSON file path

jsonl_to_json(input_file, output_file)
