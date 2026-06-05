import requests

HEADERS = {"User-Agent": "PulsePick/1.0 (https://github.com/pai0529/review-radar-clean)"}


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
                # 優先用 originalimage（高解析度），其次 thumbnail
                img = (
                    data.get("originalimage", {}).get("source")
                    or data.get("thumbnail", {}).get("source")
                    or ""
                )
                if img:
                    return img
        except Exception as e:
            print(f"Wikipedia image error ({product_name}):", e)

    return ""


def get_best_image(product_name: str, tavily_image_url: str) -> dict:
    """
    圖片優先順序：
    1. Wikipedia（準確、免費）
    2. Tavily（不穩定，但可用）
    3. 空字串（交給前端 fallback）
    """
    wiki_img = get_wikipedia_image(product_name)
    if wiki_img:
        return {"image_url": wiki_img, "image_type": "product"}

    if tavily_image_url:
        return {"image_url": tavily_image_url, "image_type": "product"}

    return {"image_url": "", "image_type": "fallback"}
