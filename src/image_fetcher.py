import os
import google.generativeai as genai
from pathlib import Path


def generate_image(topic: str) -> str | None:
    """Generate an image using Gemini Imagen and save it to disk. Returns the file path."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("GEMINI_API_KEY not set — skipping image generation.")
        return None

    try:
        genai.configure(api_key=api_key)
        client = genai.ImageGenerationModel("imagen-3.0-generate-002")
        result = client.generate_images(
            prompt=f"A visually striking, professional image representing: {topic}. Clean, modern style, suitable for social media.",
            number_of_images=1,
            aspect_ratio="1:1",
        )
        image_data = result.images[0]._image_bytes

        output_path = Path(__file__).parent.parent / "latest_post.jpg"
        output_path.write_bytes(image_data)
        print(f"Image saved to {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None
