from tools.ocr import run_ocr
from tools.web_search import fetch_book_summary
from tools.summarizer import summarize_page
from tools.prompt_generator import generate_image_prompt
from tools.image_gen import generate_image
from evaluation.evaluation import evaluate_summary

def run_agent(image_path: str, book_name: str, author_name: str = ""):
    ocr_text, confidence = run_ocr(image_path)

    book_summary = fetch_book_summary(book_name, author_name)

    page_summary = summarize_page(ocr_text)

    # Evaluate the summary for faithfulness and hallucination
    evaluation = evaluate_summary(ocr_text, page_summary)

    image_prompt = generate_image_prompt(
        page_summary=page_summary,
        book_context=book_summary
    )

    image = generate_image(image_prompt)

    return {
        "ocr_text": ocr_text,
        "ocr_confidence": confidence,
        "book_context": book_summary,
        "summary": page_summary,
        "image_prompt": image_prompt,
        "image": image,
        "evaluation": evaluation
    }
