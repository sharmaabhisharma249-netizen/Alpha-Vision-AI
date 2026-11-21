from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


# ==========================================
# AI REPORT
# ==========================================

def generate_ai_report(report):

    prompt = f"""
You are an expert stock market analyst.

Analyze the following stock report and provide:

1. Company Overview
2. Technical Analysis
3. Fundamental Analysis
4. Risk Analysis
5. Valuation
6. Investment Recommendation
7. Long-term Outlook

Stock Report:

{report}
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"AI Error: {e}"


# ==========================================
# NEWS SENTIMENT
# ==========================================

def analyze_news_sentiment(news):

    if not news:

        return "Neutral"

    articles = ""

    for item in news:

        articles += f"""
Title: {item.get('title','')}

Publisher: {item.get('publisher','')}

"""

    prompt = f"""
You are a stock market analyst.

Read these news headlines.

Return ONLY ONE WORD.

Positive

Negative

Neutral

News:

{articles}
"""

    try:

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception:

        return "Neutral"