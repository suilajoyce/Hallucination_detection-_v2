import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances

def find_closest_paragraph(target_text, paragraphs):
    """
    Finds the paragraph closest to the target_text using Euclidean distance.
    
    Parameters:
        target_text (str): The text to compare with the list of paragraphs.
        paragraphs (list of str): A list of paragraphs to search.

    Returns:
        str: The paragraph closest to the target_text.
    """
    # Combine the target text with the list of paragraphs
    texts = [target_text] + paragraphs

    # Convert texts to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute the Euclidean distances between the target text and each paragraph
    distances = euclidean_distances(tfidf_matrix[0], tfidf_matrix[1:]).flatten()

    # Find the index of the closest paragraph
    closest_index = np.argmin(distances)

    return paragraphs[closest_index]

# Example usage
target_text = "Elon Musk is a technology entrepreneur and investor."
paragraphs = [
    "Albert Einstein developed the theory of relativity.",
    "Elon Musk is the CEO of Tesla and SpaceX.",
    "Marie Curie was a physicist and chemist who conducted pioneering research on radioactivity.",
    "Isaac Newton formulated the laws of motion and universal gravitation."
]

closest_paragraph = find_closest_paragraph(target_text, paragraphs)
print("Closest paragraph:")
print(closest_paragraph)
