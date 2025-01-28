import json

def verify_end_value(input_file):
    """
    Verifies whether the "end" attribute in "soft_labels" corresponds to the length of "model_output_text" - 1.
    
    Parameters:
    - input_file: Path to the input JSONL file.
    
    Returns:
    - List of tuples (line_number, object_id, discrepancy) where discrepancies are found.
    """
    discrepancies = []
    
    with open(input_file, 'r') as infile:
        for line_number, line in enumerate(infile, start=1):
            obj = json.loads(line)
            
            model_output_text = obj.get("model_output_text", "")
            expected_end = len(model_output_text) - 1
            
            for label in obj.get("soft_labels", []):
                if label.get("end") != expected_end:
                    discrepancies.append((line_number, obj.get("id"), label.get("end"), expected_end))
    
    return discrepancies

# Example usage
input_path = '/home/chinjoyce/Downloads/train/Extras/new/output.jsonl'
discrepancies = verify_end_value(input_path)

# Print the results
if discrepancies:
    print("Discrepancies found in the following data items:")
    for line_number, obj_id, actual_end, expected_end in discrepancies:
        print(f"Line {line_number}, ID {obj_id}: 'end' = {actual_end}, expected = {expected_end}")
else:
    print("No discrepancies found. All 'end' values match the expected length.")
