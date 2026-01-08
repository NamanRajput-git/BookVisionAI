from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    Returns a shared instance of the ChatHuggingFace LLM.
    Configured for Google Gemma-2-2B-IT.
    """
    llm = HuggingFaceEndpoint(
        repo_id="google/gemma-2-2b-it",
        task="text-generation",
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.4,
        huggingfacehub_api_token=os.getenv("HF_API_KEY")
    )
    
    return ChatHuggingFace(llm=llm)
