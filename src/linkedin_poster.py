import os
import requests


def _get_person_id(token: str) -> str | None:
    response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if response.status_code == 200:
        return response.json().get("id")
    print(f"Could not fetch LinkedIn person ID: {response.status_code} {response.text}")
    return None


def post_to_linkedin(text: str) -> bool:
    """Post a text update to LinkedIn (personal profile or organization page)."""
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
    if not token:
        print("LINKEDIN_ACCESS_TOKEN not set — skipping LinkedIn.")
        return False

    org_id = os.environ.get("LINKEDIN_ORG_ID", "")
    if org_id:
        author = f"urn:li:organization:{org_id}"
    else:
        person_id = _get_person_id(token)
        if not person_id:
            return False
        author = f"urn:li:person:{person_id}"

    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=payload,
        timeout=15,
    )

    if response.status_code == 201:
        print(f"LinkedIn post ID: {response.headers.get('x-restli-id', 'unknown')}")
        return True

    print(f"LinkedIn post failed: {response.status_code} {response.text}")
    return False
