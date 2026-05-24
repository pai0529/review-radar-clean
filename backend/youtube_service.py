from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

youtube = build(
    "youtube",
    "v3",
    developerKey=os.getenv("YOUTUBE_API_KEY")
)

def search_youtube_videos(query, max_results=3):
    videos = []

    try:
        request = youtube.search().list(
            part="snippet",
            q=f"{query} review 評測 開箱",
            type="video",
            maxResults=max_results,
            order="relevance"
        )

        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]

            videos.append({
                "video_id": video_id,
                "title": title,
                "channel": channel,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

    except Exception as e:
        print("YouTube search error:", e)
        return []

    return videos


def get_video_comments(video_id, max_comments=20):
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText"
        )

        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

    except Exception as e:
        print("YouTube comments error:", e)
        return []

    return comments


def collect_youtube_reviews(product_name, max_videos=3, comments_per_video=20):
    videos = search_youtube_videos(product_name, max_results=max_videos)

    all_comments = []

    for video in videos:
        comments = get_video_comments(
            video["video_id"],
            max_comments=comments_per_video
        )

        for comment in comments:
            all_comments.append({
                "source": "youtube",
                "video_title": video["title"],
                "channel": video["channel"],
                "video_url": video["url"],
                "text": comment
            })

    return {
        "videos": videos,
        "comments": all_comments
    }