from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from tools.ocr import run_ocr
from tools.web_search import fetch_book_summary
from tools.summarizer import summarize_page
from tools.prompt_generator import generate_image_prompt
from tools.image_gen import generate_image
from evaluation.evaluation import evaluate_summary

def run_agent(image_path: str, book_name: str, author_name: str = ""):
    """
    Orchestrate the BookVision pipeline using LangChain Expression Language (LCEL).
    """
    
    # Step 1: Initial Data Loading (OCR + Book Context)
    step1_loader = RunnablePassthrough.assign(
        ocr_result=lambda x: run_ocr(x["image_path"]),
        book_context=lambda x: fetch_book_summary(x["book_name"], x["author_name"])
    ) | RunnablePassthrough.assign(
        ocr_text=lambda x: x["ocr_result"][0],
        ocr_confidence=lambda x: x["ocr_result"][1]
    )
    
    # Step 2: Summarization
    step2_summarizer = RunnablePassthrough.assign(
        summary=lambda x: summarize_page(x["ocr_text"])
    )
    
    # Step 3: Evaluation & Prompt Gen (Parallel)
    step3_processing = RunnablePassthrough.assign(
        evaluation=lambda x: evaluate_summary(x["ocr_text"], x["summary"]),
        image_prompt=lambda x: generate_image_prompt(x["summary"], x["book_context"])
    )
    
    # Step 4: Image Generation
    step4_generation = RunnablePassthrough.assign(
        image=lambda x: generate_image(x["image_prompt"])
    )
    
    # Full chain
    agent_chain = step1_loader | step2_summarizer | step3_processing | step4_generation
    
    # Execute
    result = agent_chain.invoke({
        "image_path": image_path,
        "book_name": book_name,
        "author_name": author_name
    })
    
    return result
