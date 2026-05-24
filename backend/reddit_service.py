import requests

HEADERS = {
    "User-Agent": "ReviewRadarBot/1.0"
}

def collect_reddit_reviews(keyword, limit=5):

    posts = []
    comments = []

    url = f"https://www.reddit.com/search.json?q={keyword}&limit={limit}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    data = response.json()

    for post in data["data"]["children"]:

        post_data = post["data"]

        title = post_data.get("title", "")
        selftext = post_data.get("selftext", "")
        permalink = post_data.get("permalink", "")

        post_url = f"https://www.reddit.com{permalink}"

        posts.append({
            "title": title,
            "url": post_url
        })

        # 抓留言
        try:

            comment_url = f"https://www.reddit.com{permalink}.json"

            comment_response = requests.get(
                comment_url,
                headers=HEADERS
            )

            comment_json = comment_response.json()

            if len(comment_json) > 1:

                comment_list = comment_json[1]["data"]["children"]

                for c in comment_list[:10]:

                    if c["kind"] != "t1":
                        continue

                    body = c["data"].get("body", "")

                    if body:
                        comments.append({
                            "text": body,
                            "source": "Reddit"
                        })

        except Exception:
            pass

    return {
        "posts": posts,
        "comments": comments
    }