import os
from dotenv import load_dotenv
import google.generativeai as genai

from core.groq_chat import ask_groq
from core.news_engine import get_stock_news
from core.ai_analyst import analyze_news_sentiment

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_ai(question, stock_data):

    company = stock_data.get("company", "Unknown Company")

    news = get_stock_news(company)

    if news:
        sentiment = analyze_news_sentiment(news)
    else:
        news = "No recent news available."
        sentiment = "Neutral"

    prompt = f"""
You are AlphaVision AI, an expert financial analyst.

Analyze the stock ONLY using the data below.

Company : {company}

Current Price : {stock_data.get("price", "N/A")}

PE Ratio : {stock_data.get("pe", "N/A")}

RSI : {stock_data.get("rsi", "N/A")}

Trend : {stock_data.get("trend", "N/A")}

Technical Score : {stock_data.get("technical_score", "N/A")}/20

Fundamental Score : {stock_data.get("fundamental_score", "N/A")}/70

Risk Level : {stock_data.get("risk_level", "Not Available")}

Risk Score : {stock_data.get("risk_score", "N/A")}/15

Valuation : {stock_data.get("valuation", "N/A")}

Valuation Score : {stock_data.get("valuation_score", "N/A")}/30

Overall Score : {stock_data.get("overall_score", "N/A")}/140

Question:
{question}

News Sentiment : {sentiment}

Recent News:
{news}

Rules:

1. Never guarantee profits.
2. Explain in simple English.
3. Mention strengths.
4. Mention risks.
5. Mention whether suitable for long-term or short-term.
6. Mention possible buy zone if appropriate.
7. Mention stop loss if appropriate.
8. Mention target if appropriate.
9. Keep answer under 250 words.

Format:

## Strengths

## Risks

## Buy Zone

## Stop Loss

## Target

## Suitable For

## Final Verdict
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:

        print(f"Gemini Error: {e}")
        print("Switching to Groq...")

        return ask_groq(prompt)