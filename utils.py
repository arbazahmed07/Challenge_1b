import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def load_pdfs(pdf_paths):
    all_sections = []
    for path in pdf_paths:
        # Normalize path for Windows
        normalized_path = os.path.normpath(path)
        if not os.path.exists(normalized_path):
            print(f"Warning: PDF file not found: {normalized_path}")
            continue
            
        try:
            doc = fitz.open(normalized_path)
            for i, page in enumerate(doc, start=1):
                text = page.get_text()
                for para in text.split("\n\n"):
                    clean_para = para.strip()
                    if 30 < len(clean_para) < 600:  # Ignore too short/long
                        all_sections.append({
                            "document": os.path.basename(normalized_path),
                            "page": i,
                            "text": clean_para
                        })
            doc.close()
        except Exception as e:
            print(f"Error processing {normalized_path}: {e}")
            continue
    
    print(f"Loaded {len(all_sections)} sections from {len([p for p in pdf_paths if os.path.exists(os.path.normpath(p))])} PDF files")
    return all_sections

def embed_and_rank_sections(pdf_paths, persona):
    sections = load_pdfs(pdf_paths)
    
    if not sections:
        print("No sections found to process")
        return [], []

    # Handle both direct string values and nested objects
    persona_str = persona.get('persona', '') if isinstance(persona, dict) else str(persona)
    job_str = persona.get('job_to_be_done', '') if isinstance(persona, dict) else ''
    
    query = f"{persona_str} needs to: {job_str}"
    print(f"Query: {query}")
    
    query_embedding = model.encode([query])[0]
    section_embeddings = model.encode([s["text"] for s in sections])
    sims = cosine_similarity([query_embedding], section_embeddings)[0]

    top_indices = sims.argsort()[-5:][::-1]  # Top 5 matches

    extracted_sections = []
    refined = []

    for rank, idx in enumerate(top_indices, start=1):
        s = sections[idx]
        extracted_sections.append({
            "document": s["document"],
            "page": s["page"],
            "section_title": s["text"][:50] + "..." if len(s["text"]) > 50 else s["text"],
            "importance_rank": rank
        })
        refined.append({
            "document": s["document"],
            "page": s["page"],
            "refined_text": s["text"]
        })

    return extracted_sections, refined
