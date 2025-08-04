import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


def scrape_article(url: str) -> str:
    """Fetch and extract text content from the given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator="\n")


def summarize_article(url: str, temperature: float = 0.7) -> str:
    """
    Scrape the article at `url` and use OpenAI GPT model
    to generate a concise, organized summary.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    content = scrape_article(url)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        temperature=temperature,
    )
    return response.choices[0].message.content
