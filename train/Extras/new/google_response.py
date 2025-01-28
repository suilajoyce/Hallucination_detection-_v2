import requests
from bs4 import BeautifulSoup
import wikipediaapi

def google_search(query):
    """Perform a Google search and return the top search results."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Google search failed. Please try again.")
    return response.text

def extract_wikipedia_link(search_results):
    """Extract the first Wikipedia link from Google search results."""
    soup = BeautifulSoup(search_results, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "wikipedia.org/wiki/" in href:
            # Extract the actual Wikipedia link
            start = href.find("http")
            end = href.find("&", start)
            return href[start:end] if end != -1 else href[start:]
    return None

def fetch_wikipedia_content(wikipedia_url):
    """Fetch and return the Wikipedia page content."""
    wiki = wikipediaapi.Wikipedia("en")
    page_name = wikipedia_url.split("/wiki/")[-1]
    page = wiki.page(page_name)
    if not page.exists():
        raise Exception("Wikipedia page not found.")
    return page.text

def main():
    query = input("Enter your search query: ")
    try:
        # Perform Google search
        search_results = google_search(query)
        
        # Extract Wikipedia link
        wikipedia_link = extract_wikipedia_link(search_results)
        if not wikipedia_link:
            print("No Wikipedia page found for the query.")
            return
        
        print(f"Found Wikipedia page: {wikipedia_link}")
        
        # Fetch Wikipedia content
        content = fetch_wikipedia_content(wikipedia_link)
        print("\nWikipedia Content:\n")
        print(content[:1000])  # Print the first 1000 characters as a preview
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
