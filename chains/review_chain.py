"""
chains/review_chain.py
"""

import os
import json
import time
from groq import Groq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

REVIEW_PROMPT = PromptTemplate(
    input_variables=["review", "category"],
    template="""
You are an expert e-commerce review analyst.
Analyze the following {category} product review and respond ONLY with a valid JSON object.

Review:
\"\"\"{review}\"\"\"

Return EXACTLY this JSON structure (no extra text, no markdown, no backticks):
{{
  "sentiment": "<one of: Positive | Negative | Neutral | Mixed>",
  "summary": "<one clear sentence summarizing the review>",
  "issues": ["<issue 1>", "<issue 2>"],
  "positives": ["<positive 1>", "<positive 2>"],
  "action": "<recommended business action>",
  "confidence": "<High | Medium | Low>"
}}
"""
)


def analyze_review(review_text, category="General"):
    formatted_prompt = REVIEW_PROMPT.format(
        review=review_text,
        category=category
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a precise JSON-only response bot. Never include markdown or explanation."
            },
            {
                "role": "user",
                "content": formatted_prompt
            }
        ],
        temperature=0.2,
        max_tokens=400,
    )
    return response.choices[0].message.content


def bulk_analyze(reviews, category="General"):
    from utils.helpers import parse_analysis
    results = []
    for review in reviews:
        try:
            raw = analyze_review(review, category)
            parsed = parse_analysis(raw)
            results.append(parsed)
            time.sleep(0.5)
        except Exception as e:
            results.append({
                "sentiment": "Error",
                "summary": f"Analysis failed: {str(e)}",
                "issues": [],
                "positives": [],
                "action": "Retry",
                "confidence": "Low"
            })
    return results