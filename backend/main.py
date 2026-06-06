from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote

from youtube_service import collect_youtube_reviews
from reddit_service import collect_reddit_reviews
from dcard_service import collect_dcard_reviews
from tavily_service import search_web_reviews
from image_service import get_best_image, get_wikipedia_image

import os
import json
import redis as redis_lib

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="PulsePick API")

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis_lib.from_url(REDIS_URL) if REDIS_URL else None

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

def cache_get(slug: str):
    if redis_client:
        data = redis_client.get(f"pulsepick:{slug}")
        return json.loads(data) if data else None
    # fallback: 本地檔案
    cache_file = CACHE_DIR / f"{slug}.json"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def cache_set(slug: str, result: dict):
    if redis_client:
        redis_client.set(f"pulsepick:{slug}", json.dumps(result, ensure_ascii=False))
    else:
        # fallback: 本地檔案
        cache_file = CACHE_DIR / f"{slug}.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug-version")
def debug_version():
    return {
        "version": "pulsepick-product-image-type-v1",
        "analyze_type": "json_body"
    }

def get_brand_image(product_name: str):
    name = product_name.lower()

    # 只有大型 app / 軟體 / 社群服務才用 Google favicon（這些網域一定有高品質 favicon）
    # 餐廳、實體品牌交給 Tavily 搜食物/產品照，效果更好
    app_brands = {
        # AI / 工具
        "chatgpt": "openai.com",
        "openai": "openai.com",
        "claude": "anthropic.com",
        "gemini": "gemini.google.com",
        "notion": "notion.so",
        "cursor": "cursor.com",
        # 社群 / 娛樂 app
        "tiktok": "tiktok.com",
        "instagram": "instagram.com",
        "discord": "discord.com",
        "spotify": "spotify.com",
        "netflix": "netflix.com",
        "youtube": "youtube.com",
        "twitter": "twitter.com",
        "facebook": "facebook.com",
        "line": "line.me",
        "threads": "threads.net",
        "reddit": "reddit.com",
        "twitch": "twitch.tv",
        "linkedin": "linkedin.com",
    }

    for key, domain in app_brands.items():
        if key in name:
            return {
                "image_url": f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{domain}&size=256",
                "image_type": "app_logo",  # 這個 type 不會被 Tavily 覆蓋
            }

    return {
        "image_url": (
            "https://ui-avatars.com/api/"
            f"?name={quote(product_name)}"
            "&background=111827"
            "&color=ffffff"
            "&size=512"
        ),
        "image_type": "fallback"
    }

class ReviewRequest(BaseModel):
    product_name: str
    reviews: List[str]
    youtube_url: str = ""

@app.post("/analyze")
def analyze_reviews(data: ReviewRequest):
    print("analyze endpoint hit")
    print(data)

    slug = data.product_name.lower().replace(" ", "-")

    cached_data = cache_get(slug)
    if cached_data:
        print("cache hit:", slug)
        cached_data["cached"] = True
        return cached_data

    print("cache miss:", slug)

    # app 品牌（社群/工具類）直接用 Google favicon，不需要搜尋
    brand_data = get_brand_image(data.product_name)
    is_app_brand = brand_data["image_type"] == "app_logo"

    youtube_data = collect_youtube_reviews(
        data.product_name,
        max_videos=3,
        comments_per_video=20
    )

    youtube_comments = youtube_data["comments"]
    youtube_texts = [comment["text"] for comment in youtube_comments]

    print("youtube comments:", len(youtube_comments))

    reddit_data = collect_reddit_reviews(
        data.product_name,
        limit=5
    )

    reddit_comments = reddit_data["comments"]
    reddit_texts = [comment["text"] for comment in reddit_comments]

    print("reddit comments:", len(reddit_comments))

    dcard_data = collect_dcard_reviews(
        data.product_name,
        limit=5
    )

    dcard_comments = dcard_data["comments"]
    dcard_texts = [comment["text"] for comment in dcard_comments]

    print("dcard comments:", len(dcard_comments))

    tavily_data = search_web_reviews(data.product_name)
    tavily_results = tavily_data["results"] if isinstance(tavily_data, dict) else tavily_data
    tavily_image_url = tavily_data.get("image_url", "") if isinstance(tavily_data, dict) else ""

    tavily_texts = [
        f"{item['title']}：{item['content']}"
        for item in tavily_results
    ]

    # 餐廳品牌清單 → 搜 logo 而非食物照
    restaurant_keywords = [
        "kfc", "肯德基", "mcdonald", "麥當勞", "burger king", "漢堡王",
        "starbucks", "星巴克", "din tai fung", "鼎泰豐",
        "haidilao", "海底撈", "kura", "藏壽司",
    ]
    name_lower = data.product_name.lower()
    is_restaurant = any(k in name_lower for k in restaurant_keywords)

    # app 品牌用 Google favicon，餐廳搜 logo，其他搜產品圖
    if is_app_brand:
        image_url = brand_data["image_url"]
        image_type = "app_logo"
    else:
        mode = "logo" if is_restaurant else "product"
        img_result = get_best_image(data.product_name, tavily_image_url, mode=mode)
        image_url = img_result["image_url"]
        image_type = img_result["image_type"]

    print("tavily results:", len(tavily_results))
    print("image url:", image_url)
    print("image type:", image_type)

    all_reviews = (
        data.reviews
        + youtube_texts
        + reddit_texts
        + dcard_texts
        + tavily_texts
    )

    reviews_text = "\n".join(all_reviews)

    prompt = f"""
你是一個專業商品與 App 評論分析 AI。

商品名稱：
{data.product_name}

以下是來自多平台的使用者評論：

{reviews_text}

請只回傳 JSON，不要加任何說明文字。

JSON 格式如下：
{{
  "score": 8.5,
  "summary": "一句話總結這個商品或 App 的整體評價",
  "pros": ["優點1", "優點2", "優點3"],
  "cons": ["缺點1", "缺點2", "缺點3"],
  "target_users": ["適合族群1", "適合族群2"],
  "not_target_users": ["不適合族群1", "不適合族群2"],
  "suggestion": "購買或使用建議",
  "confidence": "高 / 中 / 低"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    content = response.choices[0].message.content

    try:
        analysis = json.loads(content)

    except Exception:
        analysis = {
            "score": 0,
            "summary": "AI 回傳格式解析失敗",
            "pros": [],
            "cons": [],
            "target_users": [],
            "not_target_users": [],
            "suggestion": content,
            "confidence": "低"
        }

    result = {
        "product_name": data.product_name,
        "image_url": image_url,
        "image_type": image_type,

        "manual_reviews_count": len(data.reviews),

        "youtube_comments_count": len(youtube_comments),
        "youtube_videos": youtube_data["videos"],

        "reddit_comments_count": len(reddit_comments),
        "reddit_posts": reddit_data["posts"],

        "dcard_comments_count": len(dcard_comments),
        "dcard_posts": dcard_data["posts"],

        "tavily_results_count": len(tavily_results),
        "tavily_results": tavily_results,

        "analysis": analysis,
        "cached": False
    }

    cache_set(slug, result)

    return result