import os
import json
from datetime import datetime
from utils.pdf_parser import extract_sections_from_pdf
from utils.relevance_ranker import rank_sections

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def load_input():
    with open(os.path.join(INPUT_DIR, "persona.json")) as f:
        meta = json.load(f)
    persona_text = f"{meta['persona']['role']}: {meta['job_to_be_done']['task']}"
    pdfs = [doc["filename"] for doc in meta["documents"]]
    return persona_text, pdfs, meta

def summarize_title(text):
    # Use first sentence or short preview as title
    lines = text.strip().split('\n')
    for line in lines:
        if len(line.strip()) > 15:
            return line.strip()[:100]  # limit to 100 characters
    return lines[0].strip() if lines else "Untitled Section"

def main():
    persona_text, pdf_files, meta = load_input()
    all_sections = []
    for pdf_file in pdf_files:
        path = os.path.join(INPUT_DIR, pdf_file)
        if not os.path.exists(path):
            print(f"Skipping missing file: {pdf_file}")
            continue
        sections = extract_sections_from_pdf(path)
        for sec in sections:
            sec["document"] = pdf_file
        all_sections.extend(sections)

    # Rank sections using MiniLM
    top_sections = rank_sections(all_sections, persona_text)

    # Build output JSON
    output = {
        "metadata": {
            "input_documents": pdf_files,
            "persona": meta["persona"]["role"],
            "job_to_be_done": meta["job_to_be_done"]["task"],
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    for i, sec in enumerate(top_sections):
        title = summarize_title(sec["text"])
        output["extracted_sections"].append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "section_title": title,
            "importance_rank": i + 1
        })
        output["sub_section_analysis"].append({
            "document": sec["document"],
            "page_number": sec["page_number"],
            "refined_text": sec["text"][:500]  # preview first 500 characters
        })

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "output.json"), "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
