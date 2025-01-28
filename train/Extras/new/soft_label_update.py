import json
import re

def merge_token(token_list):
    merged_tokens = []
    current_token = ""

    for token in token_list:
        if token == "<|endoftext|>":  # Ignore the end-of-text token
            continue
        if token == "<\/s>":  # Ignore the end-of-sequence token
            continue
        if token == "</s>":  # Ignore the end-of-sequence token
            continue

        if token == ".":  # Ignore isolated period
            if current_token:  # Add the current token without the period
                merged_tokens.append(current_token)
            current_token = ""
            continue

        if not token.startswith("\u0120"):  # No space at the start of the token => merge it
            current_token += token
        else:  # Token starts with space => start a new word
            if current_token:  # Add the current merged token to the list
                merged_tokens.append(current_token)
            current_token = token  # Start a new word

    # Add the last token if it's valid
    if current_token and current_token != ".":
        merged_tokens.append(current_token)

    return merged_tokens

def group_tokens_into_words(token_list):
    grouped_words = []
    current_word = []

    for token in token_list:
        if token.startswith("\u0120"):  # Indicates a token starting with space (new word)
            if current_word:
                grouped_words.append("".join(current_word))  # Join and store the current word
            current_word = [token.lstrip("\u0120")]  # Start a new word
        else:
            current_word.append(token)  # Add token to the current word

    if current_word:
        grouped_words.append("".join(current_word))  # Append the last word

    return grouped_words

def create_spans_from_tokens(token_list, model_input_text):
    spans = []
    current_position = 0  # Start at the beginning of the model_input_text

    # Group tokens into words (tokens without space between them)
    grouped_words = group_tokens_into_words(token_list)

    for word in grouped_words:
        word_start = -1
        word_end = -1

        # Process each token in the grouped word
        for i, token in enumerate(word.split()):
            token_clean = token.strip()  # Clean the token (removes leading/trailing spaces)

            # Search for the token in the model_input_text starting from the current_position
            token_start = model_input_text.find(token_clean, current_position)

            if token_start != -1:
                token_end = token_start + len(token_clean)  # End index of the token
                current_position = token_end  # Move the current_position forward
            else:
                # If any token in the word is not found, mark that we need to create spans for each token
                word_start = -1
                break  # Stop looking for the rest of the tokens in the word if one is not found

        if word_start == -1:
            # Add each token as a separate span if the word was not fully found
            for token in word.split():
                token_clean = token.strip()  # Clean the token
                token_start = model_input_text.find(token_clean, current_position)
                if token_start != -1:  # Only add spans for tokens found in model_input_text
                    token_end = token_start + len(token_clean)
                    spans.append({"start": token_start, "end": token_end, "prob": 1})
                    current_position = token_end  # Update current_position to the end of the token
                else:
                    print(f"Token '{token}' not found in model_input_text.")  # Debugging info

    return spans

def process_json_and_update_jsonl(output_jsonl_file, soft_labels_list):
    with open(output_jsonl_file, 'w', encoding='utf-8') as out_file:
        for soft_labels in soft_labels_list:
            for label in soft_labels:
                out_file.write(json.dumps(label) + '\n')

    print(f"Soft labels have been written to {output_jsonl_file}")

def main(input_file_path, reference_file_path):
    soft_labels_list = []

    # Open input file and reference response file
    with open(input_file_path, 'r') as input_file, open(reference_file_path, 'r') as ref_file:
        input_lines = input_file.readlines()
        reference_data = json.load(ref_file)

        if len(input_lines) != len(reference_data):
            raise ValueError("Input and reference files must have the same number of elements.")

        # Process each line from both files
        for input_line, reference_item in zip(input_lines, reference_data):
            item = json.loads(input_line.strip())
            reference_response = reference_item['ref']  # 'ref' attribute in reference file

            model_input = item['model_input']
            model_output_tokens = item['model_output_tokens']
            model_output_text = item["model_output_text"]

            # Step 1: Merge tokens
            merged_tokens = merge_token(model_output_tokens)

            # Step 2: Create spans for merged tokens, filtering based on the model_input
            soft_labels = create_spans_from_tokens(merged_tokens, model_input)

            # Step 3: Determining probability for each span
            for span in soft_labels:
                span_text = model_input[span['start']:span['end']]
                if span_text in reference_response:
                    span['prob'] = 0  # If found in reference response, probability = 0
                else:
                    span['prob'] = 1  # Otherwise, probability = 1

            soft_labels_list.append(soft_labels)

            # Display result for debugging
            print(f"ID: {item['id']}")
            print(f"Soft Labels: {soft_labels}\n")

        return soft_labels_list

# Example of usage
if __name__ == "__main__":
    reference_response_file_path = "/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/reference_response-en.json"
    file_path = "/home/chinjoyce/Downloads/MUSHROOM-task3/test-unlabeled/v1/converted_test_en.jsonl"  # Your file here
    output_jsonl_file = "/home/chinjoyce/Downloads/MUSHROOM-task3/test-unlabeled/Results.jsonl"  # Your output file here

    # Running the main function
    soft_labels_list = main(file_path, reference_response_file_path)
    process_json_and_update_jsonl(output_jsonl_file, soft_labels_list)
    print("Submission ready!!!")
