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

    image_query = f"{product_name} official product image"

    all_results = []
    image_url = ""

    # 先搜尋商品圖片
    try:
        image_response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": image_query,
                "search_depth": "basic",
                "max_results": 3,
                "include_images": True,
            },
            timeout=15,
        )

        if image_response.status_code == 200:
            image_data = image_response.json()
            images = image_data.get("images", [])

            if images:
                image_url = images[0]

    except Exception as e:
        print("Tavily image error:", e)

    # 再搜尋評論資料
    for query in queries:
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5,
                    "include_images": False,
                },
                timeout=15,
            )

            if response.status_code != 200:
                print("Tavily failed:", response.status_code, response.text[:200])
                continue

            data = response.json()

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