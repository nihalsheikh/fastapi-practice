from fastapi import FastAPI, HTTPException, status
from bs4 import BeautifulSoup
import requests

app = FastAPI()

URL = "https://indianexpress.com"

@app.get("/news")
def get_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Fallback if no headlines/title found
    top_block_title = []

    for item in soup.find_all("a", class_="topblockNews__featuredLink"):
        top_block_title.append(item.text)

    sidebar_title = []
    for item in soup.find_all("a", class_="topblockNews__sidebarLink"):
        sidebar_title.append(item.text)

    return {
        "message": "Fetched news headlines",
        "Top Block Title": top_block_title[:2],
        "Sidebar Title": sidebar_title[:5]
    }

# Web Crawling without FastAPI
# from bs4 import BeautifulSoup
# import requests

# url = "https://indianexpress.com"

# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")

# print(soup.title.text)
