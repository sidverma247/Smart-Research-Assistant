import streamlit as st
import json
import pandas as pd
import re

from utils.parser import parse_document
from backend.summarizer import summarize
from backend.qa_engine import answer_question_with_memory, generate_questions
from backend.evaluator import evaluate_answers


# Load memory if available
try:
    if "chat_history" not in st.session_state:
        with open("memory.json", "r") as f:
            st.session_state.chat_history = json.load(f)
except FileNotFoundError:
    st.session_state.chat_history = []

st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    .summary-box {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        color: #0d47a1;
        font-size: 1.1rem;
    }
    .justification-box {
        background-color: #fff3e0;
        border-left: 6px solid #ffb300;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        font-style: italic;
        color: #bf360c;
    }
    .feedback-box {
        background-color: #e8f5e9;
        border-left: 6px solid #43a047;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #1b5e20;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Smart Research Assistant")
st.markdown("Summarize, question, challenge and explore documents with memory & feedback.")

# --- Upload / Paste Tabs ---
tab1, tab2 = st.tabs(["📂 Upload File", "✍️ Paste Text"])
doc_text = None
show_summary = False

with tab1:
    uploaded_file = st.file_uploader("Upload a PDF or TXT", type=["pdf", "txt"])
    if uploaded_file:
        try:
            doc_text = parse_document(uploaded_file)
            if "doc_text" not in st.session_state or st.session_state.doc_text != doc_text:
                st.session_state.chat_history = []
            st.success("✅ File uploaded!")
            if st.button("🔄 Summarize Document"):
                st.session_state.doc_text = doc_text
                show_summary = True
        except Exception as e:
            st.error(f"❌ Could not parse file: {e}")
            st.stop()

with tab2:
    pasted_text = st.text_area("Paste your text here", height=250)
    if pasted_text.strip():
        doc_text = pasted_text.strip()
        if "doc_text" not in st.session_state or st.session_state.doc_text != doc_text:
            st.session_state.chat_history = []
        st.success("✅ Text received!")
        if st.button("🔄 Summarize Text"):
            st.session_state.doc_text = doc_text
            show_summary = True

# --- Shared Logic ---
if "doc_text" in st.session_state and st.session_state.doc_text:
    doc_text = st.session_state.doc_text
    st.markdown("---")

    if show_summary:
        st.subheader("📌 Summary")
        with st.spinner("Generating summary..."):
            try:
                summary = summarize(doc_text)
                st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error generating summary: {e}")
                st.stop()

    mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"], horizontal=True)

    # --- Ask Anything Mode ---
    if mode == "Ask Anything":
        user_question = st.text_input("Ask a question based on the document")

        if user_question:
            try:
                response = answer_question_with_memory(doc_text, user_question, st.session_state.chat_history)

                # Trim justification to first sentence
                raw_just = response["justification"]
                sentences = re.split(r'(?<=[.!?]) +', raw_just.strip())
                short_just = sentences[0] if sentences else raw_just

                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": response["answer"],
                    "justification": short_just,
                    "location": response["location"]
                })

                st.markdown("### ✅ Answer")
                st.write(response["answer"])
                st.markdown(
                    f'<div class="justification-box"><strong>Justification ({response["location"]}):</strong><br>{short_just}</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"❌ Answering failed: {e}")

        # Memory view
        if "chat_history" in st.session_state and st.session_state.chat_history:
            with st.expander("🧠 View Q&A Memory History"):
                if st.button("🗑️ Clear Memory History"):
                    st.session_state.clear()  # Wipe everything from session (memory + doc_text + state flags)
                    st.rerun()


                st.markdown("### 🧠 Memory (Q&A History):")
                for i, mem in enumerate(st.session_state.chat_history):
                    st.markdown(f"**{i+1}. Q:** {mem['question']}")
                    st.markdown(f"**   A:** {mem['answer']}")
                    st.markdown(f"**   Justification ({mem.get('location', 'N/A')}):** {mem.get('justification', 'N/A')}")

                    # Highlight short justification inside paragraph
                    highlight = mem.get("justification", "")
                    short_highlight = highlight.strip().split('.')[0] + '.' if '.' in highlight else highlight[:200] + '...'
                    paragraphs = doc_text.split("\n\n")
                    target_para = next((p for p in paragraphs if highlight.strip() in p), "")
                    if short_highlight in target_para:
                        highlighted_para = target_para.replace(
                            short_highlight,
                            f"<mark style='background-color: #ffff99'>{short_highlight}</mark>"
                        )
                    else:
                        highlighted_para = "<i>Could not highlight justification in context.</i>"

                    st.markdown(f"📄 **Context for Q{i+1}:**", unsafe_allow_html=True)
                    st.markdown(highlighted_para, unsafe_allow_html=True)

    # --- Challenge Me Mode ---
    elif mode == "Challenge Me":
        if "challenge_index" not in st.session_state:
            st.session_state.challenge_index = 0
            st.session_state.challenge_questions = []
            st.session_state.challenge_complete = False
            st.session_state.answer_submitted = False

        st.subheader("🧪 Challenge Me")

        if st.button("🔁 Reset Challenge"):
            st.session_state.challenge_index = 0
            st.session_state.challenge_questions = []
            st.session_state.challenge_complete = False
            st.session_state.answer_submitted = False

        if st.button("Generate Questions"):
            try:
                questions = generate_questions(doc_text)
                if questions[0].get("question") == "Unable to parse valid questions":
                    st.warning("⚠️ Gemini returned an unstructured response.")
                else:
                    st.session_state.challenge_questions = questions
                    st.session_state.challenge_index = 0
                    st.session_state.challenge_complete = False
                    st.session_state.answer_submitted = False
            except Exception as e:
                st.error(f"❌ Error generating questions: {e}")

        if st.session_state.challenge_questions and not st.session_state.challenge_complete:
            i = st.session_state.challenge_index
            question = st.session_state.challenge_questions[i]

            st.markdown(f"### Q{i+1}: {question['question']}")
            user_input = st.text_input("Your Answer", key=f"user_input_{i}")

            if not st.session_state.answer_submitted:
                if st.button("Submit Answer", key=f"submit_{i}"):
                    try:
                        result = evaluate_answers(question["question"], user_input, question["answer"], doc_text)
                        st.session_state.feedback = result["feedback"]
                        st.session_state.justification = result["justification"]
                        st.session_state.answer_submitted = True
                    except Exception as e:
                        st.error(f"❌ Evaluation error: {e}")

            if st.session_state.answer_submitted:
                st.markdown(f'<div class="feedback-box"><strong>Feedback:</strong> {st.session_state.feedback}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="justification-box"><strong>Justification:</strong> {st.session_state.justification}</div>', unsafe_allow_html=True)

                if i + 1 < len(st.session_state.challenge_questions):
                    if st.button("Next Question", key=f"next_{i}"):
                        st.session_state.challenge_index += 1
                        st.session_state.answer_submitted = False
                        st.rerun()
                else:
                    st.success("🎉 You completed all questions!")
                    st.session_state.challenge_complete = True

# Save memory to disk
if "chat_history" in st.session_state and st.session_state.chat_history:
    with open("memory.json", "w") as f:
        json.dump(st.session_state.chat_history, f)

# Export Q&A
if "chat_history" in st.session_state and st.session_state.chat_history:
    if st.button("📤 Export as CSV"):
        pd.DataFrame(st.session_state.chat_history).to_csv("qa_history.csv", index=False)
        st.success("Saved as qa_history.csv")

    

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#999;'>© 2025 Smart Research Assistant | Made By SIDDHARTH VERMA</p>", unsafe_allow_html=True)
