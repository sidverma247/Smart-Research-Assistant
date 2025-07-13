from flask import Flask, request, jsonify
from backend.summarizer import summarize
from backend.qa_engine import answer_question_with_memory, generate_questions
from backend.evaluator import evaluate_answers

app = Flask(__name__)

memory = []

@app.route("/")
def home():
    return "✅ Smart Research Assistant API is running!"

@app.route("/summarize", methods=["POST"])
def summarize_text():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "Text is required"}), 400
        summary = summarize(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()
        doc_text = data.get("doc_text", "")
        question = data.get("question", "")
        if not doc_text.strip() or not question.strip():
            return jsonify({"error": "Both doc_text and question are required"}), 400
        response = answer_question_with_memory(doc_text, question, memory)
        memory.append({
            "question": question,
            "answer": response["answer"],
            "justification": response["justification"],
            "location": response["location"]
        })
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/reset", methods=["POST"])
def reset_memory():
    global memory
    memory = []
    return jsonify({"message": "Memory cleared."})

@app.route("/generate-questions", methods=["POST"])
def generate_questions_api():
    try:
        data = request.get_json()
        doc_text = data.get("text", "")
        if not doc_text.strip():
            return jsonify({"error": "Document text required"}), 400
        questions = generate_questions(doc_text)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer_api():
    try:
        data = request.get_json()
        question = data.get("question", "")
        user_answer = data.get("user_answer", "")
        correct_answer = data.get("correct_answer", "")
        doc_text = data.get("doc_text", "")

        if not all([question, user_answer, correct_answer, doc_text]):
            return jsonify({"error": "All fields are required"}), 400

        result = evaluate_answers(question, user_answer, correct_answer, doc_text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
