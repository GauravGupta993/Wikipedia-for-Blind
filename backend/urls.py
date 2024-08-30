import requests
from bs4 import BeautifulSoup

# Function to get all hyperlinks from a Wikipedia page
def get_wikipedia_links(url):
    # Send a GET request to the Wikipedia page
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> tags, which represent hyperlinks
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Filter for proper URLs (excluding fragment identifiers and Wikipedia-specific links)
        if href.startswith('/wiki/') and not href.startswith('/wiki/Special:'):
            full_url = 'https://en.wikipedia.org' + href
            links.append(full_url)
    
    return links

# URL of the Wikipedia page to scrape
wiki_url = 'https://en.wikipedia.org/wiki/Albert_Einstein'

# Get all hyperlinks from the Wikipedia page
all_links = get_wikipedia_links(wiki_url)

# Print the list of hyperlinks
for link in all_links:
    print(link)
