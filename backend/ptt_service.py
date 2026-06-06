import time
import requests
from bs4 import BeautifulSoup

BOARDS = [
    "MobileComm",
    "nb-shopping",
    "PC_Shopping",
    "Steam",
    "food",
    "eat",
]

def _make_session() -> requests.Session:
    """建立模擬真實瀏覽器的 Session，並通過 PTT 的年齡驗證"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.ptt.cc/",
    })
    # 設定 over18 cookie 通過年齡驗證
    session.cookies.set("over18", "1", domain="www.ptt.cc")
    return session


def _fetch_article_text(session: requests.Session, href: str) -> str:
    try:
        resp = session.get(f"https://www.ptt.cc{href}", timeout=8)
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.select_one("#main-content")
        if not content:
            return ""
        for tag in content.select(".article-metaline, .article-metaline-right, .push"):
            tag.decompose()
        return content.get_text(separator=" ").strip()[:800]
    except Exception as e:
        print("PTT article fetch error:", e)
        return ""


def collect_ptt_reviews(keyword: str, max_posts: int = 3) -> dict:
    posts = []
    comments = []
    session = _make_session()

    for board in BOARDS:
        if len(posts) >= max_posts * 2:
            break
        try:
            resp = session.get(
                f"https://www.ptt.cc/bbs/{board}/search?q={keyword}",
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

                time.sleep(0.5)  # 避免太快被擋
                text = _fetch_article_text(session, href)
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
