import requests

HEADERS = {
    "User-Agent": "ReviewRadarBot/1.0"
}

def collect_reddit_reviews(keyword, limit=5):
    posts = []
    comments = []

    try:
        url = f"https://www.reddit.com/search.json?q={keyword}&limit={limit}"

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            print("Reddit search status:", response.status_code)
            print("Reddit search text:", response.text[:300])
            return {
                "posts": posts,
                "comments": comments
            }

        data = response.json()

        for post in data.get("data", {}).get("children", []):
            post_data = post.get("data", {})

            title = post_data.get("title", "")
            permalink = post_data.get("permalink", "")

            if not permalink:
                continue

            post_url = f"https://www.reddit.com{permalink}"

            posts.append({
                "title": title,
                "url": post_url
            })

            try:
                comment_url = f"https://www.reddit.com{permalink}.json"

                comment_response = requests.get(
                    comment_url,
                    headers=HEADERS,
                    timeout=10
                )

                if comment_response.status_code != 200:
                    print("Reddit comment status:", comment_response.status_code)
                    continue

                comment_json = comment_response.json()

                if len(comment_json) > 1:
                    comment_list = comment_json[1].get("data", {}).get("children", [])

                    for c in comment_list[:10]:
                        if c.get("kind") != "t1":
                            continue

                        body = c.get("data", {}).get("body", "")

                        if body:
                            comments.append({
                                "text": body,
                                "source": "Reddit"
                            })

            except Exception as e:
                print("Reddit comment error:", e)

    except Exception as e:
        print("Reddit search error:", e)

    return {
        "posts": posts,
        "comments": comments
    }