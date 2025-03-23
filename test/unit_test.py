import sys
import os
import time
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.myagent import ask_tariffwhisperer

# 🔍 Improved test queries with expected HTS codes for validation
test_queries = [
    # ✅ Basic queries with expected codes
    {"query": "What is the HTS code for leather wallets?", "expected": "4202.31.60"},
    {"query": "What is the HTS classification for cotton t-shirts?", "expected": "6109.10.00"},
    {"query": "HTS code for wireless earbuds?", "expected": "8518.30.20"},
    {"query": "How are plastic toys classified?", "expected": "9503.00.00"},
]

def extract_hts_code(answer):
    """Extract HTS code from response"""
    match = re.search(r'HTS Code:\s*([0-9\.]+)', answer)
    if match:
        return match.group(1)
    return None

def evaluate_answer(answer, expected_code):
    """Evaluate if the answer contains the expected code"""
    if not answer.strip():
        return False, "Empty answer"
    
    extracted_code = extract_hts_code(answer)
    if not extracted_code:
        return False, "No HTS code found"
    
    # Remove dots for comparison
    extracted_clean = extracted_code.replace(".", "")
    expected_clean = expected_code.replace(".", "")
    
    # Check if the extracted code starts with the expected code 
    # (allows for more specific codes)
    if extracted_clean.startswith(expected_clean) or expected_clean.startswith(extracted_clean):
        return True, f"Matched: {extracted_code} vs {expected_code}"
    
    return False, f"Mismatch: {extracted_code} vs {expected_code}"

print("🧪 Running robustness tests on TariffWhisperer...\n")

results = {
    "success": 0,
    "failure": 0
}

for idx, test in enumerate(test_queries, 1):
    query = test["query"]
    expected = test.get("expected")
    
    print(f"🧠 [{idx}] Q: {query}")
    try:
        answer = ask_tariffwhisperer(query)
        if not answer.strip():
            print("⚠️  No answer returned!\n")
            results["failure"] += 1
        else:
            correct, reason = evaluate_answer(answer, expected) if expected else (True, "No expected code")
            if correct:
                print(f"✅ Answer (CORRECT): {reason}\n{answer.strip()[:200]}...\n")
                results["success"] += 1
            else:
                print(f"❌ Answer (INCORRECT): {reason}\n{answer.strip()[:200]}...\n")
                results["failure"] += 1
    except Exception as e:
        print(f"❌ Exception occurred: {e}\n")
        results["failure"] += 1

    time.sleep(2)  # ⏱️ throttle between requests

print(f"✅ Test run complete: {results['success']} successes, {results['failure']} failures")
print(f"Success rate: {results['success'] / (results['success'] + results['failure']) * 100:.1f}%")