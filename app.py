import re
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Study Workspace", page_icon="📚", layout="wide")

st.title("📚 AI Study Workspace")
st.caption("A lightweight AI/NLP product prototype for turning fragmented course notes into structured study context.")

st.info(
    "Prototype scope: local NLP + retrieval. No external API is required. "
    "The architecture is intentionally designed so an LLM/RAG layer can be added later."
)

with st.sidebar:
    st.header("Product Goal")
    st.write(
        "Help students spend less time manually reorganising fragmented notes "
        "and more time understanding, reviewing and acting on what matters."
    )
    st.header("Current Demo")
    st.markdown(
        "- Topic extraction\n"
        "- Key-point ranking\n"
        "- Study-task generation\n"
        "- Retrieval-based Q&A\n"
        "- Editable workspace"
    )

default_text = """Large Language Models (LLMs) generate text by predicting tokens based on context.
Prompt engineering structures instructions, context, constraints and output format.
Retrieval-Augmented Generation (RAG) retrieves relevant external information before generation.
Embeddings represent text as vectors so semantically similar content can be compared.
AI agents combine a model with tools, memory or state, and a workflow to complete tasks.
Evaluation for AI products should consider quality, task success, latency, cost and user feedback.
"""

tab1, tab2, tab3 = st.tabs(["1. Add Notes", "2. Study Workspace", "3. Ask Workspace"])

with tab1:
    st.subheader("Add course material")
    uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded is not None:
        notes = uploaded.read().decode("utf-8", errors="ignore")
    else:
        notes = st.text_area(
            "Or paste your notes here",
            value=default_text,
            height=280
        )
    st.session_state["notes"] = notes

def split_sentences(text):
    parts = re.split(r'(?<=[.!?。！？])\s+|\n+', text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 20]

def extract_topics(text, top_n=8):
    sentences = split_sentences(text)
    if not sentences:
        return []
    try:
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=120)
        matrix = vec.fit_transform(sentences)
        scores = matrix.sum(axis=0).A1
        features = vec.get_feature_names_out()
        ranked = sorted(zip(features, scores), key=lambda x: x[1], reverse=True)
        seen = set()
        topics = []
        for term, score in ranked:
            clean = term.strip()
            if clean not in seen and len(clean) > 2:
                seen.add(clean)
                topics.append(clean)
            if len(topics) >= top_n:
                break
        return topics
    except ValueError:
        return []

def rank_key_points(text, top_n=6):
    sentences = split_sentences(text)

    if not sentences:
        return []

    if len(sentences) <= top_n:
        return sentences

    vec = TfidfVectorizer(stop_words="english")
    matrix = vec.fit_transform(sentences)

    centroid = np.asarray(matrix.mean(axis=0))
    scores = cosine_similarity(matrix, centroid).ravel()

    ranked_idx = scores.argsort()[::-1][:top_n]
    ranked_idx = sorted(ranked_idx)

    return [sentences[i] for i in ranked_idx]

def generate_tasks(topics, key_points):
    tasks = []
    if topics:
        tasks.append(f"Review and define the main concepts: {', '.join(topics[:4])}.")
    if key_points:
        tasks.append("Turn the top 3 key points into flashcards using your own wording.")
        tasks.append("Write one example or use case for each major concept.")
        tasks.append("Identify one concept you cannot explain confidently and revisit the source notes.")
        tasks.append("Create 3 self-test questions and answer them without looking at the notes.")
    return tasks[:5]

with tab2:
    st.subheader("Structured study context")
    notes = st.session_state.get("notes", default_text)
    topics = extract_topics(notes)
    key_points = rank_key_points(notes)
    tasks = generate_tasks(topics, key_points)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Concepts / Topics")
        if topics:
            st.write("\n".join([f"- {t}" for t in topics]))
        else:
            st.write("Add more notes to extract topics.")

        st.markdown("### Key Points")
        if key_points:
            st.write("\n".join([f"- {p}" for p in key_points]))
        else:
            st.write("Add more notes to rank key points.")

    with c2:
        st.markdown("### Suggested Study Tasks")
        if tasks:
            st.write("\n".join([f"- {t}" for t in tasks]))
        else:
            st.write("Add more notes to generate tasks.")

        st.markdown("### Editable Workspace")
        editable = st.text_area(
            "Refine the AI/NLP output into your own study plan",
            value="\n".join(tasks),
            height=220
        )
        st.download_button(
            "Download study plan",
            data=editable,
            file_name="study_plan.txt",
            mime="text/plain"
        )

with tab3:
    st.subheader("Ask questions about your notes")
    notes = st.session_state.get("notes", default_text)
    question = st.text_input("Question", placeholder="e.g. What is the difference between RAG and an AI agent?")

    if question:
        sentences = split_sentences(notes)
        if not sentences:
            st.warning("Please add more notes first.")
        else:
            corpus = sentences + [question]
            vec = TfidfVectorizer(stop_words="english")
            matrix = vec.fit_transform(corpus)
            scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
            top_idx = scores.argsort()[::-1][:3]
            st.markdown("### Most relevant passages")
            for i in top_idx:
                if scores[i] > 0:
                    st.write(f"- {sentences[i]}")
            st.caption(
                "Current prototype retrieves the most relevant passages rather than generating a new answer. "
                "A next iteration would add an LLM on top of this retrieval layer."
            )

st.divider()
st.markdown("### Product thinking behind the prototype")
st.markdown(
    """
**Problem** → students spend time reorganising fragmented notes before they can study.  
**User** → university students managing multiple technical and business modules.  
**Workflow** → add notes → structure context → identify concepts/key points → generate tasks → ask the workspace.  
**AI role** → reduce manual organisation and surface relevant context; keep outputs editable and traceable.  
**Prototype** → this Streamlit app.  
**Feedback plan** → test with 3–5 students on usefulness, trust, editing behaviour and missing features.  
**Iteration** → add PDF ingestion, source citations, LLM summarisation and RAG-based answering.
"""
)
