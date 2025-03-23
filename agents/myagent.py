# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# # from langchain_huggingface import HuggingFaceEndpoint
# # from huggingface_hub import login
# # from retrieval.faiss_retriever import CBPRetriever
# # import re
# # from langchain.schema import SystemMessage, HumanMessage
# # from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

# # # 🔐 Authenticate Hugging Face
# # login("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")

# # # 🧠 Load Model (Mistral or Zephyr via Inference API)
# # llm = HuggingFaceEndpoint(
# #     repo_id="mistralai/Mistral-7B-Instruct-v0.2",  # Using Mistral instead of Zephyr
# #     huggingfacehub_api_token="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",
# #     temperature=0.2,  # Lower temperature for more precise answers
# #     max_new_tokens=400
# # )

# # # 📚 Load FAISS-Based CBP Retriever
# # retriever = CBPRetriever()

# # # Helper function to format the HTS code
# # def format_hts_code(hts_code):
# #     # Clean up the HTS code to ensure correct format
# #     hts_code = re.sub(r'[^\d.]', '', hts_code)  # Remove non-digit/period chars
# #     if not hts_code:
# #         return None
# #     return hts_code

# # # 🔍 Core Classification Logic
# # def ask_tariffwhisperer(query: str) -> str:
# #     if not query.strip():
# #         return "⚠️ Please enter a non-empty query."

# #     # Step 1: Retrieve Rulings
# #     results = retriever.search(query, k=3)
# #     if not results:
# #         return "⚠️ No relevant CBP rulings were found for this query."

# #     context = ""
# #     for i, r in enumerate(results, 1):
# #         context += (
# #             f"[{i}] {r['title']} ({r['date']})\n"
# #             f"URL: {r['url']}\n"
# #             f"{r['text'][:500].strip()}...\n\n"
# #         )

# #     # Step 2: Construct Prompt with explicit structure
# #     system_template = """You are a customs classification AI assistant specialized in HTS codes. Your task is to determine the correct 10-digit HTS code for products based on CBP rulings.

# # IMPORTANT INSTRUCTIONS:
# # 1. Analyze the provided CBP rulings carefully
# # 2. Identify the most relevant ruling that matches the product description
# # 3. Extract or derive the correct 10-digit HTS code
# # 4. Provide a short, clear justification (3-5 sentences maximum)
# # 5. Format your response in exactly this structure:
# #    - HTS Code: [10-digit code]
# #    - Justification: [3-5 sentence explanation]
# #    - Reference: [relevant ruling number]

# # If you cannot determine a code with high confidence, state this clearly and recommend consulting a customs expert."""

# #     human_template = """Product Query: {query}

# # Relevant CBP Rulings:
# # {context}

# # Provide the HTS code and justification:"""

# #     chat_prompt = ChatPromptTemplate.from_messages([
# #         SystemMessagePromptTemplate.from_template(system_template),
# #         HumanMessagePromptTemplate.from_template(human_template)
# #     ])

# #     formatted_prompt = chat_prompt.format_prompt(
# #         query=query,
# #         context=context
# #     )

# #     # Step 3: Get Response
# #     response = llm.invoke(formatted_prompt.to_messages())
    
# #     # Format the response
# #     answer = response.content.strip()
    
# #     # Ensure the answer doesn't exceed 800 characters
# #     if len(answer) > 800:
# #         # Try to find the structured parts and truncate the rest
# #         hts_match = re.search(r'HTS Code:\s*([0-9\.]+)', answer)
# #         justification_match = re.search(r'Justification:\s*(.*?)(?=Reference:|$)', answer, re.DOTALL)
# #         reference_match = re.search(r'Reference:\s*(.*?)(?=\n|$)', answer)
        
# #         if hts_match and justification_match:
# #             truncated_answer = f"HTS Code: {hts_match.group(1)}\n\n"
# #             truncated_answer += f"Justification: {justification_match.group(1).strip()[:300]}...\n\n"
# #             if reference_match:
# #                 truncated_answer += f"Reference: {reference_match.group(1)}"
# #             answer = truncated_answer

# #     return answer


# # # 🧪 CLI Interface
# # if __name__ == "__main__":
# #     print("🔍 Ask TariffWhisperer a question:")
# #     try:
# #         user_input = input("> ")
# #         result = ask_tariffwhisperer(user_input)
# #         print("\n🧠 Answer:\n", result)
# #     except KeyboardInterrupt:
# #         print("\n👋 Exiting.")
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)

# import os
# import re
# from langchain_huggingface import HuggingFaceEndpoint
# from huggingface_hub import login
# from langchain.schema import SystemMessage, HumanMessage
# from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

# class TariffWhisperer:
#     def __init__(self):
#         # Authenticate with Hugging Face
#         self.api_token = "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"
#         # login(self.api_token)
        
#         # Initialize LLM
#         self.llm = HuggingFaceEndpoint(
#             repo_id="mistralai/Mistral-7B-Instruct-v0.2",
#             huggingfacehub_api_token=self.api_token,
#             temperature=0.2,
#             max_new_tokens=400
#         )
        
#         # Initialize retriever (assuming you have CBPRetriever implementation)
#         from retrieval.faiss_retriever import CBPRetriever
#         self.retriever = CBPRetriever()
    
#     def query(self, question):
#         if not question.strip():
#             return "⚠️ Please enter a non-empty query."
#         # Step 1: Retrieve Rulings
#         results = self.retriever.search(question, k=3)
#         if not results:
#             return "⚠️ No relevant CBP rulings were found for this query."
#         context = ""
#         for i, r in enumerate(results, 1):
#             context += (
#                 f"[{i}] {r['title']} ({r['date']})\n"
#                 f"URL: {r['url']}\n"
#                 f"{r['text'][:500].strip()}...\n\n"
#             )
#         # Step 2: Construct Prompt with explicit structure
#         system_template = """You are a customs classification AI assistant specialized in HTS codes. Your task is to determine the correct 10-digit HTS code for products based on CBP rulings.
# IMPORTANT INSTRUCTIONS:
# 1. Analyze the provided CBP rulings carefully
# 2. Identify the most relevant ruling that matches the product description
# 3. Extract or derive the correct 10-digit HTS code
# 4. Provide a short, clear justification (3-5 sentences maximum)
# 5. Format your response in exactly this structure:
#    - HTS Code: [10-digit code]
#    - Justification: [3-5 sentence explanation]
#    - Reference: [relevant ruling number]
# If you cannot determine a code with high confidence, state this clearly and recommend consulting a customs expert."""
#         human_template = """Product Query: {query}
# Relevant CBP Rulings:
# {context}
# Provide the HTS code and justification:"""
#         chat_prompt = ChatPromptTemplate.from_messages([
#             SystemMessagePromptTemplate.from_template(system_template),
#             HumanMessagePromptTemplate.from_template(human_template)
#         ])
#         formatted_prompt = chat_prompt.format_prompt(
#             query=question,
#             context=context
#         )
#         # Step 3: Get Response
#         response = self.llm.invoke(formatted_prompt.to_messages())
        
#         # Handle different response types from LangChain
#         if hasattr(response, 'content'):
#             # If response is an object with content attribute
#             answer = response.content.strip()
#         else:
#             # If response is a string directly
#             answer = str(response).strip()
        
#         # Ensure the answer doesn't exceed 800 characters
#         if len(answer) > 800:
#             # Try to find the structured parts and truncate the rest
#             hts_match = re.search(r'HTS Code:\s*([0-9\.]+)', answer)
#             justification_match = re.search(r'Justification:\s*(.*?)(?=Reference:|$)', answer, re.DOTALL)
#             reference_match = re.search(r'Reference:\s*(.*?)(?=\n|$)', answer)
            
#             if hts_match and justification_match:
#                 truncated_answer = f"HTS Code: {hts_match.group(1)}\n\n"
#                 truncated_answer += f"Justification: {justification_match.group(1).strip()[:300]}...\n\n"
#                 if reference_match:
#                     truncated_answer += f"Reference: {reference_match.group(1)}"
#                 answer = truncated_answer
#         return answer

# # Helper function for the unit test
# def ask_tariffwhisperer(query):
#     agent = TariffWhisperer()
#     return agent.query(query)




import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import re
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

class TariffWhisperer:
    def __init__(self):
        self.api_token = "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"

        self.llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            huggingfacehub_api_token=self.api_token,
            temperature=0.2,
            max_new_tokens=400
        )

        from retrieval.faiss_retriever import CBPRetriever
        self.retriever = CBPRetriever()
    
    def query(self, question):
        if not question.strip():
            return "⚠️ Please enter a non-empty query."

        results = self.retriever.search(question, k=3)
        if not results:
            return "⚠️ No relevant CBP rulings were found for this query."

        context = ""
        for i, r in enumerate(results, 1):
            context += (
                f"[{i}] {r['title']} ({r['date']})\n"
                f"URL: {r['url']}\n"
                f"{r['text'][:500].strip()}...\n\n"
            )

        system_template = """You are a customs classification AI assistant specialized in HTS codes. Your task is to determine the correct 10-digit HTS code for products based on CBP rulings.

IMPORTANT INSTRUCTIONS:
1. Analyze the provided CBP rulings carefully
2. Identify the most relevant ruling that matches the product description
3. Extract or derive the correct 10-digit HTS code
4. Provide a short, clear justification (3-5 sentences maximum)
5. Format your response in exactly this structure:
   - HTS Code: [10-digit code]
   - Justification: [3-5 sentence explanation]
   - Reference: [relevant ruling number]

If you cannot determine a code with high confidence, state this clearly and recommend consulting a customs expert."""

        human_template = """Product Query: {query}

Relevant CBP Rulings:
{context}

Provide the HTS code and justification:"""

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ])

        formatted_prompt = chat_prompt.format_prompt(
            query=question,
            context=context
        )

        try:
            response = self.llm.invoke(formatted_prompt.to_messages())
            answer = response.content.strip() if hasattr(response, "content") else str(response).strip()
        except Exception as e:
            return f"❌ Error during LLM inference: {e}"

        if len(answer) > 800:
            hts_match = re.search(r'HTS Code:\s*([0-9\.]+)', answer)
            justification_match = re.search(r'Justification:\s*(.*?)(?=Reference:|$)', answer, re.DOTALL)
            reference_match = re.search(r'Reference:\s*(.*?)(?=\n|$)', answer)

            if hts_match and justification_match:
                answer = f"HTS Code: {hts_match.group(1)}\n\n"
                answer += f"Justification: {justification_match.group(1).strip()[:300]}...\n\n"
                if reference_match:
                    answer += f"Reference: {reference_match.group(1)}"

        return answer

# 🔍 CLI or test interface
def ask_tariffwhisperer(query):
    agent = TariffWhisperer()
    return agent.query(query)

if __name__ == "__main__":
    print("🔍 Ask TariffWhisperer a question:")
    try:
        user_input = input("> ")
        result = ask_tariffwhisperer(user_input)
        print("\n🧠 Answer:\n", result)
    except KeyboardInterrupt:
        print("\n👋 Exiting.")
