import json
import os
import random
import sys

from rss_fetcher import fetch_article
from content_generator import generate_posts
from image_fetcher import generate_image
from linkedin_poster import post_to_linkedin
from instagram_poster import post_to_instagram


def load_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "topics.json")
    with open(config_path) as f:
        return json.load(f)


def build_raw_github_url() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "shivamwahi2000/social-autoposter")
    return f"https://raw.githubusercontent.com/{repo}/main/latest_post.jpg"


def main() -> None:
    config = load_config()
    topic = random.choice(config["topics"])
    feeds = config["rss_feeds"]

    print(f"[+] Today's topic: {topic}")

    article = fetch_article(feeds)
    if article:
        print(f"[+] Article: {article['title']} ({article['source']})")
    else:
        print("[!] No article fetched — generating from topic only.")
        article = {"title": topic, "summary": "", "link": "", "source": ""}

    print("[+] Generating posts with Gemini Flash...")
    posts = generate_posts(article, topic)

    print("[+] Generating image with Gemini Imagen...")
    image_path = generate_image(topic)

    results = {}

    # LinkedIn
    linkedin_ok = post_to_linkedin(posts["linkedin"])
    results["linkedin"] = "posted" if linkedin_ok else "skipped/failed"

    # Instagram
    if image_path:
        image_url = build_raw_github_url()
        instagram_ok = post_to_instagram(posts["instagram"], image_url)
        results["instagram"] = "posted" if instagram_ok else "skipped/failed"
    else:
        print("[!] No image generated — skipping Instagram.")
        results["instagram"] = "skipped (no image)"

    # Summary
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    for platform, status in results.items():
        icon = "✓" if status == "posted" else "✗"
        print(f"  {icon} {platform.capitalize()}: {status}")

    print("\n--- LinkedIn Post ---")
    print(posts["linkedin"])
    print("\n--- Instagram Caption ---")
    print(posts["instagram"])

    if all(s != "posted" for s in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
