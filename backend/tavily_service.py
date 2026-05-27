import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_web_reviews(product_name):

    queries = [
        f"{product_name} 評價 site:dcard.tw",
        f"{product_name} 心得 site:ptt.cc",
        f"{product_name} review site:reddit.com",
        f"{product_name} 評測 site:mobile01.com"
    ]

    all_results = []

    for query in queries:

        try:

            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5
                },
                timeout=15
            )

            if response.status_code != 200:
                print("Tavily failed:", response.status_code)
                continue

            data = response.json()

            results = data.get("results", [])

            for item in results:

                all_results.append({
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "url": item.get("url", ""),
                    "query": query
                })

        except Exception as e:
            print("Tavily error:", e)

    return all_results