import os
import json
from datetime import datetime
from utils import load_pdfs, embed_and_rank_sections

# Use local paths for development, Docker paths for container
if os.path.exists("./input"):
    INPUT_DIR = "./input"
    OUTPUT_DIR = "./output"
elif os.path.exists("/app/input"):
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
else:
    # Create local directories if they don't exist
    INPUT_DIR = "./input"
    OUTPUT_DIR = "./output"
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    persona_path = os.path.join(INPUT_DIR, "persona.json")
    
    # Check if persona.json exists
    if not os.path.exists(persona_path):
        print(f"Error: persona.json not found at {persona_path}")
        print(f"Please ensure persona.json exists in the input directory: {INPUT_DIR}")
        print("\nTip: Run 'python setup_test.py' to copy files from a collection for testing")
        return
    
    with open(persona_path, "r", encoding="utf-8") as f:
        persona_data = json.load(f)

    documents = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    
    if not documents:
        print(f"Warning: No PDF files found in {INPUT_DIR}")
        print("Please add PDF files to the input directory")
        print("\nTip: Run 'python setup_test.py' to copy files from a collection for testing")
        return
    
    print(f"Found {len(documents)} PDF files:")
    for doc in documents:
        print(f"  - {doc}")
    
    document_paths = [os.path.join(INPUT_DIR, doc) for doc in documents]

    print(f"\nProcessing with persona: {persona_data.get('persona', 'Unknown')}")
    print(f"Job to be done: {persona_data.get('job_to_be_done', 'Unknown')}")
    
    sections, refined = embed_and_rank_sections(document_paths, persona_data)

    if not sections:
        print("No relevant sections found. Check your PDF files and persona configuration.")
        return

    output = {
        "metadata": {
            "documents": documents,
            "persona": persona_data["persona"],
            "job_to_be_done": persona_data["job_to_be_done"],
            "timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": sections,
        "subsection_analysis": refined
    }

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_path = os.path.join(OUTPUT_DIR, "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing complete!")
    print(f"- Found {len(sections)} top relevant sections")
    print(f"- Output saved to: {output_path}")

if __name__ == "__main__":
    main()
