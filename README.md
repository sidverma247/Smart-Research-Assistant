# 🧠 Smart Research Assistant (Gemini API Version)

An AI-powered assistant that reads, summarizes, and intelligently interacts with research papers, legal docs, or manuals using the **Gemini 2.0 Flash API by Google**.

---

## 🚀 Features

- 📄 Upload PDF or TXT documents
- ✨ Generate automatic summaries (≤150 words)
- ❓ Ask contextual questions with memory
- 🧠 Challenge yourself with AI-generated questions
- 💬 Justified answers with highlighted source snippets
- 📤 Export Q&A to CSV or PDF
- 🌐 Gemini API integration via HTTP (no LangChain/OpenAI)

---

## 📁 Folder Structure

smart-research-assistant/
├── app.py # Streamlit app UI
├── api.py # Optional FastAPI endpoint layer
├── backend/
│ ├── qa_engine.py # Gemini-powered Q&A logic
│ ├── summarizer.py # Gemini summarization logic
│ ├── evaluator.py # Evaluates your answers via Gemini
├── utils/
│ ├── parser.py # PDF/TXT parser
│ ├── gemini.py # Gemini API HTTP integration
│ ├── snippet_extractor.py # Extracts supporting document snippets
├── memory.json # Stores Q&A memory
├── requirements.txt # Dependencies
├── .env # Your Gemini API key
├── gemini-api.postman_collection.json ✅ Postman support
└── README.md

## Setup Instructions

1. Clone the Repo : https://github.com/sidverma247/Smart-Research-Assistant

