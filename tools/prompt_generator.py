from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
client = InferenceClient(token=HF_API_KEY)


def extract_book_metadata(book_context: str) -> dict:
    """Extract structured metadata from Open Library context."""
    metadata = {
        "title": "",
        "author": "",
        "year": "",
        "genre": "",
        "subjects": ""
    }
    
    if not book_context:
        return metadata
    
    for line in book_context.split("\n"):
        if line.startswith("Title:"):
            metadata["title"] = line.replace("Title:", "").strip()
        elif line.startswith("Author:"):
            metadata["author"] = line.replace("Author:", "").strip()
        elif line.startswith("First Published:"):
            metadata["year"] = line.replace("First Published:", "").strip()
        elif line.startswith("Subjects:"):
            metadata["subjects"] = line.replace("Subjects:", "").strip()
            metadata["genre"] = metadata["subjects"].split(",")[0].strip()
    
    return metadata


def get_era_style(year: str) -> str:
    """Map publication year to artistic era and style."""
    try:
        yr = int(year)
        if yr < 1800:
            return "classical painting style, baroque or renaissance aesthetics, rich oil painting textures"
        elif yr < 1850:
            return "romantic era illustration, dramatic landscapes, emotional intensity, JMW Turner inspired"
        elif yr < 1900:
            return "Victorian illustration style, detailed engravings, Pre-Raphaelite influences, realistic portraiture"
        elif yr < 1950:
            return "early 20th century illustration, art nouveau elements, golden age illustration style"
        elif yr < 2000:
            return "mid-century illustration, bold compositions, realistic rendering"
        else:
            return "contemporary digital art, cinematic composition, photorealistic elements"
    except:
        return "classical book illustration style"


def refine_prompt_with_llm(scene_summary: str, book_context: str, metadata: dict) -> str:
    """Use LLM to create a refined, thematic prompt."""
    
    era_style = get_era_style(metadata.get("year", ""))
    
    try:
        response = client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert art director creating image prompts for book illustrations.
Your task is to convert a scene description into a detailed visual prompt that:
1. Preserves the literary theme and mood of the book
2. Uses period-appropriate visual style
3. Focuses on concrete visual elements (lighting, composition, colors)
4. Avoids inventing details not in the scene

Output ONLY the refined prompt, no explanations."""
                },
                {
                    "role": "user",
                    "content": f"""Create an illustration prompt for this scene:

BOOK: {metadata.get('title', 'Unknown')} by {metadata.get('author', 'Unknown')}
ERA: {metadata.get('year', 'Unknown')}
GENRE: {metadata.get('genre', 'Literary Fiction')}
RECOMMENDED STYLE: {era_style}

SCENE TO ILLUSTRATE:
{scene_summary}

Generate a detailed, visual prompt that captures the essence of this scene while staying true to the book's era and theme."""
                }
            ],
            model="google/gemma-2-2b-it",
            max_tokens=400,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM refinement failed: {e}")
        return None


def generate_image_prompt(page_summary: str, book_context: str) -> str:
    """
    Generate a refined, theme-preserving image prompt.
    Uses LLM to enhance the prompt with book-specific style.
    """
    
    # Extract metadata from book context
    metadata = extract_book_metadata(book_context)
    
    # Get era-appropriate style
    era_style = get_era_style(metadata.get("year", ""))
    
    # Try LLM refinement
    refined_prompt = refine_prompt_with_llm(page_summary, book_context, metadata)
    
    if refined_prompt:
        # Add quality modifiers to LLM output
        final_prompt = f"""masterpiece, best quality, highly detailed illustration

{refined_prompt}

STYLE: {era_style}
QUALITY: professional book illustration, sharp details, rich textures"""
    else:
        # Fallback to template-based prompt
        final_prompt = f"""masterpiece, best quality, highly detailed illustration

BOOK: {metadata.get('title', 'Unknown')} ({metadata.get('year', '')})
GENRE: {metadata.get('genre', 'Literary Fiction')}

SCENE:
{page_summary}

STYLE: {era_style}
ATMOSPHERE: Faithful to the literary source, emotionally resonant
QUALITY: professional book illustration, sharp details, rich textures"""

    return final_prompt.strip()


def validate_prompt(prompt: str, page_summary: str) -> bool:
    """Validates prompt is correctly formatted."""
    return "SCENE" in prompt or "illustration" in prompt.lower()
