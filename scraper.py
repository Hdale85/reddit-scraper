"""
Reddit Trend Scraper
====================
Scrapes trending posts from any subreddit and exports to CSV.
No API key required — uses Reddit's public JSON endpoint.

Usage:
    python scraper.py --subreddit python --limit 25 --sort hot
    python scraper.py --subreddit technology --limit 50 --sort top --output tech_trends.csv
"""

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


HEADERS = {"User-Agent": "RedditTrendScraper/1.0 (personal research tool)"}


def fetch_posts(subreddit: str, sort: str = "hot", limit: int = 25) -> list[dict]:
    """Fetch posts from a subreddit using Reddit's public JSON API."""
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    req = Request(url, headers=HEADERS)

    try:
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: Could not fetch r/{subreddit}")
        sys.exit(1)
    except URLError as e:
        print(f"[ERROR] Network error: {e.reason}")
        sys.exit(1)

    posts = []
    for item in data["data"]["children"]:
        p = item["data"]
        posts.append({
            "rank":        len(posts) + 1,
            "title":       p.get("title", ""),
            "author":      p.get("author", "[deleted]"),
            "score":       p.get("score", 0),
            "upvote_ratio": p.get("upvote_ratio", 0),
            "comments":    p.get("num_comments", 0),
            "awards":      p.get("total_awards_received", 0),
            "flair":       p.get("link_flair_text", ""),
            "is_nsfw":     p.get("over_18", False),
            "url":         f"https://reddit.com{p.get('permalink', '')}",
            "external_url": p.get("url", ""),
            "created_utc": datetime.utcfromtimestamp(p.get("created_utc", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "scraped_at":  datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return posts


def export_csv(posts: list[dict], output_file: str) -> None:
    """Write posts to a CSV file."""
    if not posts:
        print("[WARN] No posts to export.")
        return

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=posts[0].keys())
        writer.writeheader()
        writer.writerows(posts)

    print(f"[OK] Exported {len(posts)} posts → {output_file}")


def print_summary(posts: list[dict], subreddit: str) -> None:
    """Print a quick summary to stdout."""
    print(f"\n{'='*60}")
    print(f"  r/{subreddit} — Top {len(posts)} posts")
    print(f"{'='*60}")
    for p in posts[:10]:  # preview first 10
        score = str(p["score"]).rjust(7)
        print(f"  {score} pts | {p['title'][:55]}")
    if len(posts) > 10:
        print(f"  ... and {len(posts) - 10} more (see CSV)")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Scrape trending Reddit posts to CSV")
    parser.add_argument("--subreddit", default="python",      help="Subreddit name (default: python)")
    parser.add_argument("--sort",      default="hot",         choices=["hot", "top", "new", "rising"], help="Sort order")
    parser.add_argument("--limit",     default=25, type=int,  help="Number of posts (max 100)")
    parser.add_argument("--output",    default="",            help="Output CSV filename (auto-generated if omitted)")
    args = parser.parse_args()

    limit = min(args.limit, 100)
    output = args.output or f"r_{args.subreddit}_{args.sort}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    print(f"[*] Scraping r/{args.subreddit} ({args.sort}, {limit} posts)...")
    time.sleep(1)  # polite delay

    posts = fetch_posts(args.subreddit, args.sort, limit)
    print_summary(posts, args.subreddit)
    export_csv(posts, output)


if __name__ == "__main__":
    main()
