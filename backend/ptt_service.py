import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": "over18=1",
}

# 依商品類型選看板
BOARDS = [
    "MobileComm",   # 手機
    "nb-shopping",  # 筆電/3C
    "PC_Shopping",  # 電腦
    "Steam",        # 遊戲
    "food",         # 食物
    "eat",          # 美食
]


def _fetch_article_text(href: str) -> str:
    try:
        resp = requests.get(
            f"https://www.ptt.cc{href}",
            headers=HEADERS,
            timeout=8,
        )
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.select_one("#main-content")
        if not content:
            return ""
        # 移除 meta 資訊區塊，只留文章本文
        for tag in content.select(".article-metaline, .article-metaline-right"):
            tag.decompose()
        return content.get_text(separator=" ").strip()[:800]
    except Exception as e:
        print("PTT article fetch error:", e)
        return ""


def collect_ptt_reviews(keyword: str, max_posts: int = 3) -> dict:
    posts = []
    comments = []

    for board in BOARDS:
        if len(posts) >= max_posts * 2:
            break
        try:
            resp = requests.get(
                f"https://www.ptt.cc/bbs/{board}/search?q={keyword}",
                headers=HEADERS,
                timeout=10,
            )
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            articles = soup.select(".r-ent")

            for article in articles[:max_posts]:
                title_tag = article.select_one(".title a")
                if not title_tag:
                    continue
                title = title_tag.text.strip()
                href = title_tag.get("href", "")
                if not href:
                    continue

                text = _fetch_article_text(href)
                if not text:
                    continue

                posts.append({
                    "title": title,
                    "url": f"https://www.ptt.cc{href}",
                    "board": board,
                })
                comments.append({
                    "text": text,
                    "source": "PTT",
                })

        except Exception as e:
            print(f"PTT board error ({board}):", e)

    return {"posts": posts, "comments": comments}
