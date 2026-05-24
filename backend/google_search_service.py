import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX")

def google_search_reviews(product_name, max_results=5):
    results = []

    queries = [
        f"{product_name} 評價 site:dcard.tw",
        f"{product_name} 心得 site:ptt.cc",
        f"{product_name} review site:reddit.com",
        f"{product_name} 評測 site:mobile01.com",
    ]

    for query in queries:
        try:
            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "key": GOOGLE_SEARCH_API_KEY,
                    "cx": GOOGLE_SEARCH_CX,
                    "q": query,
                    "num": max_results,
                },
                timeout=10,
            )

            if response.status_code != 200:
                print("Google search failed:", response.status_code, response.text[:300])
                continue

            data = response.json()

            for item in data.get("items", []):
                results.append({
                    "source": "Google Search",
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", ""),
                    "query": query,
                })

        except Exception as e:
            print("Google search error:", e)

    return results