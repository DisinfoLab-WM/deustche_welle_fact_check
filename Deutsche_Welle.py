import feedparser
import json
import time  # Import the time module
import re  # Importing regex for HTML parsing
import requests
import xml.etree.ElementTree as ET

# DW RSS Feed URL
rss_url = "https://rss.dw.com/rdf/rss-en-all"
# Parse RSS Feed
feed = feedparser.parse(rss_url)

# Initialize the articles dictionary
articles = {"articles": {}}
# Function to remove HTML tags from text
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
# Loop through RSS entries and store in the dictionary
for index, entry in enumerate(feed.entries):
    # Extract full text from content or description
    full_text = entry.content[0].value if 'content' in entry else entry.description
    full_text = remove_html_tags(full_text)  # Clean HTML tags
    dfs = entry.get("dc:date", "")
    # dfs =  entry.get("published")
    date_published = dfs
    # date_published = f'{dfs[0]}-{"{:02d}".format(dfs[1])}-{"{:02d}".format(dfs[2])} {"{:02d}".format(dfs[3])}:{"{:02d}".format(dfs[4])}:{"{:02d}".format(dfs[5])}'
    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": "",#entry.author,  # Use 'Unknown' if creator is not available
        "date_published": date_published,
        "unix_date_published": time.mktime(date_published) if date_published else None,  # Corrected to use time.mktime
        "organization_country": "Germany", 
        "site_name": "Deutsche_Welle",
        "url": entry.link,
        "language": "en",  
    }
# Save articles to a local JSON file
with open("DW.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)
print("Articles saved locally in DW.json!")
