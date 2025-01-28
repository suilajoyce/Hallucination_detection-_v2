from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(sentence1, sentence2):
    # Create the vectorizer
    vectorizer = TfidfVectorizer()
    
    # Fit and transform the sentences into TF-IDF vectors
    vectors = vectorizer.fit_transform([sentence1, sentence2])
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:2])
    
    return cosine_sim[0][0]  # Return the similarity score

# Example usage
sentence1 = "alberto"
sentence2 = "albero"
similarity_score = calculate_cosine_similarity(sentence1, sentence2)
print(f"Cosine Similarity: {similarity_score:.8f}")
