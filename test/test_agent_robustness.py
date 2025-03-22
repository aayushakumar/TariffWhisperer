import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.myagent import ask_tariffwhisperer

# 🔍 Define test queries
test_queries = [
    # ✅ Basic
    "What is the HTS code for leather wallets?",
    "What is the HTS classification for steel pipes?",
    "HTS code for wireless earbuds?",
    "How are plastic toys classified?",

    # 🤖 Reworded
    "I’m importing t-shirts made of cotton — which HTS code applies?",
    "What tariff classification would a stainless steel pipe fall under?",
    "Looking for the correct HTS code to import Bluetooth earphones.",

    # 📦 Edge cases
    "HTS code for robotic dog toys?",
    "What’s the classification for hybrid material shoes (rubber and fabric)?",
    "I need to ship medical latex gloves — what code do I use?",

    # 🧠 Vague
    "What’s the code for those popular tech accessories?",
    "I have a box of mixed electronics — how do I classify that?"
]

print("🧪 Running robustness tests on TariffWhisperer...\n")

for idx, query in enumerate(test_queries, 1):
    print(f"🧠 [{idx}] Q: {query}")
    try:
        answer = ask_tariffwhisperer(query)
        if not answer.strip():
            print("⚠️  No answer returned!\n")
        elif "USA-USA" in answer or len(answer) > 1000:
            print("⚠️  Possibly malformed or overly verbose output:\n", answer[:200], "...\n")
        else:
            print("✅ Answer:\n", answer.strip(), "\n")
    except Exception as e:
        print("❌ Exception occurred:", e, "\n")

    time.sleep(2)  # ⏱️ throttle between requests

print("✅ Test run complete.")
