import json

def adjust_labels(input_file, output_file):
    """
    Adjusts the "end" attribute in "soft_labels" and the second value in "hard_labels" for each object in a JSONL file.

    Parameters:
    - input_file: Path to the input JSONL file.
    - output_file: Path to save the modified JSONL file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            obj = json.loads(line)
            
            # Adjust "soft_labels"
            if "soft_labels" in obj:
                for label in obj["soft_labels"]:
                    label["end"] = max(0, label["end"] - 1)  # Ensure non-negative values
            
            # Adjust "hard_labels"
            if "hard_labels" in obj:
                obj["hard_labels"] = [
                    [start, max(0, end - 1)]  # Ensure non-negative values
                    for start, end in obj["hard_labels"]
                ]
            
            # Write the modified object back to the output file
            outfile.write(json.dumps(obj) + '\n')

# Example usage
input_path = '/home/chinjoyce/Downloads/train/Extras/new/submission_2.jsonl'
output_path = '/home/chinjoyce/Downloads/train/Extras/new/output.jsonl'
adjust_labels(input_path, output_path)
print(f"File processed and saved to {output_path}")
