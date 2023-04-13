import json
import os
from bs4 import BeautifulSoup

input_dir = './data/raw/documentation/'
output_file = './data/preprocessed/documentation/documentation.json'

# Get a list of all HTML files in the input directory
html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]

json_data_list = []

for html_file_name in html_files:
    html_file_path = os.path.join(input_dir, html_file_name)

    # Read the HTML content
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the title
    title = soup.title.string if soup.title else 'Untitled'

    # Find the devsite-content container
    devsite_content = soup.find('devsite-content')

    if devsite_content:
        # Extract the relevant content within the devsite-content container
        text_parts = []
        for tag in devsite_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text_parts.append(tag.get_text(strip=True))

        content = ' '.join(text_parts)
    else:
        content = ''

    # Write a summary
    # This example simply takes the first 200 characters of the content
    summary = content[:200] + ('...' if len(content) > 200 else '')

    # Create a JSON object
    json_data = {
        'title': title,
        'content': content
    }
    
    json_data_list.append(json_data)

# Save the JSON data to a file
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_data_list, json_file, ensure_ascii=False, indent=4)
