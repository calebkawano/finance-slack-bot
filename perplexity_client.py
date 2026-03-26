import logging
import requests
from config import PERPLEXITY_API_KEY

logger = logging.getLogger(__name__)

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

SYSTEM_PROMPT = (
    "You are a finance news assistant. When asked for a finance news story, "
    "respond using EXACTLY this format with no extra text:\n"
    "HEADLINE: <the article headline>\n"
    "SUMMARY: <1-2 sentence summary of the story>\n"
    "URL: <direct link to the article>"
)

USER_PROMPT = (
    "Find the single most important finance news story from today. "
    "It can be about markets, stocks, macroeconomics, earnings, or crypto. "
    "Provide the headline, a 1-2 sentence summary, and a direct URL to the source article."
)


def fetch_finance_news() -> tuple[str, str, str]:
    """
    Query Perplexity for today's top finance news story.
    Returns (headline, summary, url). Raises on API errors.
    """
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
    }

    response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()
    citations = data.get("citations", [])

    logger.debug("Perplexity raw response:\n%s", content)

    headline, summary, url = _parse_response(content)

    # Fall back to first citation if URL wasn't parsed from the body
    if not url and citations:
        url = citations[0]
        logger.info("URL not found in body; using first citation: %s", url)

    if not headline:
        raise ValueError("Perplexity response did not contain a parseable headline.")

    return headline, summary, url


def _parse_response(content: str) -> tuple[str, str, str]:
    headline = ""
    summary = ""
    url = ""

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("HEADLINE:"):
            headline = stripped.removeprefix("HEADLINE:").strip()
        elif stripped.startswith("SUMMARY:"):
            summary = stripped.removeprefix("SUMMARY:").strip()
        elif stripped.startswith("URL:"):
            url = stripped.removeprefix("URL:").strip()

    return headline, summary, url
