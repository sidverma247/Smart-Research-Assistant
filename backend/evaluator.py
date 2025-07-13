from utils.gemini import call_gemini
from utils.snippet_extractor import extract_snippet
import json

def evaluate_answers(question, user_answer, correct_answer, doc_text):
    prompt = f"""
You are a helpful evaluator.

Evaluate the user's answer by comparing it to the correct answer, using the document as reference.

Return your response ONLY in the following JSON format:
{{
  "feedback": "<brief, clear feedback: Correct / Partially Correct / Incorrect, with reasoning>",
  "justification": "<a justification pulled from or grounded in the document>"
}}

Question: {question}
Correct Answer: {correct_answer}
User Answer: {user_answer}
Document:
\"\"\"
{doc_text}
\"\"\"
"""

    response = call_gemini(prompt)

    try:
        result = json.loads(response) if isinstance(response, str) else response
        feedback = result.get("feedback", "").strip()
        justification = result.get("justification", "").strip()

        if not justification:
            justification = extract_snippet(doc_text, correct_answer)

    except Exception:
        feedback = response.strip() if isinstance(response, str) else "No feedback."
        justification = extract_snippet(doc_text, correct_answer)

    return {
        "feedback": feedback or "No feedback.",
        "justification": justification or "No justification."
    }
