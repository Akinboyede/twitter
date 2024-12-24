import requests
import csv
import datetime
import time
from pathlib import Path

# API Keys
NEWS_API_KEY = 'f365b7cc45294a91a1f2b4e39c72884d'
XAI_API_KEY = "xai-FMxq2gD0kACm8ES13rZamX7ipjFVzc4vKoLhn4Sya8dTLzt0RJoWV1yM9A2RKCbEBGdNve0pg0nHxW5o"

# Path to the CSV file to save content
CONTENT_FILE_PATH = Path("content_log.csv")

# Function to fetch today's news articles
# Function to fetch today's news articles with a query parameter
# Function to fetch trending news from a specific source to ensure results

def fetch_trending_news():
    

    query = "news"
    source = "cnn ,the-new-york-times , espn , bbc-sport  , entertainment-weekly , buzzfeed"  # Example source; replace with another if preferred
    url = f"https://newsapi.org/v2/everything?q={query}&sources={source}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if articles:
            return articles[:5]  # Fetching multiple articles
        else:
            print("No articles found.")
            return []
    else:
        print("Error fetching news:", response.status_code)
        print("Response content:", response.content)
        return []



# Function to create a post with X.AI's API
def create_social_media_post_with_xai(article_description):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an assistant that creates engaging social media posts."},
            {"role": "user", "content": f"Create a short and engaging Twitter post based on this news: {article_description}"}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('choices')[0]['message']['content']
    else:
        print("Error creating post with X.AI:", response.status_code, response.text)
        return None
def get_random_fun_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    if response.status_code == 200:
        fact = response.json().get('text', 'No fun fact available at the moment.')
        return fact
    else:
        return "Error fetching fun fact."


# Function to save content to a CSV file
def save_to_csv(content_type, content):
    with open(CONTENT_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), content_type, content])
    print(f"Content saved to {CONTENT_FILE_PATH}")

# Main function to automatically generate news and save posts
def run_bot():
    while True:
        fun_fact = get_random_fun_fact()
        save_to_csv("Fun Fact", fun_fact)

        articles = fetch_trending_news()
        for article in articles:
            description = article.get('description', 'No description available')
            url = article.get('url', '')
            if description:
                post = create_social_media_post_with_xai(description)
                if post:
                    post_with_url = f"{post} - Read more: {url}"
                    save_to_csv("News Post", post_with_url)
        
        time.sleep(1800)  # Wait 10 minutes before generating again

# Create the CSV file with headers if it doesn’t exist
if not CONTENT_FILE_PATH.exists():
    with open(CONTENT_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Content Type", "Content"])

# Run the bot
if __name__ == "__main__":
    run_bot()
