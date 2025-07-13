import os
import json
import re
import requests
import difflib
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def call_gemini(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def answer_question_with_memory(doc_text: str, user_question: str, chat_history: list):
    history_prompt = ""
    for entry in chat_history:
        history_prompt += f"Q: {entry['question']}\nA: {entry['answer']}\n"

    prompt = f"""
You are an AI assistant that answers questions using only the following document:

--- Document ---
{doc_text[:3000]}
----------------

Below is a conversation history between the user and assistant about the document. Use the conversation context to better understand follow-up questions.

Conversation History:
{history_prompt}

Now answer the user's latest question. Respond ONLY in this JSON format:
{{
  "answer": "<your answer>",
  "justification": "<quote or sentence from the document that supports your answer>"
}}

Q: {user_question}
A:
"""

    response = call_gemini(prompt).strip()

    try:
        if response.startswith('{') and response.endswith('}'):
            parsed = json.loads(response)
        else:
            match = re.search(r'{.*}', response, re.DOTALL)
            parsed = json.loads(match.group(0)) if match else {"answer": response, "justification": ""}

        answer = parsed.get("answer", "").strip()
        justification_text = parsed.get("justification", "").strip()

        if justification_text:
            justification = find_justification_with_position(doc_text, justification_text)
        else:
            justification = find_justification_with_position(doc_text, answer.split(".")[0][:100])

    except Exception:
        answer = response
        justification = find_justification_with_position(doc_text, answer.split(".")[0][:100])

    return {
        "answer": answer,
        "justification": justification["text"],
        "location": f"Paragraph {justification['paragraph']} | Line {justification['line']} | Sentence {justification['sentence']}"
    }


def generate_questions(doc_text: str):
    prompt = f"""
You are an assistant. Based on the document below, generate exactly 3 logic-based or comprehension-focused questions.

Reply in raw JSON format like:
[
  {{"question": "What is X?", "answer": "Y"}},
  {{"question": "Why is Z important?", "answer": "..."}},
  {{"question": "How does A affect B?", "answer": "..."}}
]

Document:
\"\"\"{doc_text[:3000]}\"\"\"
"""

    response = call_gemini(prompt)

    try:
        parsed = json.loads(response) if isinstance(response, str) else response
        if isinstance(parsed, list) and all("question" in q for q in parsed):
            return parsed
    except Exception:
        pass

    matches = re.findall(r'"question"\s*:\s*"([^"]+)"\s*,\s*"answer"\s*:\s*"([^"]+)"', response)
    if matches:
        return [{"question": q, "answer": a} for q, a in matches]

    return [{"question": "Unable to parse valid questions", "answer": "N/A"}]


def find_justification_with_position(doc_text: str, target_text: str):
    if not target_text:
        return {
            "text": "Could not extract justification from the document.",
            "paragraph": "N/A",
            "line": "N/A",
            "sentence": "N/A"
        }

    lines = doc_text.split('\n')
    paragraphs = [p.strip() for p in doc_text.split('\n\n') if p.strip()]
    sentences = re.split(r'(?<=[.!?]) +', doc_text)

    best_match = ""
    best_ratio = 0
    best_sent_idx = -1

    for i, sentence in enumerate(sentences):
        ratio = difflib.SequenceMatcher(None, sentence.lower(), target_text.lower()).ratio()
        if ratio > best_ratio and len(sentence.strip()) > 20:
            best_ratio = ratio
            best_match = sentence.strip()
            best_sent_idx = i

    if best_ratio > 0.3:
        para_idx = next((i for i, p in enumerate(paragraphs) if best_match[:10].lower() in p.lower()), -1)
        line_idx = next((i for i, l in enumerate(lines) if best_match[:10].lower() in l.lower()), -1)

        return {
            "text": best_match,
            "paragraph": para_idx + 1 if para_idx >= 0 else "N/A",
            "line": line_idx + 1 if line_idx >= 0 else "N/A",
            "sentence": best_sent_idx + 1
        }

    return {
        "text": "Could not extract justification from the document.",
        "paragraph": "N/A",
        "line": "N/A",
        "sentence": "N/A"
    }
