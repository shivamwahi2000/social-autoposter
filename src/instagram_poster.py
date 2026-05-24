import os
import requests
import time


_GRAPH_BASE = "https://graph.facebook.com/v19.0"


def post_to_instagram(caption: str, image_url: str) -> bool:
    """
    Publish a photo post to an Instagram Business account via the Graph API.

    Two-step process required by Meta:
      1. Create a media container (returns creation_id)
      2. Publish the container
    """
    ig_user_id = os.environ.get("INSTAGRAM_USER_ID", "")
    access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")

    if not ig_user_id or not access_token:
        print("INSTAGRAM_USER_ID or INSTAGRAM_ACCESS_TOKEN not set — skipping Instagram.")
        return False

    # Step 1: create media container
    container_resp = requests.post(
        f"{_GRAPH_BASE}/{ig_user_id}/media",
        params={
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token,
        },
        timeout=20,
    )

    if container_resp.status_code != 200:
        print(f"Instagram container creation failed: {container_resp.status_code} {container_resp.text}")
        return False

    creation_id = container_resp.json().get("id")
    if not creation_id:
        print("Instagram: no creation_id returned from container endpoint.")
        return False

    # Brief pause — Meta recommends waiting before publishing
    time.sleep(2)

    # Step 2: publish
    publish_resp = requests.post(
        f"{_GRAPH_BASE}/{ig_user_id}/media_publish",
        params={
            "creation_id": creation_id,
            "access_token": access_token,
        },
        timeout=20,
    )

    if publish_resp.status_code == 200:
        print(f"Instagram post ID: {publish_resp.json().get('id', 'unknown')}")
        return True

    print(f"Instagram publish failed: {publish_resp.status_code} {publish_resp.text}")
    return False
