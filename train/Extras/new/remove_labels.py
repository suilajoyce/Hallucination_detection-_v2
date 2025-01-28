import json

def remove_labels_from_jsonl(input_file, output_file):
  """
  Reads a JSONL file, removes 'soft_labels' and 'hard_labels' 
  attributes from each element, and writes the modified data to a new JSONL file.

  Args:
    input_file: Path to the input JSONL file.
    output_file: Path to the output JSONL file.
  """
  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
      data = json.loads(line)
      data.pop('soft_labels', None) 
      data.pop('hard_labels', None) 
      outfile.write(json.dumps(data) + '\n')

if __name__ == "__main__":
  input_jsonl = "/home/chinjoyce/Downloads/MUSHROOM-task3/val/mushroom.en-val.v2.jsonl"  # Replace with your input file path
  output_jsonl = "/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/deleted_labels.jsonl"  # Replace with your desired output file path
  remove_labels_from_jsonl(input_jsonl, output_jsonl)