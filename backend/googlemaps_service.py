import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def collect_googlemaps_reviews(place_name: str) -> dict:
    """用 Google Places API (New) 抓餐廳評論（只在有 API key 時啟用）"""
    comments = []

    if not GOOGLE_MAPS_API_KEY:
        return {"comments": comments}

    try:
        # Step 1: 用 Text Search 找地點
        search_resp = requests.post(
            "https://places.googleapis.com/v1/places:searchText",
            headers={
                "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
                "X-Goog-FieldMask": "places.id,places.displayName",
                "Content-Type": "application/json",
            },
            json={"textQuery": place_name, "languageCode": "zh-TW"},
            timeout=8,
        )

        if search_resp.status_code != 200:
            print("Google Maps search error:", search_resp.status_code, search_resp.text[:200])
            return {"comments": comments}

        places = search_resp.json().get("places", [])
        if not places:
            return {"comments": comments}

        place_id = places[0]["id"]

        # Step 2: 取得評論
        detail_resp = requests.get(
            f"https://places.googleapis.com/v1/places/{place_id}",
            headers={
                "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
                "X-Goog-FieldMask": "reviews,rating",
            },
            params={"languageCode": "zh-TW"},
            timeout=8,
        )

        if detail_resp.status_code != 200:
            print("Google Maps detail error:", detail_resp.status_code)
            return {"comments": comments}

        data = detail_resp.json()
        reviews = data.get("reviews", [])

        for review in reviews:
            text = review.get("text", {}).get("text", "").strip()
            rating = review.get("rating", "")
            if text:
                comments.append({
                    "text": f"[評分 {rating}/5] {text}",
                    "source": "Google Maps",
                })

        print(f"Google Maps reviews for {place_name}: {len(comments)}")

    except Exception as e:
        print("Google Maps error:", e)

    return {"comments": comments}
