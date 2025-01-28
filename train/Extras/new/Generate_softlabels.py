import json
import numpy as np
from typing import List, Dict

def softmax(logits: List[float]) -> List[float]:
    """Apply softmax to logits to get probabilities."""
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / exp_logits.sum()

def generate_labels(data: List[Dict], threshold: float = 0.5) -> List[Dict]:
    """
    Generate soft_labels and hard_labels for the given data.
    
    Args:
        data: List of dictionaries containing model_output_text and model_output_logits.
        threshold: Probability threshold for determining hard_labels.
        
    Returns:
        List of dictionaries with soft_labels and hard_labels added.
    """
    results = []
    
    for entry in data:
        output_text = entry["model_output_text"]
        output_logits = entry["model_output_logits"]
        output_tokens = entry["model_output_tokens"]

        # Generate spans (soft_labels)
        soft_labels = []
        start = 0
        for token, logit in zip(output_tokens, output_logits):
            end = start + len(token)
            prob = softmax([logit])[0]  # Convert logit to probability
            soft_labels.append({"start": start, "prob": prob, "end": end})
            start = end

        # Generate hard_labels
        hard_labels = [
            [span["start"], span["end"]]
            for span in soft_labels if span["prob"] > threshold
        ]
        
        # Append results
        entry["soft_labels"] = soft_labels
        entry["hard_labels"] = hard_labels
        results.append(entry)

    return results

# Example Usage
if __name__ == "__main__":
    input_file = "/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/deleted_labels.jsonl"
    output_file = "/home/chinjoyce/Downloads/MUSHROOM-task3/train/Extras/new/testwithdeletedlabels.jsonl"

    # Load the input data
    with open(input_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    # Generate soft_labels and hard_labels
    labeled_data = generate_labels(data)

    # Save the output
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in labeled_data:
            f.write(json.dumps(entry) + "\n")
