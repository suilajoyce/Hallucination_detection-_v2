import numpy as np

def softmax(logits):
    """
    Computes the softmax probabilities for a set of logit values.

    Args:
        logits (list or np.ndarray): A list or array of logit values.

    Returns:
        np.ndarray: The softmax probabilities.
    """
    # Subtract the maximum logit for numerical stability
    logits = np.array(logits)
    exp_values = np.exp(logits - np.max(logits))
    probabilities = exp_values / np.sum(exp_values)
    return probabilities

def average_softmax(logits):
    """
    Calculates the average of softmax probabilities for a set of logit values.

    Args:
        logits (list or np.ndarray): A list or array of logit values.

    Returns:
        float: The average of the softmax probabilities.
    """
    probabilities = softmax(logits)
    return np.mean(probabilities)

# Example usage
logits = [-11.1029033661, -8.5361289978]
average_probability = average_softmax(logits)
print("Softmax probabilities:", softmax(logits))
print("Average of softmax probabilities:", average_probability)
