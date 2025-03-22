# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from langchain.agents import initialize_agent, Tool
# from langchain.agents.agent_types import AgentType
# from langchain_community.llms import HuggingFaceHub
# from langchain_huggingface import HuggingFaceEndpoint

# from huggingface_hub import login
# from retrieval.faiss_retriever import CBPRetriever


# # 🔐 Login once with your HF token (or set env var)
# login("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")  # or use os.environ['HUGGINGFACEHUB_API_TOKEN']

# # ---- Tool: CBP Ruling Retriever ----
# retriever = CBPRetriever()

# def retrieve_rulings_tool(query: str) -> str:
#     results = retriever.search(query, k=3)
#     output = ""
#     for i, r in enumerate(results, 1):
#         output += f"[{i}] Title: {r['title']}\nDate: {r['date']}\nURL: {r['url']}\nText: {r['text'][:500]}...\n\n"
#     return output.strip()

# tools = [
#     Tool(
#         name="ruling_retriever",
#         func=retrieve_rulings_tool,
#         description="Use this to find past customs rulings and HTS codes relevant to the product."
#     )
# ]

# # ---- Load LLM from Hugging Face Inference API ----
# llm = HuggingFaceEndpoint(
#     repo_id="tiiuae/falcon-7b-instruct",
#     huggingfacehub_api_token="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",  # ✅ real token
#     temperature=0.3,                     # ✅ moved here
#     max_length=200                         # ✅ also moved here
# )


# # ---- Initialize ReAct Agent ----
# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     handle_parsing_errors=True  # ✅ this will retry if the output is malformed
# )


# def run_agent(query: str) -> str:
#     return agent.run(query)

# if __name__ == "__main__":
#     print("🔍 Ask TariffWhisperer a question:")
#     q = input("> ")
#     result = run_agent(q)
#     print("\n🧠 Answer:\n", result)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import login
from retrieval.faiss_retriever import CBPRetriever

# 🔐 Authenticate Hugging Face
login("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")

# 🧠 Load Model (Zephyr-7B Alpha via Inference API)
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-alpha",
    huggingfacehub_api_token="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",
    temperature=0.3,
    max_new_tokens=300
)

# 📚 Load FAISS-Based CBP Retriever
retriever = CBPRetriever()


# 🔍 Core Classification Logic
def ask_tariffwhisperer(query: str) -> str:
    if not query.strip():
        return "⚠️ Please enter a non-empty query."

    # Step 1: Retrieve Rulings
    results = retriever.search(query, k=3)
    if not results:
        return "⚠️ No relevant CBP rulings were found for this query."

    context = ""
    for i, r in enumerate(results, 1):
        context += (
            f"[{i}] {r['title']} ({r['date']})\n"
            f"URL: {r['url']}\n"
            f"{r['text'][:500].strip()}...\n\n"
        )

    # Step 2: Construct Prompt
    prompt = f"""
You are a customs classification AI assistant. Based on the product description and the retrieved CBP rulings, provide the best possible HTS code and justification.

Guidelines:
- Use relevant rulings provided below.
- Return the HTS code in 10-digit format if available.
- Summarize in 3-5 sentences.
- If you are unsure, recommend consulting a customs expert.

---

User Query:
{query}

Relevant CBP Rulings:
{context}

---

🧠 Your Answer:
"""

    # Step 3: Get Response
    response = llm.invoke(prompt).strip()

    return response


# 🧪 CLI Interface
if __name__ == "__main__":
    print("🔍 Ask TariffWhisperer a question:")
    try:
        user_input = input("> ")
        result = ask_tariffwhisperer(user_input)
        print("\n🧠 Answer:\n", result)
    except KeyboardInterrupt:
        print("\n👋 Exiting.")
