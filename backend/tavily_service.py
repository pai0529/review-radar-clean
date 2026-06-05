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

    # 用多個查詢提高找到正確圖片的機率
    image_queries = [
        f"{product_name} official product photo",
        f"{product_name} cover art",
    ]

    # 過濾掉廣告、icon、小圖等不合適的圖片
    BAD_URL_PATTERNS = [
        "favicon", "icon", "logo", "avatar", "thumb",
        "ads", "banner", "sponsor", "tracking",
        ".gif", "pixel", "1x1",
    ]

    def is_good_image(url: str) -> bool:
        url_lower = url.lower()
        if any(p in url_lower for p in BAD_URL_PATTERNS):
            return False
        # 只接受常見圖片格式或 CDN URL
        return any(ext in url_lower for ext in [".jpg", ".jpeg", ".png", ".webp", "images", "img", "media", "photo"])

    all_results = []
    image_url = ""

    # 搜尋商品圖片
    for image_query in image_queries:
        if image_url:
            break
        try:
            image_response = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": image_query,
                    "search_depth": "basic",
                    "max_results": 5,
                    "include_images": True,
                },
                timeout=15,
            )

            if image_response.status_code == 200:
                image_data = image_response.json()
                images = image_data.get("images", [])
                good_images = [img for img in images if is_good_image(img)]
                if good_images:
                    image_url = good_images[0]
                elif images:
                    image_url = images[0]  # fallback 到第一張

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