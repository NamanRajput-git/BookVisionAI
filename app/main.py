from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
from app.agent import run_agent

app = FastAPI()

# Enable CORS for Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/process-page/")
async def process_page(
    book_name: str,
    file: UploadFile,
    author_name: str = ""
):
    import tempfile
    import os
    import traceback
    from fastapi.responses import JSONResponse

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            image_path = tmp.name

        import base64
        
        result = run_agent(image_path, book_name, author_name)
        
        image_b64 = ""
        if result["image"]:
            image_b64 = base64.b64encode(result["image"]).decode("utf-8")
        
        return {
            "ocr_text": result["ocr_text"],
            "ocr_confidence": result["ocr_confidence"],
            "book_context": result["book_context"],
            "summary": result["summary"],
            "image_prompt": result["image_prompt"],
            "image": image_b64,
            "evaluation": result["evaluation"]
        }
    except Exception as e:
        error_msg = f"Server Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return JSONResponse(status_code=500, content={"detail": error_msg})
