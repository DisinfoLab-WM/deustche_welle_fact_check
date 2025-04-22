import feedparser
import json
import time  # Import the time module
import re  # Importing regex for HTML parsing
# Press One RSS Feed URL
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
    author = entry.author
    if "leighpressoneph" in author:
        author = ""
    # Extract full text from content or description
    full_text = entry.content[0].value if 'content' in entry else entry.description
    full_text = remove_html_tags(full_text)  # Clean HTML tags
    # Cut off at 'PressOne.PH' if it exists
    cutoff_point = full_text.find("PressOne.PH")
    if cutoff_point != -1:
        full_text = full_text[:cutoff_point]
    dfs = entry.published_parsed
    date_published = f'{dfs[0]}-{"{:02d}".format(dfs[1])}-{"{:02d}".format(dfs[2])} {"{:02d}".format(dfs[3])}:{"{:02d}".format(dfs[4])}:{"{:02d}".format(dfs[5])}'
    articles["articles"][str(index)] = {
        "title": entry.title,
        "text": full_text.strip(),  # Use full text if available and strip whitespace
        "author": author,  # Use 'Unknown' if creator is not available
        "date_published": date_published,
        "unix_date_published": time.mktime(entry.published_parsed) if entry.published_parsed else None,  # Corrected to use time.mktime
        "organization_country": "Philippines",  
        "site_name": "Press One",
        "url": entry.link,
        "language": "en",  
    }
# Save articles to a local JSON file
with open("Press_One.json", "w", encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)
print("Articles saved locally in Press_One.json!")
