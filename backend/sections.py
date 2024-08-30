import requests
from bs4 import BeautifulSoup

def get_wikipedia_sections(url):
    # Make a request to fetch the content of the page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page: {response.status_code}")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the section headings (h2, h3, h4, etc.)
    sections = []
    for heading in soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
        section_title = heading.get_text().strip()
        sections.append(section_title)

    return sections

# Example usage
url = "https://en.wikipedia.org/wiki/Python_(programming_language)"  # Example Wikipedia page
sections = get_wikipedia_sections(url)

print("Sections found on the page:")
for index, section in enumerate(sections):
    print(f"{index + 1}. {section}")