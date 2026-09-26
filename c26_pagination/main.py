from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

URL = "https://news.ycombinator.com"

app = FastAPI()

news = []

# Web Crawl
@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.find_all("span", class_="titleline"):
        news.append(item.text)

    # Pagination Logic
    start = (page - 1) * limit
    end = start + limit

    return {
        "message":"Fetched news from YCombinator",
        "page": page,
        "limit": limit,
        "total_news": len(news),
        "news": news[start:end] # python slice method is inclusive of start but not end value
    }
