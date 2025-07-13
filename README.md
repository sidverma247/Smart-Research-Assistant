
# 🧠 Smart Research Assistant (Gemini API Version)

An AI-powered assistant that reads, summarizes, and intelligently interacts with research papers, legal docs, or manuals using the **Gemini 2.0 Flash API by Google**.

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
