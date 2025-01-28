import requests

import spacy
nlp = spacy.load("en_core_web_sm")
def extract_subject(text):
    doc=nlp(text)
    for token in doc:
        if "subj" in token.dep_:
            return token.text
    return "subject not found"

text="Does cornsalad have flowers?"
subject = extract_subject(text)
print("Extracted Subject:", subject)





def search_wikipedia(query):
    # Step 1: Search for articles
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query
    }
    search_response = requests.get(search_url, params=search_params)
    search_data = search_response.json()
    #print(search_data)

    if not search_data['query']['search']:
        return "No results found."

    # Get the title of the first article
    title = search_data['query']['search'][0]['title']
    print(title)

    # Step 2: Retrieve the summary of the article
    extract_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": title
    }
    extract_response = requests.get(search_url, params=extract_params)
    extract_data = extract_response.json()

    # Extract the summary
    page = next(iter(extract_data['query']['pages'].values()))
    return page.get("extract", "Summary not available.")

# Example usage
query = subject
subject = extract_subject(query)
description = search_wikipedia('')
print(description)


# import wikipedia

# def extract_wikipedia_response(query):
#     try:
#         # Search for the query in Wikipedia
#         search_results = wikipedia.search(query)
        
#         if not search_results:
#             return "No results found for the query."

#         # Get the first result's title
#         page_title = search_results[0]
        
#         # Retrieve the summary of the page
#         summary = wikipedia.summary(page_title)
        
#         return {
#             "title": page_title,
#             "summary": summary,
#             "url": wikipedia.page(page_title).url
#         }
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Example usage
# query = "Captain Morgan invented"
# response = extract_wikipedia_response(query)

# print("Title:", response['title'])
# print("Summary:", response['summary'])
# print("URL:", response['url'])