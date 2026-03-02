# FinAnalyzer — AI-Powered Financial Statement Analyzer

A comprehensive, interactive financial statement analysis tool built with Streamlit, Plotly, and Claude AI.

![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?logo=plotly&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-Powered-A855F7)

## Features

- **📊 Executive Dashboard** — KPI cards, revenue trends, financial health radar
- **📐 25+ Financial Ratios** — Profitability, liquidity, leverage, efficiency, cash flow, growth
- **📈 Interactive Charts** — Plotly-powered area, bar, line, radar, and pie charts
- **✦ AI Analysis** — Claude AI generates executive summaries, risk assessment, and investment ratings
- **✏️ Editable Data** — Full data input with auto-calculating derived fields

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub → Select this repo → Deploy!

### Enable AI Analysis (Optional)

Add your Anthropic API key in Streamlit Cloud:
- App Settings → Secrets → Add: `ANTHROPIC_API_KEY = "sk-ant-..."`

Without an API key, a demo analysis is shown.

## Built by Ayush • Powered by Claude AI
