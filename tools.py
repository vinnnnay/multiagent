from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import requests
except ImportError:
    requests = None

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    if TavilyClient is None:
        return "tavily-python is not installed; web search is unavailable."

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "TAVILY_API_KEY is not configured; web search is unavailable."

    tavily = TavilyClient(api_key=api_key)
    results = tavily.search(query=query, max_results=5)

    out = []
    for r in results.get('results', []):
        out.append(
            f"Title: {r.get('title', 'N/A')}\nURL: {r.get('url', 'N/A')}\nSnippet: {r.get('content', '')[:300]}\n"
        )

    return "\n----\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    if requests is None:
        return "requests is not installed; scraping is unavailable."

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return "beautifulsoup4 is not installed; scraping is unavailable."

    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
