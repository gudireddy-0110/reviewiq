import streamlit as st
import pandas as pd
from chains.review_chain import analyze_review, bulk_analyze
from utils.helpers import render_sentiment_badge, parse_analysis

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Review IQ - Review Intelligence for E-Commerce",
    page_icon="🔍",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
}

.main { background-color: #0d0d0d; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f5f5f5 0%, #a3e635 60%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.hero-sub {
    color: #6b7280;
    font-size: 1.05rem;
    margin-bottom: 2rem;
    font-weight: 300;
}
.card {
    background: #161616;
    border: 1px solid #222;
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1rem;
}
.badge-positive  { background:#14532d; color:#86efac; padding:3px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; }
.badge-negative  { background:#450a0a; color:#fca5a5; padding:3px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; }
.badge-neutral   { background:#1c1917; color:#d6d3d1; padding:3px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; }
.badge-mixed     { background:#1c1400; color:#fde68a; padding:3px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; }

.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4b5563;
    margin-bottom: 0.25rem;
}
.result-value {
    color: #e5e7eb;
    font-size: 0.97rem;
    line-height: 1.55;
}
.divider { border-top: 1px solid #1f1f1f; margin: 1.2rem 0; }
.stTextArea textarea {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button {
    background: linear-gradient(135deg, #a3e635, #22d3ee) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.8rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
.upload-box {
    border: 1.5px dashed #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    color: #4b5563;
    font-size: 0.9rem;
}
.metric-box {
    background: #161616;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #a3e635;
}
.metric-label { color: #6b7280; font-size: 0.8rem; margin-top: 0.1rem; }
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 👩‍💻 About This Project")
    st.markdown("**Gudi Indhu Reddy**")
    st.markdown("Aspiring Software Engineer")
    st.markdown("---")
    st.markdown("### 🛠 Tech Stack")
    st.markdown("- ⚡ Groq API — LLaMA 3.3 70B")
    st.markdown("- 🔗 LangChain PromptTemplate")
    st.markdown("- 🐍 Python 3.11")
    st.markdown("- 📊 Pandas — CSV processing")
    st.markdown("- 🖥 Streamlit — UI")
    st.markdown("---")
    st.markdown("### 💡 Why I Built This")
    st.markdown("Many E-commerce platforms process millions of reviews. This tool automates sentiment extraction and gives actionable insights using LLMs.")
    st.markdown("---")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/gudireddy-0110)")
    st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/gudi-indhu-reddy)")
# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">ReviewIQ</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Review Intelligence for E-Commerce · Built using Groq LLM + LangChain</div>', unsafe_allow_html=True)
# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍 Single Review", "📊 Bulk CSV Analysis"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Single Review
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        st.markdown('<div class="result-label">Paste a product review</div>', unsafe_allow_html=True)
        review_text = st.text_area(
            label="",
            placeholder="e.g. The product arrived two days late and the packaging was damaged. However, the item itself works great and the quality is excellent...",
            height=200,
            label_visibility="collapsed"
        )

        product_category = st.selectbox(
            "Product Category (optional — improves accuracy)",
            ["General", "Electronics", "Fashion & Apparel", "Home & Kitchen", "Beauty & Personal Care", "Books", "Sports & Outdoors"],
            label_visibility="visible"
        )

        analyze_btn = st.button("Analyze Review →", use_container_width=False)

    with col_right:
        if analyze_btn:
            if not review_text.strip():
                st.warning("Please paste a review first.")
            else:
                with st.spinner("Analyzing with LLM..."):
                    raw_result = analyze_review(review_text, product_category)
                    result = parse_analysis(raw_result)

                sentiment = result.get("sentiment", "Unknown")
                st.markdown(f'<div class="card">', unsafe_allow_html=True)

                st.markdown(f'<div class="result-label">Sentiment</div>', unsafe_allow_html=True)
                badge_class = f"badge-{sentiment.lower()}" if sentiment.lower() in ["positive","negative","neutral","mixed"] else "badge-neutral"
                st.markdown(f'<span class="{badge_class}">{sentiment.upper()}</span>', unsafe_allow_html=True)
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="result-label">One-Line Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-value">{result.get("summary","—")}</div>', unsafe_allow_html=True)
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="result-label">Key Issues Raised</div>', unsafe_allow_html=True)
                issues = result.get("issues", [])
                if issues:
                    for issue in issues:
                        st.markdown(f'<div class="result-value">• {issue}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-value">No major issues detected.</div>', unsafe_allow_html=True)
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="result-label">Positive Highlights</div>', unsafe_allow_html=True)
                positives = result.get("positives", [])
                if positives:
                    for p in positives:
                        st.markdown(f'<div class="result-value">✓ {p}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-value">None mentioned.</div>', unsafe_allow_html=True)
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="result-label">Recommended Action</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-value">{result.get("action","—")}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="height:340px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
                <div style="font-size:2.5rem; margin-bottom:1rem;">🔍</div>
                <div style="font-family:'Syne',sans-serif; color:#374151; font-size:1rem; font-weight:700;">Analysis will appear here</div>
                <div style="color:#4b5563; font-size:0.85rem; margin-top:0.4rem;">Paste a review and click Analyze</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Bulk CSV
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="result-label" style="margin-bottom:0.8rem;">Upload a CSV file with a <code>review</code> column</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "review" not in df.columns:
            st.error("CSV must have a column named `review`. Please check your file.")
        else:
            st.success(f"Loaded {len(df)} reviews.")
            st.dataframe(df.head(5), use_container_width=True)

            max_rows = st.slider("How many reviews to analyze? (API cost control)", 1, min(50, len(df)), min(10, len(df)))

            if st.button("Run Bulk Analysis →"):
                subset = df.head(max_rows).copy()
                with st.spinner(f"Analyzing {max_rows} reviews... this may take a moment."):
                    results = bulk_analyze(subset["review"].tolist())
                    subset["sentiment"]  = [r.get("sentiment","?") for r in results]
                    subset["summary"]    = [r.get("summary","?") for r in results]
                    subset["action"]     = [r.get("action","?") for r in results]

                # Metrics
                counts = subset["sentiment"].str.lower().value_counts()
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f'<div class="metric-box"><div class="metric-num">{counts.get("positive",0)}</div><div class="metric-label">Positive</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-box"><div class="metric-num">{counts.get("negative",0)}</div><div class="metric-label">Negative</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="metric-box"><div class="metric-num">{counts.get("mixed",0)}</div><div class="metric-label">Mixed</div></div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div class="metric-box"><div class="metric-num">{counts.get("neutral",0)}</div><div class="metric-label">Neutral</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(subset[["review","sentiment","summary","action"]], use_container_width=True)

                csv_out = subset.to_csv(index=False)
                st.download_button("⬇ Download Results CSV", csv_out, "analyzed_reviews.csv", "text/csv")
    else:
        st.markdown("""
        <div class="upload-box">
            <div style="font-size:2rem; margin-bottom:0.5rem;">📄</div>
            <div>Drop your CSV here — needs a <strong>review</strong> column</div>
            <div style="margin-top:0.4rem; font-size:0.8rem;">Sample: <code>review, product_name, rating</code></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Generate Sample CSV"):
            sample = pd.DataFrame({
                "review": [
                    "Amazing product! Fast delivery and great quality. Will definitely buy again.",
                    "The item broke after two days. Very disappointed with the build quality.",
                    "It's okay. Nothing special but does the job. Packaging was a bit damaged.",
                    "Exceeded my expectations! The color is exactly as shown and fits perfectly.",
                    "Terrible customer service. The product is fine but returning it was a nightmare."
                ],
                "product_name": ["Wireless Earbuds","Phone Case","Desk Lamp","Running Shoes","Smart Watch"],
                "rating": [5, 1, 3, 5, 2]
            })
            st.download_button("⬇ Download Sample CSV", sample.to_csv(index=False), "sample_reviews.csv", "text/csv")
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#4b5563; font-size:0.82rem; padding:1rem 0 2rem 0;">
    🔍 <strong style="color:#a3e635;">ReviewIQ</strong> · 
    Designed & Built by 
    <strong style="color:#e5e7eb;">Gudi Indhu Reddy</strong> 
    
</div>
""", unsafe_allow_html=True)