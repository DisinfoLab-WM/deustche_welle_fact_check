import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pytz
import os

# Set up Selenium WebDriver with Chrome
options = Options()
options.add_argument("--headless")  # Uncomment for headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Initialize WebDriver wait
wait = WebDriverWait(driver, 1)

# URL of the DW Fact Check section
section_url = "https://www.dw.com/en/fact-check/t-56584214"

# Step 1: Load the page
driver.get(section_url)

# Step 2: Click "Show more" until no more button is found
while True:
    try:
        # Wait for the 'Show more' button to be clickable and click it
        show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(text(), 'Show more')]")))
        show_more_button.click()
        time.sleep(2)  # Wait for new articles to load
    except (TimeoutException, NoSuchElementException):
        print("No more 'Show more' button found.")
        break

# Step 3: Extract article links from the page
soup = BeautifulSoup(driver.page_source, "html.parser")
article_links = []

# Define a list of keywords for non-article content
non_article_keywords = [
    "how-to-reach-dw-fact-check",
    "accessibility-statement",
    "legal-notice",
    "meet-the-team",
    "how-dw-fact-checks-fake-news"
    # "dossier-team-dw-fact-check",
    # "european-union-general-data-protection-regulation-gdpr-valid-may-25-2018"
]

non_article_links = [
    "https://www.dw.com/en/dossier-team-dw-fact-check/a-66713297",
    "https://www.dw.com/en/european-union-general-data-protection-regulation-gdpr-valid-may-25-2018/a-63500655",
    "https://www.dw.com/en/how-to-spot-fake-news-propaganda-deepfakes-disinformation-bots-or-ai-fakes-with-fact-checking/a-67738458"
]

# Find all article links in the central cluster
for a_tag in soup.find_all("a", href=True):
    href = a_tag['href']
    # Filter for article links in the format '/en/slug/a-<digits>'
    if re.match(r'^/en/[^/]+/a-\d+$', href):
        # Exclude non-article content based on keywords
        if not any(keyword in href for keyword in non_article_keywords):
            full_url = "https://www.dw.com" + href
            if full_url not in article_links:
                if full_url not in non_article_links:
                    # print(full_url)
                    article_links.append(full_url)

if len(article_links) < 31:
    print(len("not enough article links found, trying again"))
    os.system("python3 main.py")
    

print(f"Found {len(article_links)} articles.")

# Step 4: Create a list to store articles
articles_data = []

# Step 5: Visit each article, extract title, author, date, and save it
for idx, link in enumerate(article_links, start=1):
    driver.get(link)

    article_soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Extract title
    title_tag = article_soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No title"

    # Extract authors
    authors = []
    author_tags = article_soup.find_all("a", class_=lambda class_name: class_name and "author" in class_name)
    for tag in author_tags:
        author_name = tag.get_text(strip=True)
        if author_name:  # Ensure non-empty author names
            if author_name not in authors:
                authors.append(author_name)

    # Remove any empty strings or whitespace-only entries
    authors = [author.strip() for author in authors if author.strip()]

    # Extract publication date
    time_tag = article_soup.find("time", {"aria-hidden": "true"})
    date_published = time_tag.get_text(strip=True) if time_tag else "Unknown"
    # Convert publication date to Unix timestamp and reformat to "YYYY-MM-DD"
    if date_published != "Unknown":
        try:
            # Parse the date using the current format
            date_obj = datetime.strptime(date_published, "%m/%d/%Y")
            # Format the date to "YYYY-MM-DD"
            date_published = date_obj.strftime("%Y-%m-%d")
            unix_date_published = int(date_obj.timestamp())
        except ValueError:
            date_published = "Unknown"
            unix_date_published = None
    else:
        unix_date_published = None

    # Site details
    site_location = "Germany"  # DW is a German news outlet
    site_name = "Deutsche Welle"

    # Extract article paragraphs
    paragraphs = article_soup.select("section div p")
    article_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)

    # Append article data to the list
    articles_data.append({
        "text": article_text,
        "title": title,
        "authors": authors,
        "date_published": date_published,
        "unix_date_published": unix_date_published,
        "site_location": site_location,
        "site_name": site_name,
        "url": link
    })

    print(f"Processed article: {title}")

# Step 6: Save articles data to a JSON file
with open("articles_data.json", "w", encoding="utf-8") as json_file:
    json.dump(articles_data, json_file, indent=4, ensure_ascii=False)

# Close the WebDriver
driver.quit()