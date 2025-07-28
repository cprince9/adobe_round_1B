## Project Structure
Round1B_Project/
├── input/
│   ├── persona.json           # Persona and task description
│   └── *.pdf                  # Input documents
├── output/
│   └── output.json            # Generated result (top 5 sections + summary)
├── utils/
│   ├── pdf_parser.py          # PDF text extraction
│   └── relevance_ranker.py    # Section ranking using MiniLM
├── main.py                    # Main pipeline script
├── requirements.txt           # Dependencies
└── README.md                  # This file


## Features

Extracts content from multiple PDFs
Matches content with persona intent
Uses lightweight MiniLM from sentence-transformers
Ranks and returns top 5 most relevant sections
Outputs both section metadata and subsection summaries

## Prepare Input Folder

Place all .pdf files in input/
Include persona.json

## how to run

pip install -r requirements.txt
python main.py
