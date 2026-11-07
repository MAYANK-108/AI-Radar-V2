import os
import re
import time
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIStatusError
from scraper import fetch_articles

load_dotenv()
GROQ_API = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-20b"  

client = Groq(api_key=GROQ_API)

def parse_score(raw_content: str) -> int | None:
    if not raw_content:
        return None
    
    match = re.search(r'\b(10|[1-9])\b', raw_content.strip())
    if match:
        score = int(match.group(1))
        return max(1, min(score, 10)) 
    return None

def call_groq(prompt):
    response = client.chat.completions.create(
       model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=400
    )
    raw_output = response.choices[0].message.content
    return parse_score(raw_output)
    
def score_article(title: str, summary: str | None) -> int | None:
    clean_summary = summary if (summary and summary.strip()) else "No summary provided."
    
    prompt = f"""Evaluate the article below using a 1-10 scale.

SCORING MATRIX:
- Score 8-10: Net-new, actionable consumer AI tool or major functional product update live right now.
- Modifiers (Cap at 10): +2 if entirely Free (no card required), +1 if Open Source, -1 if Paid-Only (no free tier).
- Hard Cap Max 3: Corporate adoption news, academic papers/theory, opinions/policy, or future waitlists/announcements without a live tool interface.

OUTPUT SPECIFICATION:
Reply with ONLY a single raw digit from 1 to 10. No conversational filler, formatting, or prefixes.

Article Title: {title}
Summary: {clean_summary}"""

    try:
        return call_groq(prompt)

    except RateLimitError as e:
        print(f"⚠️ [Rate Limit] Hitting limits for '{title[:30]}...'. Retrying after 3 seconds.")
        time.sleep(3.0)

        try:
            return call_groq(prompt)
        except Exception:
            print("An Error has occured ,Try Again Later")
            return None

    except APIStatusError as e:
        print(f"❌ [Groq API Error Status {e.status_code}] Failure on '{title[:30]}...'. Details: {e.message}")
        return None
        
    except Exception as e:
        print(f"❌ [Unexpected System Error]: {str(e)}")
        return None


if __name__ == "__main__":
    print(f"🚀 Starting evaluation test utilizing model: {GROQ_MODEL}\n")
    
    test_articles = fetch_articles()

    for index, article in enumerate(test_articles, 1):
        print(f"Processing Article #{index}: '{article['title']}'")
        final_score = score_article(article['title'], article['summary'])
        print(f"📊 Extracted Final clamped Score: {final_score}")
        print("-" * 50)
