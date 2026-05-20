"""
utils/helpers.py
────────────────
Parsing and display utilities for review analysis results.
"""

import json
import re


def parse_analysis(raw_text: str) -> dict:
    """
    Safely parse the LLM's JSON response.
    Handles edge cases like extra whitespace or partial markdown.
    """
    if not raw_text:
        return _empty_result("Empty response from LLM")

    # Strip markdown code fences if model adds them
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*",     "", cleaned)
    cleaned = re.sub(r"\s*```$",     "", cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        # Normalize sentiment to Title Case
        if "sentiment" in data:
            data["sentiment"] = str(data["sentiment"]).capitalize()
        return data
    except json.JSONDecodeError:
        # Fallback: try to extract JSON object with regex
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        return _empty_result(f"Could not parse: {cleaned[:100]}")


def _empty_result(reason: str) -> dict:
    return {
        "sentiment": "Unknown",
        "summary": reason,
        "issues": [],
        "positives": [],
        "action": "Manual review needed",
        "confidence": "Low"
    }


def render_sentiment_badge(sentiment: str) -> str:
    """Return HTML badge string for a sentiment label."""
    colors = {
        "positive": ("#14532d", "#86efac"),
        "negative": ("#450a0a", "#fca5a5"),
        "neutral":  ("#1c1917", "#d6d3d1"),
        "mixed":    ("#1c1400", "#fde68a"),
    }
    bg, fg = colors.get(sentiment.lower(), ("#1c1917", "#d6d3d1"))
    return (
        f'<span style="background:{bg}; color:{fg}; padding:3px 12px; '
        f'border-radius:20px; font-size:0.8rem; font-weight:600;">'
        f'{sentiment.upper()}</span>'
    )
