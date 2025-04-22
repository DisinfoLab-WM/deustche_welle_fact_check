import feedparser
import json
import time  # Import the time module
import re  # Importing regex for HTML parsing
# Verificat RSS Feed URL
rss_url = "https://www.verificat.cat/feed/"
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
    author = entry.author
    if "redaccio" in author:
        author = ""
    dfs = entry.published_parsed
    date_published = f'{dfs[0]}-{"{:02d}".format(dfs[1])}-{"{:02d}".format(dfs[2])} {"{:02d}".format(dfs[3])}:{"{:02d}".format(dfs[4])}:{"{:02d}".format(dfs[5])}'
    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": author,  # Use 'Unknown' if creator is not available
        "date_published": date_published,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,  # Corrected to use time.mktime
        "organization_country": "Spain",  
        "site_name": "verificat",
        "url": entry.link,
        "language": "ca",  
    }
# Save articles to a local JSON file
with open("Verificat.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)
print("Articles saved locally in Verificat.json!")