# 🔍 ReviewIQ — E-Commerce Review Analyzer

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=flat&logo=chainlink&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-F55036?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

An AI-powered product review analysis tool built with **LangChain prompt chains**, **Groq LLM API (LLaMA 3)**, and **Streamlit**. Designed to extract sentiment, key issues, highlights, and recommended actions from e-commerce product reviews — both single and in bulk via CSV.

---

## ✨ Features

- **Single Review Analysis** — Paste any review and get structured AI insights instantly
- **Bulk CSV Processing** — Upload a CSV with a `review` column and analyze up to 50 reviews at once
- **Structured JSON Output** — LangChain PromptTemplate enforces consistent, parseable LLM responses
- **Sentiment Classification** — Positive / Negative / Neutral / Mixed
- **Actionable Recommendations** — Business action suggested per review
- **Export Results** — Download analyzed CSV with new columns

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| LLM Backend | Groq API — LLaMA 3 8B (free tier) |
| Prompt Engineering | LangChain `PromptTemplate` |
| UI | Streamlit |
| Data Processing | Pandas |
| Language | Python 3.11+ |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/review-analyzer.git
cd review-analyzer
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Get a free Groq API key at [console.groq.com](https://console.groq.com)

```bash
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY
```

### 5. Run the app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
review-analyzer/
├── app.py                    # Main Streamlit application
├── chains/
│   └── review_chain.py       # LangChain PromptTemplate + Groq API calls
├── utils/
│   └── helpers.py            # JSON parsing, badge rendering
├── data/
│   └── sample_reviews.csv    # Sample data for testing
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🧠 How It Works

1. User inputs a review (or uploads CSV)
2. `LangChain PromptTemplate` formats the prompt with `review` and `category` variables
3. Formatted prompt is sent to **Groq's LLaMA 3** via the Groq SDK
4. LLM returns a structured JSON response
5. `helpers.py` safely parses the JSON with fallback handling
6. Results are displayed in the Streamlit UI

```python
# Core LangChain pattern used in this project
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["review", "category"],
    template="Analyze this {category} review: {review} ..."
)
formatted = prompt.format(review="Great product!", category="Electronics")
```

---

## 📊 Sample Output

```json
{
  "sentiment": "Mixed",
  "summary": "Customer praised product quality but was unhappy with late delivery.",
  "issues": ["Delivery arrived 2 days late", "Packaging was damaged"],
  "positives": ["Product works great", "Excellent build quality"],
  "action": "Follow up with customer regarding shipping experience",
  "confidence": "High"
}
```
<img width="1920" height="964" alt="Screenshot 2026-05-20 193256" src="https://github.com/user-attachments/assets/906bb513-e1a3-4d5e-a2ad-340b2b349ad8" />

<img width="1920" height="967" alt="Screenshot 2026-05-20 193312" src="https://github.com/user-attachments/assets/c13f1864-b839-45a0-a5b3-0768cf53a586" />

<img width="1920" height="964" alt="Screenshot 2026-05-20 193344" src="https://github.com/user-attachments/assets/f9849b32-b176-4791-9d53-d5ba76f69a7b" />

---

## 🔮 Future Improvements

- [ ] Add OpenAI / Gemini model toggle
- [ ] Trend analysis across multiple CSVs
- [ ] Auto-categorize reviews by product type
- [ ] LangChain memory for multi-turn review conversations
- [ ] Deploy to Streamlit Cloud (free hosting)

---

## 👤 Author

**Gudi Indhu Reddy**
B.Tech Information Technology | Malla Reddy Engineering College for Women | 2026
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)

---
*This project was independently designed and built as part of my Gen-AI portfolio
to demonstrate LLM integration, prompt engineering, and full-stack Python development.*
