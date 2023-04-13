import os
import requests
from bs4 import BeautifulSoup
import shutil
import re

def sanitize_title(title):
    # Replace invalid characters and newline characters with underscores
    sanitized_title = re.sub(r'[<>:"/\\|?*\n]', "_", title)
    return sanitized_title

def save_page(url, output_dir):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title_element = soup.find("h1", class_="title")

    # Check for alternative title elements
    if not title_element:
        title_element = soup.find("h1", class_="document-title")

    if not title_element:
        title_element = soup.find("h1", class_="devsite-page-title")

    if title_element:
        title = sanitize_title(title_element.text.strip().replace(" ", "_"))
    else:
        print(f"Skipping page: {url}")
        return

    filename = os.path.join(output_dir, f"{title}.html")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Saved page: {filename}")



def main():
    base_url = "https://cloud.google.com/looker/docs/intro"
    output_dir = "data/raw/documentation"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.select("a.devsite-nav-title, a.devsite-nav-item")
    hrefs = [link["href"] for link in links]

    save_page(base_url, output_dir)  # Save the main intro page

    for href in hrefs:
        if href.startswith("http"):
            url = href
        else:
            url = f"https://cloud.google.com{href}"
        save_page(url, output_dir)


if __name__ == "__main__":
    main()