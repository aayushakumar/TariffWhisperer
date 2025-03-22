@echo off
echo Creating TariffWhisperer directory structure...

:: Create main directory


:: Create subdirectories
mkdir agents data embeddings ingest retrieval utils
mkdir data\faiss_index

:: Create files in root directory
echo. > app.py
echo gradio > requirements.txt
echo pandas >> requirements.txt
echo faiss-cpu >> requirements.txt
echo requests >> requirements.txt
echo # TariffWhisperer > README.md
echo A tool for processing tariff-related data >> README.md

:: Create files in agents/
echo. > agents\react_agent.py

:: Create files in data/
echo. > data\hts_data.csv
echo. > data\cbp_rulings.jsonl

:: Create files in embeddings/
echo. > embeddings\embedder.py

:: Create files in ingest/
echo. > ingest\scrape_cbp.py
echo. > ingest\load_hts.py

:: Create files in retrieval/
echo. > retrieval\retriever.py

:: Create files in utils/
echo. > utils\logger.py

echo Directory structure and files created successfully!
pause