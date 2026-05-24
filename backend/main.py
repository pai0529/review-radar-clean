from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from youtube_service import collect_youtube_reviews
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewRequest(BaseModel):
    product_name: str
    reviews: List[str]
    youtube_url: str = ""

@app.post("/analyze")
def analyze_reviews(data: ReviewRequest):
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

    all_reviews = data.reviews + youtube_texts

    reviews_text = "\n".join(all_reviews)

    prompt = f"""
你是一個專業商品與 App 評論分析 AI。

商品名稱：
{data.product_name}

以下是使用者評論與 YouTube 多部影片留言：
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
        response_format={"type": "json_object"}
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

    return {
        "product_name": data.product_name,
        "manual_reviews_count": len(data.reviews),
        "youtube_comments_count": len(youtube_comments),
        "youtube_videos": youtube_data["videos"],
        "analysis": analysis
    }