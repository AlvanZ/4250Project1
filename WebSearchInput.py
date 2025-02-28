import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque
import re
# 1. Make method to get the seed url
# 2. GO to page, error handle if it doesn't exist. Then you save that page
# 3. Check if page is in set, if not then add it and then go through all anchor tags that contain the seed url
# 4. Recurse to 2
# Needs set to prevent duplicates, and then language detection.



def count_html_files(directory):
    return sum(1 for file in os.listdir(directory) if file.endswith(".html"))


def run(pages: int, directoryLocation: str):
    if(count_html_files(directoryLocation)==pages):
        return "Job Done"
# Function to normalize and filter URLs
def normalize_url(base_url, link, allowed_domains, excluded_domains):
    absolute_url = urljoin(base_url, link)
    parsed_url = urlparse(absolute_url)
    print (parsed_url.netloc)
    #print (allowed_domains)
    # Check domain restrictions
    if allowed_domains and parsed_url.netloc not in allowed_domains:
        print(f"link is not in allowed domain...")
        return None
    if excluded_domains and parsed_url.netloc in excluded_domains:
        print(f"link is EXCLUDED domain...")
        return None
    print(f"valid link... \n")
    return absolute_url

# Function to extract links from a page
def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we get a valid response
        soup = BeautifulSoup(response.text, 'html.parser')

        links = set()
        for a_tag in soup.find_all('a', href=True):
            links.add(a_tag['href'])
        
        return links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

# Function to save the HTML content of a page to a file
def save_page(url, content, base_dir):
    parsed_url = urlparse(url)
    # Sanitize URL to create a valid filename
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', parsed_url.path.strip('/'))
    if not filename:
        filename = 'index'
    file_path = os.path.join(base_dir, f"{filename}.txt")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save content to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved: {file_path}")

# Web Crawler
def crawl(seed_urls, allowed_domains=None, excluded_domains=None):
    visited = set()
    to_visit = deque(seed_urls)

    # Extract domain to use as folder name
    domain = urlparse(seed_urls[0]).netloc
    base_dir = domain.replace("www.", "")  # Remove 'www.' if present

    while to_visit:
        current_url = to_visit.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        print(f"Crawling: {current_url}")
        
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                save_page(current_url, response.text, base_dir)
                links = extract_links(current_url)
            
                for link in links:
                    normalized_url = normalize_url(current_url, link, allowed_domains, excluded_domains)
                    print (f"link with nomralized url: ", normalized_url)
                    # **Ensure every extracted link is added at least once**
                    if normalized_url and normalized_url not in visited and normalized_url not in to_visit:
                        to_visit.append(normalized_url)

        except requests.RequestException as e:
            print(f"Failed to fetch {current_url}: {e}")

# Example usage
seed_urls = [ 'https://www.obsidian.net/', 'https://www.cpp.edu' ]
#doesnt check allowed domain for the frst parse

#use parsed_url.netloc to save to proper directory
allowed_domains = ['www.cpp.edu', 'www.obsidian.net']
excluded_domains = ['example.org']

crawl(seed_urls, allowed_domains=allowed_domains, excluded_domains=excluded_domains)
