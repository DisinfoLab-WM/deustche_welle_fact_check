import feedparser
import json
import time  # Import the time module
import re  # Importing regex for HTML parsing
# Rappler RSS Feed URL
rss_url = "https://pressone.ph/feed/"
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
    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": entry.get("author", ""),  # Use 'Unknown' if creator is not available
        "date_published": entry.published,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,  # Corrected to use time.mktime
        "organization_country": "Philippines",  # Assuming the organization is based in the Philippines
        "site_name": "Rappler",
        "url": entry.link,
        "language": "en",  # Assuming English for all articles
    }
# Save articles to a local JSON file
with open("Rappler.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)
print("Articles saved locally in Rappler.json!")
