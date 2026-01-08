from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

client = InferenceClient(token=HF_API_KEY)

SYSTEM_PROMPT = """You are an expert literary analyst. Your task is to analyze book page text and extract key visual and narrative elements.

You must respond in the following structured format:

**SCENE DESCRIPTION**: A vivid 2-3 sentence description of what is happening in this passage.

**CHARACTERS**: List any characters mentioned with brief descriptions (appearance, emotion, action).

**SETTING**: Describe the physical location, time of day, weather, and atmosphere.

**MOOD**: The emotional tone (e.g., tense, romantic, melancholic, adventurous).

**KEY VISUAL ELEMENTS**: List 3-5 specific objects, colors, or visual details mentioned.

**ACTION**: What is the main action or event occurring?

Be specific and focus on visually representable details. If information is not available, make reasonable inferences based on context."""

def summarize_page(ocr_text: str) -> str:
    """Extract structured visual elements from book page text"""
    
    if not ocr_text or len(ocr_text.strip()) < 20:
        return "Insufficient text extracted from the image."
    
    try:
        response = client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""Analyze the following book page text and extract visual elements for illustration:

---
{ocr_text}
---

Provide your structured analysis:"""
                }
            ],
            model="HuggingFaceH4/zephyr-7b-beta",
            max_tokens=800,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during summarization: {str(e)}"
