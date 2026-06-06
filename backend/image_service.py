import os
import requests

HEADERS = {"User-Agent": "PulsePick/1.0 (https://github.com/pai0529/review-radar-clean)"}
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def get_serper_image(product_name: str) -> str:
    """用 Serper.dev Google Image Search 取得產品圖片"""
    if not SERPER_API_KEY:
        return ""
    try:
        resp = requests.post(
            "https://google.serper.dev/images",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": f"{product_name} official product", "num": 5},
            timeout=8,
        )
        if resp.status_code == 200:
            images = resp.json().get("images", [])
            for item in images:
                url = item.get("imageUrl", "")
                if url:
                    return url
    except Exception as e:
        print(f"Serper image error ({product_name}):", e)
    return ""


def get_wikipedia_image(product_name: str) -> str:
    """從 Wikipedia 取得代表圖片，先試英文再試中文"""
    for base_url in [
        "https://en.wikipedia.org/api/rest_v1/page/summary/",
        "https://zh.wikipedia.org/api/rest_v1/page/summary/",
    ]:
        try:
            resp = requests.get(
                base_url + requests.utils.quote(product_name),
                headers=HEADERS,
                timeout=6,
            )
            if resp.status_code == 200:
                data = resp.json()
                img = (
                    data.get("originalimage", {}).get("source")
                    or data.get("thumbnail", {}).get("source")
                    or ""
                )
                # 跳過 SVG（通常是線稿或 logo）
                if img and not img.lower().endswith(".svg"):
                    return img
        except Exception as e:
            print(f"Wikipedia image error ({product_name}):", e)
    return ""


def get_best_image(product_name: str, tavily_image_url: str) -> dict:
    """
    圖片優先順序：
    1. Serper Google Image Search（準確、有 key 才啟用）
    2. Wikipedia（免費、但品質不穩）
    3. Tavily（最後手段）
    4. 空字串（前端顯示文字 fallback）
    """
    serper_img = get_serper_image(product_name)
    if serper_img:
        return {"image_url": serper_img, "image_type": "product"}

    wiki_img = get_wikipedia_image(product_name)
    if wiki_img:
        return {"image_url": wiki_img, "image_type": "product"}

    if tavily_image_url:
        return {"image_url": tavily_image_url, "image_type": "product"}

    return {"image_url": "", "image_type": "fallback"}
