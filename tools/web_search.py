import requests
from urllib.parse import quote

def fetch_book_summary(book_name: str, author_name: str = "") -> str:
    """
    Fetch book summary from Open Library API.
    Uses both book name and author for accurate results.
    """
    
    if not book_name or len(book_name.strip()) < 2:
        return ""
    
    # Build search query with author if provided
    search_query = book_name
    if author_name:
        search_query = f"{book_name} {author_name}"
    
    # Strategy 1: Open Library Search API
    try:
        search_url = "https://openlibrary.org/search.json"
        params = {
            "title": book_name,
            "limit": 1
        }
        if author_name:
            params["author"] = author_name
        
        r = requests.get(search_url, params=params, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            docs = data.get("docs", [])
            if docs:
                book = docs[0]
                title = book.get("title", book_name)
                authors = ", ".join(book.get("author_name", ["Unknown"]))
                first_sentence = " ".join(book.get("first_sentence", [""]))
                subjects = ", ".join(book.get("subject", [])[:5])
                publish_year = book.get("first_publish_year", "Unknown")
                
                summary = f"Title: {title}\n"
                summary += f"Author: {authors}\n"
                summary += f"First Published: {publish_year}\n"
                if subjects:
                    summary += f"Subjects: {subjects}\n"
                if first_sentence:
                    summary += f"Opening: {first_sentence}\n"
                
                # Try to get description from work
                work_key = book.get("key", "")
                if work_key:
                    try:
                        work_url = f"https://openlibrary.org{work_key}.json"
                        wr = requests.get(work_url, timeout=5)
                        if wr.status_code == 200:
                            work_data = wr.json()
                            desc = work_data.get("description", "")
                            if isinstance(desc, dict):
                                desc = desc.get("value", "")
                            if desc:
                                summary += f"\nDescription: {desc[:500]}"
                    except:
                        pass
                
                return summary
    except Exception as e:
        print(f"Open Library failed: {e}")
    
    # Strategy 2: DuckDuckGo Instant Answers
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={quote(search_query + ' book')}&format=json&no_html=1"
        r = requests.get(ddg_url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            abstract = data.get("Abstract", "")
            if abstract:
                return f"DuckDuckGo: {abstract}"
    except Exception as e:
        print(f"DuckDuckGo failed: {e}")
    
    return f"No book information found for '{book_name}'" + (f" by {author_name}" if author_name else "")
