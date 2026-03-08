import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
HN_SHOW_URL = "https://news.ycombinator.com/show"
YC_COMPANIES_URL = "https://www.ycombinator.com/companies"


def fetch_hn_show_startups():
    response = requests.get(
        HN_SHOW_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    startups = []

    rows = soup.select("tr.athing")

    for row in rows:
        title_link = row.select_one(".titleline > a")
        if not title_link:
            continue

        title = title_link.get_text(strip=True)
        href = title_link.get("href", "")

        if not title.lower().startswith("show hn"):
            continue

        clean_name = title.replace("Show HN:", "").replace("Show HN", "").strip()
        item_id = row.get("id")

        subtext = row.find_next_sibling("tr")
        score = 0
        comments = 0
        author = ""

        if subtext:
            score_tag = subtext.select_one(".score")
            if score_tag:
                try:
                    score = int(score_tag.text.split()[0])
                except Exception:
                    score = 0

            user_tag = subtext.select_one(".hnuser")
            if user_tag:
                author = user_tag.text

            comments_links = subtext.select("a")
            for link in comments_links:
                if "comment" in link.text:
                    try:
                        comments = int(link.text.split()[0])
                    except Exception:
                        comments = 0

        website = href if href.startswith("http") else ""

        startups.append(
            {
                "name": clean_name[:255],
                "description": title,
                "website": website,
                "category": "Show HN",
                "source": "hn",
                "source_url": f"https://news.ycombinator.com/item?id={item_id}",
                "external_id": item_id or "",
                "author": author,
                "score": score,
                "comments_count": comments,
            }
        )

    return startups


def fetch_yc_startups():
    response = requests.get(
        YC_COMPANIES_URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    startups = []
    seen = set()

    links = soup.find_all("a", href=True)

    for link in links:
        href = link.get("href", "").strip()
        text = link.get_text(" ", strip=True)

        if not href.startswith("/companies/"):
            continue

        slug = href.split("/companies/")[-1].strip("/")
        if not slug or slug in seen:
            continue

        seen.add(slug)

        name = text.split("\n")[0].strip() if text else slug.replace("-", " ").title()
        if not name:
            continue

        startups.append(
            {
                "name": name[:255],
                "description": "",
                "website": "",
                "category": "YC Company",
                "source": "yc",
                "source_url": f"https://www.ycombinator.com{href}",
                "external_id": slug,
                "author": "",
                "score": 0,
                "comments_count": 0,
            }
        )

    return startups[:100]

def fetch_github_ai_projects():
    response = requests.get(
        "https://github.com/topics/artificial-intelligence",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    startups = []
    seen = set()

    article_cards = soup.select("article.border")

    for card in article_cards:
        repo_link = card.select_one("h3 a")
        desc_tag = card.select_one("p")

        if not repo_link:
            continue

        href = repo_link.get("href", "").strip()
        if not href:
            continue

        repo_name = repo_link.get_text(" ", strip=True).replace("\n", " ").replace(" / ", "/")
        repo_name = " ".join(repo_name.split())

        if repo_name.lower() in seen:
            continue
        seen.add(repo_name.lower())

        description = desc_tag.get_text(" ", strip=True) if desc_tag else ""

        startups.append(
            {
                "name": repo_name[:255],
                "description": description,
                "website": f"https://github.com{href}",
                "category": "AI Project",
                "source": "ph",
                "source_url": f"https://github.com{href}",
                "external_id": href.strip("/").replace("/", "_"),
                "author": href.strip("/").split("/")[0],
                "score": 0,
                "comments_count": 0,
            }
        )

    return startups[:50]