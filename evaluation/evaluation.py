from huggingface_hub import InferenceClient
import os
import json
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
client = InferenceClient(token=HF_API_KEY)


def evaluate_summary(ocr_text: str, summary: str) -> dict:
    """
    Evaluate the faithfulness of a summary against the original OCR text.
    Returns a dict with faithfulness_score (1-5) and hallucination (bool).
    """
    prompt = f"""You are an evaluation assistant. Compare the original OCR text with the generated summary.

ORIGINAL OCR TEXT:
{ocr_text}

GENERATED SUMMARY:
{summary}

Evaluate:
1. Faithfulness Score (1-5): How accurately does the summary reflect the original text?
   - 5: Perfect, all details are accurate
   - 4: Very good, minor omissions
   - 3: Acceptable, some details missing or slightly off
   - 2: Poor, significant inaccuracies
   - 1: Very poor, mostly inaccurate

2. Hallucination: Does the summary contain information NOT present in the original text?

Respond ONLY with valid JSON in this exact format:
{{"faithfulness_score": <int 1-5>, "hallucination": <true/false>}}"""

    try:
        response = client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="google/gemma-2-2b-it",
            max_tokens=100,
            temperature=0.1
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON from the response
        try:
            # Find JSON in the response
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            if start != -1 and end > start:
                result = json.loads(result_text[start:end])
                return {
                    "faithfulness_score": result.get("faithfulness_score", 3),
                    "hallucination": result.get("hallucination", False)
                }
        except json.JSONDecodeError:
            pass
        
        # Default fallback
        return {"faithfulness_score": 3, "hallucination": False}
        
    except Exception as e:
        print(f"Evaluation error: {e}")
        return {"faithfulness_score": 0, "hallucination": False, "error": str(e)}
