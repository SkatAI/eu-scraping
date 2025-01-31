'''
takes the last day of available verbatim
TOC for current verbatim reports for the day

for each page
- extracts the url in the previous link
- extracts all the links in the page
'''

import requests
import re
import pandas as pd
import time


# Function to extract the date from the URL
def extract_date_from_url(url):
    match = re.search(r'CRE-\d{1,2}-(\d{4}-\d{2}-\d{2})', url)
    return match.group(1) if match else None

# Function to process a page and extract "Previous" URL and all .html links
def process_page(url):
    full_url = BASE_URL + url

    # Send a GET request to the page
    response = requests.get(full_url)
    if response.status_code != 200:
        print(f"Failed to load page: {full_url}")
        return None, []

    # Get the page content
    content = response.text

    # Extract "Previous" link
    previous_match = re.search(r'<a href="([^"]+)" title="Previous">Previous</a>', content)
    previous_url = previous_match.group(1) if previous_match else None

    # Extract all .html links
    links = re.findall(r'<a href="([^"]+\.html)"', content)
    return previous_url, links


if __name__ == "__main__":

    _iter = 1
    BASE_URL = "https://www.europarl.europa.eu"
    data = []

    # Initial URL
    # most recent available verbatims TOC
    start_url = "/doceo/document/CRE-10-2024-11-27-TOC_EN.html"
    current_url = start_url
    url_date = extract_date_from_url(current_url)


    while url_date > '2024-01-01':
        output_file = f"./data/tmp/extracted_links_{str(_iter).zfill(3)}.csv"
        # Extract the date from the current URL

        url_date = extract_date_from_url(current_url)

        previous_url, links = process_page(current_url)

        print(_iter, url_date, len(links), current_url)

        # Append links with their date to the data list
        if url_date:
            for link in links:
                data.append({
                    "page": current_url,
                    "date": url_date,
                    "url": link
                })

        # Update the URL to the "Previous" link
        current_url = previous_url

        # Respectful delay
        _iter += 1
        time.sleep(2)

        # Save the data to a CSV file
        df = pd.DataFrame(data)
        df.drop_duplicates(inplace = True)
        df.to_csv(output_file, index = False)

        print(f"{df.shape[0]} links")

