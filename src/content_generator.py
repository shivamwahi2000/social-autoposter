import os
import google.generativeai as genai


def _client() -> genai.GenerativeModel:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-flash")


def generate_posts(article: dict, topic: str) -> dict:
    """Generate platform-specific posts from an article using Gemini Flash."""
    model = _client()

    context = (
        f"Topic: {topic}\n"
        f"Article title: {article['title']}\n"
        f"Article summary: {article['summary']}"
    ).strip()

    linkedin_prompt = f"""You are a professional LinkedIn content creator.

Based on the following article, write a LinkedIn post:

{context}

Requirements:
- Professional, insightful, and thought-provoking tone
- 150–300 words
- End with a question or clear call to action that invites comments
- Maximum 3 hashtags placed at the very end
- No emojis
- Return only the post text, nothing else."""

    instagram_prompt = f"""You are an engaging Instagram content creator.

Based on the following article, write an Instagram caption:

{context}

Requirements:
- Conversational, upbeat, and relatable tone
- 60–150 words of caption text (before hashtags)
- 2–4 emojis naturally placed within the caption
- 10–15 relevant hashtags on a new line at the end
- Return only the caption text with hashtags, nothing else."""

    linkedin_response = model.generate_content(linkedin_prompt)
    instagram_response = model.generate_content(instagram_prompt)

    return {
        "linkedin": linkedin_response.text.strip(),
        "instagram": instagram_response.text.strip(),
        "article_title": article.get("title", ""),
        "article_link": article.get("link", ""),
    }
