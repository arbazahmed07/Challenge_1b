import os
import shutil
import json

def setup_collection(collection_number):
    """Copy files from a collection to the input directory for testing"""
    
    # Define collection mappings
    collections = {
        1: {
            "dir": "Collection 1",
            "persona": "Travel Planner",
            "job": "Plan a trip of 4 days for a group of 10 college friends."
        },
        2: {
            "dir": "Collection 2", 
            "persona": "HR professional",
            "job": "Create and manage fillable forms for onboarding and compliance."
        },
        3: {
            "dir": "Collection 3",
            "persona": "Food Contractor", 
            "job": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
        }
    }
    
    if collection_number not in collections:
        print(f"Invalid collection number. Choose from: {list(collections.keys())}")
        return
    
    collection = collections[collection_number]
    source_dir = collection["dir"]
    
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Collection directory not found: {source_dir}")
        return
    
    # Create input directory if it doesn't exist
    os.makedirs("input", exist_ok=True)
    
    # Clear existing files in input directory
    for file in os.listdir("input"):
        file_path = os.path.join("input", file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Copy PDF files
    pdf_count = 0
    for file in os.listdir(source_dir):
        if file.endswith(".pdf"):
            source_path = os.path.join(source_dir, file)
            dest_path = os.path.join("input", file)
            shutil.copy2(source_path, dest_path)
            pdf_count += 1
            print(f"Copied: {file}")
    
    # Create persona.json
    persona_data = {
        "persona": collection["persona"],
        "job_to_be_done": collection["job"]
    }
    
    with open("input/persona.json", "w", encoding="utf-8") as f:
        json.dump(persona_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSetup complete!")
    print(f"- Copied {pdf_count} PDF files from {source_dir}")
    print(f"- Created persona.json for {collection['persona']}")
    print(f"- Ready to run: python process_documents.py")

def list_collections():
    """List available collections"""
    print("Available collections:")
    for i in range(1, 4):
        collection_dir = f"Collection {i}"
        if os.path.exists(collection_dir):
            pdf_files = [f for f in os.listdir(collection_dir) if f.endswith(".pdf")]
            print(f"  {i}: {collection_dir} ({len(pdf_files)} PDF files)")
        else:
            print(f"  {i}: {collection_dir} (not found)")

if __name__ == "__main__":
    print("Collection Setup Tool")
    print("=" * 20)
    
    list_collections()
    
    try:
        choice = int(input("\nEnter collection number (1-3): "))
        setup_collection(choice)
    except ValueError:
        print("Please enter a valid number (1-3)")
    except KeyboardInterrupt:
        print("\nSetup cancelled")
