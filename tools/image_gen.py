from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

def generate_image(prompt: str):
    """Use HuggingFace Hub InferenceClient for image generation"""
    
    client = InferenceClient(token=HF_API_KEY)
    
    try:
        # Generate image using text-to-image
        image = client.text_to_image(
            prompt,
            model=HF_MODEL
        )
        
        # Convert PIL Image to bytes
        from io import BytesIO
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
        
    except Exception as e:
        print(f"Image generation error: {str(e)}")
        return b""  # Return empty bytes on error
