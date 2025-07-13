
# 🧠 Smart Research Assistant

A Streamlit + Flask-powered intelligent assistant that helps you summarize, ask questions, generate challenges, evaluate answers, and retain memory from documents or custom text input. Built with Gemini API for internship submission with Postman API support.

---

## 🚀 Features

- 📄 Upload PDF/TXT files or ✍️ paste custom text
- 🔍 Summarize documents
- ❓ Ask questions with context retention (memory)
- 🧠 Justified answers with snippet location
- 🏆 Challenge mode (auto-generated MCQs with feedback)
- 📤 Export memory to CSV
- ✅ Postman API support (collection included)
- 💾 Persistent Q&A memory stored as JSON

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-research-assistant.git
cd smart-research-assistant
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file in the root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

### 5. Run the API Server

```bash
python api.py
```

---

## 🌐 Postman API Usage

1. Open [Postman](https://www.postman.com/)
2. Import the included collection: `Smart_Research_Assistant.postman_collection.json`
3. Test endpoints like:
   - `POST /summarize`
   - `POST /ask`
   - `POST /generate-questions`
   - `POST /evaluate-answer`
   - `POST /reset`
   - `POST /upload-file`
   - `POST /paste-text`
   - `GET /export-csv`

Example for `POST /ask`:

```json
{
  "doc_text": "AI is a branch of computer science.",
  "question": "What is AI?"
}
```

---

## 🧠 Memory Handling

- All Q&A pairs are stored in `memory.json`
- Memory persists across sessions
- Export Q&A to `qa_history.csv`
- Clear memory using the reset button or `/reset` endpoint

---

## 📂 Project Structure

```
smart-research-assistant/
│
├── api.py                    # Flask API server
├── app.py                    # Streamlit interface
├── memory.json               # Q&A memory (auto-saved)
├── requirements.txt          # Python dependencies
├── README.md                 # Project info and usage
│
├── backend/
│   ├── qa_engine.py
│   ├── summarizer.py
│   └── evaluator.py
│
├── utils/
│   └── parser.py
│
└── Smart_Research_Assistant.postman_collection.json
```

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more info.
