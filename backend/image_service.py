import os
import requests

HEADERS = {"User-Agent": "PulsePick/1.0 (https://github.com/pai0529/review-radar-clean)"}
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def get_serper_image(product_name: str, mode: str = "product") -> str:
    """用 Serper.dev Google Image Search 取得產品圖片
    mode: 'product'（預設）或 'logo'（品牌/餐廳）
    """
    if not SERPER_API_KEY:
        return ""
    q = f"{product_name} logo" if mode == "logo" else product_name
    try:
        resp = requests.post(
            "https://google.serper.dev/images",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": q, "num": 5},
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


def get_best_image(product_name: str, tavily_image_url: str, mode: str = "product") -> dict:
    """
    圖片優先順序：
    1. Serper logo 搜尋（餐廳品牌）
    2. Serper product 搜尋（logo 找不到時的餐廳 fallback，或一般產品）
    3. Wikipedia
    4. Tavily
    5. 空字串（前端顯示文字 fallback）
    """
    serper_img = get_serper_image(product_name, mode=mode)
    if serper_img:
        return {"image_url": serper_img, "image_type": "product"}

    # 餐廳 logo 找不到 → 改搜食物照
    if mode == "logo":
        serper_img = get_serper_image(product_name, mode="product")
        if serper_img:
            return {"image_url": serper_img, "image_type": "product"}

    wiki_img = get_wikipedia_image(product_name)
    if wiki_img:
        return {"image_url": wiki_img, "image_type": "product"}

    if tavily_image_url:
        return {"image_url": tavily_image_url, "image_type": "product"}

    return {"image_url": "", "image_type": "fallback"}
