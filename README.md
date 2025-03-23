
# 🧠 TariffWhisperer

TariffWhisperer is an AI-powered HTS (Harmonized Tariff Schedule) classification assistant that retrieves and analyzes U.S. Customs and Border Protection (CBP) rulings to assign accurate 10-digit HTS codes to product descriptions.

Built using **LangChain**, **FAISS**, **Hugging Face Transformers**, and **Gradio** for a smooth UI experience.

---

## 🚀 Features

- ✅ AI classification based on real CBP rulings
- 🔎 FAISS vector search with semantic retrieval
- 📄 Custom prompt templates optimized for HTS formatting
- 🧠 Uses `mistralai/Mistral-7B-Instruct` via Hugging Face Inference API
- 📊 Returns:
  - **HTS Code**
  - **Justification**
  - **Reference ruling**

---

## 📦 Project Structure

```
TariffWhisperer/
├── app.py                      # Gradio UI entry point
├── agents/
|     └──myagent.py                 # Core AI agent (retriever + LLM + prompt)
├── retrieval/
│   └── faiss_retriever.py     # FAISS-based semantic search
├── embed_and_store.py         # Embeds rulings and builds FAISS index
├── data/
│   └── cbp_rulings.jsonl      # Rulings (real or synthetic)
│   └── faiss_index/           # FAISS index + metadata
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Create environment

```bash
conda create -n tariffwhisperer python=3.10
conda activate tariffwhisperer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare your data

Run this to build the FAISS index from `cbp_rulings.jsonl`:

```bash
python embed_and_store.py
```

---

## 🧪 Run the App

```bash
python app.py
```

The Gradio UI will open in your browser. Enter a product description and get your HTS code instantly.

---

## 🛠 Technologies Used

- [LangChain](https://www.langchain.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [HuggingFace Transformers](https://huggingface.co/)
- [Gradio](https://www.gradio.app/)

---

## 🧠 Example Queries

- "100% cotton men's short sleeve t-shirt"
- "Wireless Bluetooth earbuds with charging case"
- "Plastic toy for toddlers shaped like animals"
- "Smart watch with fitness tracking features"
- "Office folders made of polypropylene"

---

## 📌 Notes

- Uses Hugging Face Inference API with Mistral-7B (swap to Zephyr or Llama 3 as needed)
- Handles long CBP rulings with chunking + embedding
- Rulings can be scraped or generated synthetically (fallback)

---

## 👤 Author

**Aayush** – Cybersecurity Researcher | AI Builder  
[GitHub](https://github.com/your-handle) | [LinkedIn](https://linkedin.com/in/your-handle)

---

## 📜 License

MIT License
```
