from tools.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

def evaluate_summary(ocr_text: str, summary: str) -> dict:
    """
    Evaluate the faithfulness of a summary against the original OCR text.
    Returns a dict with faithfulness_score (1-5) and hallucination (bool).
    """
    system_msg = """You are an evaluation assistant. Compare the original OCR text with the generated summary.

Evaluate:
1. Faithfulness Score (1-5): How accurately does the summary reflect the original text?
   - 5: Perfect, all details are accurate
   - 4: Very good, minor omissions
   - 3: Acceptable, some details missing or slightly off
   - 2: Poor, significant inaccuracies
   - 1: Very poor, mostly inaccurate

2. Hallucination: Does the summary contain information NOT present in the original text?

Respond ONLY with valid JSON in this exact format:
{"faithfulness_score": <int 1-5>, "hallucination": <true/false>}"""

    user_msg = """ORIGINAL OCR TEXT:
{ocr_text}

GENERATED SUMMARY:
{summary}"""

    try:
        llm = get_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg),
            ("user", user_msg)
        ])
        chain = prompt | llm | StrOutputParser()
        
        result_text = chain.invoke({
            "ocr_text": ocr_text,
            "summary": summary
        })
        
        result_text = result_text.strip()
        try:
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
