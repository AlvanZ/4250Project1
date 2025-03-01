import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque
import re
from langdetect import detect
import tldextract
import csv
# 1. Make method to get the seed url
# 2. GO to page, error handle if it doesn't exist. Then you save that page
# 3. Check if page is in set, if not then add it and then go through all anchor tags that contain the seed url
# 4. Recurse to 2
# Needs set to prevent duplicates, and then language detection.


#Count the  number of 
def count_txt_files(directory):
    if(os.path.exists(directory)):
        return sum(1 for file in os.listdir(directory) if file.endswith(".txt"))
    return 0

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"
    
def write_to_csv(url, outlink_count, filename="report.csv"):
    """Appends URL and number of outlinks to a CSV file."""
    try:
        file_exists = os.path.isfile(filename)  # Check if file exists
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["URL" , "Outlinks"])  # Write header if file is new
            writer.writerow([url, outlink_count])  # Append data row
    except Exception as e:
        print(f"Error writing to CSV: {e}")
# Function to normalize and filter URLs
def normalize_url(base_url, link, allowed_domains, excluded_domains):
    absolute_url = urljoin(base_url, link)
    parsed_url = urlparse(absolute_url)
    extracted = tldextract.extract(parsed_url.netloc)
    root_domain = f"{extracted.domain}.{extracted.suffix}"

    # Allow all subdomains of Wikipedia
    if allowed_domains and not any(root_domain.endswith(domain) for domain in allowed_domains):
        return None
    if excluded_domains and any(root_domain.endswith(domain) for domain in excluded_domains):
        return None
    return absolute_url
#Function to get lang from html
def detect_language_from_html(soup):
    """Extracts the language from the <html lang="xx"> attribute."""
    html_tag = soup.find('html')
    if html_tag and html_tag.has_attr('lang'):
        return html_tag['lang'].split('-')[0]  # Extracts primary language (e.g., "en" from "en-US")
    return "unknown"

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
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', parsed_url.path.strip('/')) or 'index'

    file_path = os.path.join(base_dir, f"{filename}.txt")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Save content to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Saved: {file_path}")

# Web Crawler
def crawl(seed_urls, allowed_domains=None, excluded_domains=None, file_limit = 50):
    visited = set()
    to_visit = deque()
     #Clear CSV Before writing into it
    if os.path.exists('report.csv'):
        open('report.csv', 'w').close()
    for seed_url in seed_urls:
        extracted = tldextract.extract(urlparse(seed_url).netloc)
        domain = f"{extracted.domain}.{extracted.suffix}"
        if allowed_domains and domain not in allowed_domains:
            print(f"Skipping seed URL, not allowed: {seed_url}")
            continue
        if excluded_domains and domain in excluded_domains:
            print(f"Skipping seed URL (excluded): {seed_url}")
            continue
        to_visit.append(seed_url)

    while to_visit:
        current_url = to_visit.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        print(f"Crawling: {current_url}")
        
        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                extracted = tldextract.extract(current_url)
                subdomain = extracted.subdomain
                domain = f"{extracted.domain}.{extracted.suffix}"   
                #Use subdomain as language getter
                # if subdomain:
                #     language = subdomain
                # else:
                #     language = detect_language(response.text)
                #Use html lang to get language
                soup = BeautifulSoup(response.text, "html.parser")
                language = detect_language_from_html(soup)
                file_count = count_txt_files(f"{domain}/{language}")
                print("File count: ", file_count)
                if(file_count>=file_limit):
                    print(f"Hit file limit for {domain}/{language}")
                    continue
                base_dir = os.path.join(domain, language)
                save_page(current_url, response.text, base_dir)
                links = extract_links(current_url)
                outlink_count = len(links)
                write_to_csv(current_url, outlink_count)
                for link in links:
                    normalized_url = normalize_url(current_url, link, allowed_domains, excluded_domains)

                    # **Ensure every extracted link is added at least once**
                    if normalized_url and normalized_url not in visited and normalized_url not in to_visit:
                        to_visit.append(normalized_url)

        except requests.RequestException as e:
            print(f"Failed to fetch {current_url}: {e}")

# Example usage
seed_urls = [
    "https://www.cpp.edu/",  # Should be saved under `wikipedia.org/`
    "https://taobao.com/",         # Should be saved under `taobao.com/`
    "https://bbc.com/",            # Should be saved under `bbc.com/`
]

#doesnt check allowed domain for the frst parse

#use parsed_url.netloc to save to proper directory
allowed_domains = ["cpp.edu", "bbc.com"]  # Only crawl these
excluded_domains = ["taobao.com"]  # Ignore Taobao

crawl(seed_urls, allowed_domains=allowed_domains, excluded_domains=excluded_domains)
