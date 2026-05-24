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

    linkedin_prompt = f"""You are a thought leader and content writer at Krianno TechLabs — an AI analytics company founded in 2025 that helps SMBs and mid-market businesses turn data chaos into revenue growth through advanced analytics, autonomous AI agents, and intelligent data pipelines.

Write a LinkedIn post based on the following topic and article:

{context}

Choose ONE of these formats for the post:
- A client case study (anonymized): describe a real-world problem a business faced, how an AI/data solution solved it, and the measurable outcome
- A new AI solution or capability: explain what it does, the problem it solves, and why it matters for businesses today
- A thought leadership insight: a sharp observation about AI/data trends with a practical takeaway for business leaders

Requirements:
- Written as if posted by Krianno TechLabs
- Professional, sharp, and insights-driven tone
- 150–250 words
- Use short paragraphs for readability
- End with a thought-provoking question or CTA (e.g. "Curious how this could work for your business? Let's talk → kriannotechlabs.com")
- Maximum 3 relevant hashtags at the very end
- No emojis
- Return only the post text, nothing else."""

    instagram_prompt = f"""You are a creative content writer for Krianno TechLabs — an AI analytics company that helps businesses of all sizes unlock the power of their data using AI agents, predictive analytics, and intelligent automation.

Write an Instagram caption based on the following topic and article:

{context}

Choose ONE of these formats:
- A quick client win: "A client came to us with X problem. Here's what happened when we applied AI 👇"
- A surprising AI stat or insight that stops the scroll
- A relatable business pain point that AI can solve

Requirements:
- Written as Krianno TechLabs
- Conversational, engaging, and relatable — not overly corporate
- 60–120 words of caption text (before hashtags)
- 2–4 emojis naturally placed
- End with a soft CTA like "Link in bio" or "DM us to learn more"
- 10–15 relevant hashtags on a new line at the end
- Return only the caption with hashtags, nothing else."""

    linkedin_response = model.generate_content(linkedin_prompt)
    instagram_response = model.generate_content(instagram_prompt)

    return {
        "linkedin": linkedin_response.text.strip(),
        "instagram": instagram_response.text.strip(),
        "article_title": article.get("title", ""),
        "article_link": article.get("link", ""),
    }
