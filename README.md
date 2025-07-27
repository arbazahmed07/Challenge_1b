
---

## ✅ `Q2/approach_explanation.md` (Round 1B)
Paste this file inside `Adobe/Q2/`:

```markdown
# 🧠 Round 1B – Persona-Based PDF Intelligence

## 🎯 Goal
Extract and rank relevant sections from 3–10 PDFs based on:
- A user persona
- A job-to-be-done

---

## 🧠 How It Works

### 1. PDF Parsing
- Each PDF is parsed using `PyMuPDF`
- Paragraphs are extracted with document name + page number

### 2. Semantic Ranking
- We load an offline model (`all-MiniLM-L6-v2`) via SentenceTransformers
- Paragraphs and persona query are embedded
- Cosine similarity is used to rank relevance

### 3. Result
We return:
- Top 5 relevant sections (document, page, rank)
- Full text of each selected section

---

## 📦 Stack Used
- Python 3.10
- PyMuPDF
- Sentence-Transformers (offline)
- Scikit-learn

---

## 📂 Output Format

```json
{
  "metadata": {
    "persona": "Student",
    "job_to_be_done": "Understand organic chemistry",
    "documents": ["doc1.pdf", "doc2.pdf"],
    "timestamp": "2025-07-27T14:00:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page": 3,
      "section_title": "Reaction Kinetics",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page": 3,
      "refined_text": "This section explains the rate of reaction with examples..."
    }
  ]
}
