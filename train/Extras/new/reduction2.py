import json

def adjust_labels(input_file, output_file):
    """
    Adjust the 'end' attribute in 'soft_labels' and the second value in 'hard_labels'
    for each object in the JSONL file.

    Args:
    - input_file (str): Path to the input JSONL file.
    - output_file (str): Path to save the modified JSONL file.

    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            obj = json.loads(line)
            
            # Update 'soft_labels'
            if 'soft_labels' in obj:
                for label in obj['soft_labels']:
                    if 'end' in label:
                        label['end'] -= 1
            
            # Update 'hard_labels'
            if 'hard_labels' in obj:
                obj['hard_labels'] = [[start, end - 1] for start, end in obj['hard_labels']]
            
            # Write the updated object back to the new file
            outfile.write(json.dumps(obj) + '\n')

# Usage example
input_file_path = '/path/to/your/input.jsonl'
output_file_path = '/path/to/your/output.jsonl'
adjust_labels(input_file_path, output_file_path)
print(f"Updated file saved to {output_file_path}")
