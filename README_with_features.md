
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

📬 API Testing with Postman
Easily test and explore the Smart Research Assistant API using Postman.

🔧 Step-by-Step Instructions
1. 📥 Import Postman Collection
Download the collection file: Smart_Research_Assistant.postman_collection.json

Open Postman (desktop or web)

Click on Import → Upload Files → select the .json file

Once imported, you'll see the full suite of testable API endpoints

2. ▶️ Start the Flask API Server
Make sure your backend server is running on your local machine:

bash
Copy
Edit
python api.py
This should output:

nginx
Copy
Edit
Running on http://127.0.0.1:5000
All Postman requests will target this local server.

3. 📡 Available API Endpoints in Postman
Method	Endpoint	Description
GET	/	Health check (returns "API is running")
POST	/summarize	Summarizes the input text
POST	/ask	Answers questions based on provided text
POST	/generate-questions	Generates 3 MCQ-style questions
POST	/evaluate-answer	Evaluates user’s answer vs correct one
POST	/upload-file	Uploads a PDF or TXT file and extracts text
POST	/paste-text	Submits pasted raw text to the system
POST	/reset	Clears the current Q&A memory
GET	/export-csv	Exports all memory Q&A to a .csv file

4. 🧪 Example Flow: Ask & Export
Inside the Postman collection, you’ll find a pre-configured test folder:

mathematica
Copy
Edit
📁 Test Ask + Export CSV
   ├─ Ask Then Export (POST /ask)
   └─ Now Export CSV (GET /export-csv)
Use this to simulate a real conversation and export history.

5. ⚙️ Notes
For all JSON-based requests (/summarize, /ask, etc.), make sure headers include:

json
Copy
Edit
"Content-Type": "application/json"
For file upload (/upload-file), use form-data body and choose a valid .pdf or .txt file

The backend stores conversation history in memory, so restart will reset it unless persiste

## 📬 Contact

Feel free to connect if you have questions, ideas, or need help deploying this!

Built with ❤️ using Gemini + Streamlit By SIDDHARTH
