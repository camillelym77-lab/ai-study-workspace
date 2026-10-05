# AI Study Workspace

A lightweight AI/NLP product prototype that turns fragmented course notes into structured study context.

**Built as a sample project for Product & Technology internship applications.**

## 1. Problem

University students often study from fragmented materials: lecture slides, PDFs, notebooks, recordings, and personal notes. Before they can actually revise, they spend significant time reorganising information manually.

The product question is:

> How might we reduce the time students spend organising course material while keeping AI outputs editable, transparent, and useful for action?

## 2. Target User

Primary user:
- University / postgraduate students
- Multiple modules with mixed technical and business content
- Need fast review, prioritisation and follow-up questions

## 3. Core Workflow

1. Add or upload course notes
2. Extract key topics
3. Rank important sentences / key points
4. Generate actionable study tasks
5. Let the user edit the workspace
6. Ask questions and retrieve the most relevant source passages

## 4. AI / NLP Role

This MVP intentionally uses lightweight local NLP rather than a hosted LLM API.

Current AI/NLP components:
- **TF-IDF topic extraction**
- **Sentence relevance ranking**
- **Retrieval-based question answering**
- **Editable generated study tasks**

Why start this way:
- No API key required
- Easy to test locally
- Keeps the MVP small and explainable
- Separates the product workflow from the model layer

## 5. Prototype

The prototype is built with:
- Python
- Streamlit
- scikit-learn

Run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 6. What I Would Test With Users

I would test with 3–5 students and observe:

- Which outputs are actually useful?
- Are extracted topics too broad or too narrow?
- Do users edit the generated tasks?
- What information do they distrust?
- When do they still go back to the original source?
- Which workflow feels faster than using a generic chatbot?

Success signals:
- Reduced manual organisation time
- Higher completion of generated study tasks
- Fewer repeated searches through source notes
- Positive usefulness ratings

## 7. Next Iteration

The next version would add:

- PDF / PPT ingestion
- LLM-generated summaries and concept explanations
- RAG for grounded answers
- Source citations
- Long-term course workspace / memory
- Deadline-aware study planning
- Evaluation for hallucination, relevance, latency and task success

## 8. Product Decisions

### Why not fully automate the study plan?
Users should remain in control. AI output is editable because a study plan depends on exam format, deadlines, confidence level, and personal priorities.

### Why retrieval before generation?
For education, source-grounded answers matter. Retrieval makes it possible to show the user where an answer came from before adding an LLM generation layer.

### Why build a small MVP first?
The goal is to validate whether structured context and task generation solve a real workflow problem before investing in a more complex AI stack.

## 9. Product Story

**Problem → User → Workflow → AI Role → Prototype → Feedback → Iteration**

This project demonstrates:
- Product discovery
- AI-native workflow thinking
- Rapid prototyping
- User-centred design
- AI evaluation thinking
- Iterative product development

---

Created by **Yimeng Li**  
M.Sc. Smart Industries & Digital Transformation, National University of Singapore
