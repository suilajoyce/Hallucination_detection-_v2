import wikipedia

def extract_wikipedia_response(query):
    try:
        # Search for the query in Wikipedia
        search_results = wikipedia.search(query)
        
        if not search_results:
            return "No results found for the query."

        # Get the first result's title
        page_title = search_results[0]
        
        # Retrieve the summary of the page
        summary = wikipedia.summary(page_title)
        
        return {
            "title": page_title,
            "summary": summary,
            "url": wikipedia.page(page_title).url
        }
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
query = "Does cornsalad have flowers?"
response = extract_wikipedia_response(query)

print("Title:", response['title'])
print("Summary:", response['summary'])
print("URL:", response['url'])