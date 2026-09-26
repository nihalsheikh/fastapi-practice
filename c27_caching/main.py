from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import time

app = FastAPI()

# Web Crawl
URL = "https://news.ycombinator.com"

cache_data = []

last_fetch = 0

@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    global cache_data, last_fetch
    start_time = time.time()

    if time.time() - last_fetch > 60:
        print("Fetching Fresh Data")
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        cache_data = [
            item.text for item in soup.find_all("span", class_="titleline")
        ]

        last_fetch = time.time()
    else:
        print("Using cache data")

    end_time = time.time()

    time_taken = round(end_time - start_time, 4)
    print(f"Time Taken: {time_taken}")

    # Pagination Logic
    start = (page - 1) * limit
    end = start + limit

    return {
        "message": "News Fetched",
        "time_taken": time_taken,
        "page": page,
        "limit": limit,
        "total": len(cache_data),
        "news": cache_data[start:end]
    }
