import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search_web_reviews(product_name):
    queries = [
        f"{product_name} 評價 心得 優缺點",
        f"{product_name} PTT Dcard Mobile01 評價",
        f"{product_name} review pros cons",
    ]

    all_results = []
    image_url = ""

    for query in queries:
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5,
                    "include_images": True,
                },
                timeout=15,
            )

            if response.status_code != 200:
                print("Tavily failed:", response.status_code, response.text[:200])
                continue

            data = response.json()

            if not image_url:
                images = data.get("images", [])
                if images:
                    image_url = images[0]

            for item in data.get("results", []):
                all_results.append({
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "url": item.get("url", ""),
                    "query": query,
                })

        except Exception as e:
            print("Tavily error:", e)

    return {
        "results": all_results,
        "image_url": image_url
    }