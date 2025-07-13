
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

## 🧠 Architecture Flow

1. **User uploads a document** → parsed by `parser.py`
2. **Summary** generated via `summarizer.py` calling Gemini
3. **Ask Anything** mode → uses `qa_engine.py` with memory and justification
4. **Challenge Me** mode → generates 3 logic-based questions
5. **Evaluation** → `evaluator.py` checks answers using Gemini API
6. **Snippets** found by `snippet_extractor.py` to highlight exact justification

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourname/smart-research-assistant.git
cd smart-research-assistant
```

---

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Activate it:

- On macOS/Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Get Your Gemini API Key

- Visit: https://makersuite.google.com/app/apikey  
- Log in with your Google account  
- Click **"Create API Key"**  
- Copy the key

---

### 5. Create a `.env` File in the Project Root

Create a new file named `.env` and add this line:

```env
GEMINI_API_KEY=your_google_api_key_here
```

🔐 **Important**: Do **not** upload your `.env` file to GitHub!

---

### ▶️ Run the App

```bash
streamlit run app.py
```

Then open your browser and visit:  
👉 http://localhost:8501

---

## 📮 Postman API Support

This repo includes:

```
gemini-api.postman_collection.json
```

### How to Use:

1. Import into Postman
2. Create a new environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: your actual Gemini API key
3. Click "Send" to test `generateContent` endpoint

### Example Request Body

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Explain what generative AI is in one paragraph."
        }
      ]
    }
  ]
}
```

---

### ✅ Output Sample

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Generative AI is a form of artificial intelligence that creates new content..."
          }
        ]
      }
    }
  ]
}
```

---

## 📬 Contact

Feel free to connect if you have questions, ideas, or need help deploying this!

Built with ❤️ using Gemini + Streamlit
