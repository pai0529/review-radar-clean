from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

from youtube_service import collect_youtube_reviews
from reddit_service import collect_reddit_reviews
from dcard_service import collect_dcard_reviews
from tavily_service import search_web_reviews

import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI(
    title="Review Radar API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康檢查
@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# Debug
@app.get("/debug-version")
def debug_version():
    return {
        "version": "youtube-reddit-dcard-api-no-google",
        "analyze_type": "json_body"
    }

# Request Model
class ReviewRequest(BaseModel):
    product_name: str
    reviews: List[str]
    youtube_url: str = ""

# 分析 API
@app.post("/analyze")
def analyze_reviews(data: ReviewRequest):

    print("analyze endpoint hit")
    print(data)

    # =========================
    # YouTube
    # =========================
    youtube_data = collect_youtube_reviews(
        data.product_name,
        max_videos=3,
        comments_per_video=20
    )

    youtube_comments = youtube_data["comments"]

    youtube_texts = [
        comment["text"]
        for comment in youtube_comments
    ]

    print("youtube comments:", len(youtube_comments))

    # =========================
    # Reddit
    # =========================
    reddit_data = collect_reddit_reviews(
        data.product_name,
        limit=5
    )

    reddit_comments = reddit_data["comments"]

    reddit_texts = [
        comment["text"]
        for comment in reddit_comments
    ]

    print("reddit comments:", len(reddit_comments))

    # =========================
    # Dcard
    # =========================
    dcard_data = collect_dcard_reviews(
        data.product_name,
        limit=5
    )

    dcard_comments = dcard_data["comments"]

    dcard_texts = [
        comment["text"]
        for comment in dcard_comments
    ]

    print("dcard comments:", len(dcard_comments))
     # =========================
    # Tavily Search
    # =========================
    tavily_results = search_web_reviews(
        data.product_name
    )

    tavily_texts = [
        f"{item['title']}：{item['content']}"
        for item in tavily_results
    ]

    print("tavily results:", len(tavily_results))

    # =========================
    # 合併所有評論
    # =========================
    all_reviews = (
        data.reviews
        + youtube_texts
        + reddit_texts
        + dcard_texts
        + tavily_texts
    )

    reviews_text = "\n".join(all_reviews)

    # =========================
    # AI Prompt
    # =========================
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

    # =========================
    # OpenAI 分析
    # =========================
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

    # =========================
    # JSON 解析
    # =========================
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

    # =========================
    # 回傳結果
    # =========================
    return {
        "product_name": data.product_name,

        "manual_reviews_count": len(data.reviews),

        "youtube_comments_count": len(youtube_comments),
        "youtube_videos": youtube_data["videos"],

        "reddit_comments_count": len(reddit_comments),
        "reddit_posts": reddit_data["posts"],

        "dcard_comments_count": len(dcard_comments),
        "dcard_posts": dcard_data["posts"],

        "tavily_results_count": len(tavily_results),
        "tavily_results": tavily_results,
        "analysis": analysis

    }