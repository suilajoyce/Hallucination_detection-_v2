import json

def update_jsonl_with_soft_labels(carick_file, deleted_file, output_file, key='id'):
    # Read the carick_results JSONL
    with open(carick_file, 'r', encoding='utf-8') as f:
        carick_data = [json.loads(line) for line in f]

    # Read the deleted_labels JSONL and create a dictionary with id as the key
    with open(deleted_file, 'r', encoding='utf-8') as f:
        deleted_data = {json.loads(line)[key]: json.loads(line) for line in f}
    
    # Add soft_labels from carick_results to the corresponding entry in deleted_labels
    for entry in carick_data:
        if entry[key] in deleted_data:
            deleted_data[entry[key]]['soft_labels'] = entry['soft_labels']
    
    # Write the updated data back to the carick_results file (output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in deleted_data.values():
            f.write(json.dumps(entry) + '\n')

# Example usage
carick_file = '/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/carick_results.jsonl'
deleted_file = '/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/deleted_labels.jsonl'
output_file = '/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/carick_results.jsonl'

update_jsonl_with_soft_labels(carick_file, deleted_file, output_file)
