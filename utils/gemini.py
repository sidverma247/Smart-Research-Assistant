import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def gemini_chat(prompt: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY,
    }
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    try:
        res = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        res.raise_for_status()
        text = res.json()['candidates'][0]['content']['parts'][0]['text']
        return json.loads(text) if text.strip().startswith("{") else {"feedback": text}
    except Exception as e:
        return {"feedback": "Gemini error", "justification": str(e)}

gemini_call = gemini_chat


def call_gemini(prompt: str):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        res = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        res.raise_for_status()

        text = res.json()['candidates'][0]['content']['parts'][0]['text']

        # Try to parse structured JSON if Gemini returns it
        return json.loads(text) if text.strip().startswith("{") else {"feedback": text.strip()}

    except Exception as e:
        print("❌ Gemini API call failed:", str(e))
        return {
            "feedback": "Error: Could not connect to Gemini.",
            "justification": str(e)
        }