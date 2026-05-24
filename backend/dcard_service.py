import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def collect_dcard_reviews(keyword, limit=10):

    posts = []
    comments = []

    try:

        search_url = (
            f"https://www.dcard.tw/service/api/v2/search/posts"
            f"?query={keyword}"
        )

        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:
            print("Dcard search failed:", response.status_code)

            return {
                "posts": posts,
                "comments": comments
            }

        data = response.json()

        for post in data[:limit]:

            title = post.get("title", "")
            excerpt = post.get("excerpt", "")
            post_id = post.get("id")

            forum = post.get("forumName", "")

            post_url = (
                f"https://www.dcard.tw/f/{forum}/p/{post_id}"
            )

            posts.append({
                "title": title,
                "url": post_url
            })

            if excerpt:
                comments.append({
                    "text": excerpt,
                    "source": "Dcard"
                })

            # 抓留言
            try:

                comment_url = (
                    f"https://www.dcard.tw/service/api/v2/posts/{post_id}/comments"
                )

                comment_response = requests.get(
                    comment_url,
                    headers=HEADERS,
                    timeout=10
                )

                if comment_response.status_code != 200:
                    continue

                comment_data = comment_response.json()

                for c in comment_data[:10]:

                    content = c.get("content", "")

                    if content:
                        comments.append({
                            "text": content,
                            "source": "Dcard"
                        })

            except Exception as e:
                print("Dcard comment error:", e)

    except Exception as e:
        print("Dcard error:", e)

    return {
        "posts": posts,
        "comments": comments
    }