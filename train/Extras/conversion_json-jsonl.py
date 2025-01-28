import json

def convert_json_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            return
    
    with open(output_file, 'w') as jsonl_file:
        for item in data:
            jsonl_file.write(json.dumps(item) + '\n')

# Example usage
convert_json_to_jsonl('/home/chinjoyce/Downloads/train/Extras/mushroom.en-train_nolabel.v2.json', '/home/chinjoyce/Downloads/train/Extras/test.jsonl')