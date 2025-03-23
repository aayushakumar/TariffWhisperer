import sys
import os
import time
import re
import random
from colorama import init, Fore, Style

# Initialize colorama
init()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.myagent import ask_tariffwhisperer

# Comprehensive test queries with expected HTS codes
test_queries = [
    # Basic apparel queries
    {"query": "What is the HTS code for cotton t-shirts?", "expected": "6109.10.00", "category": "Apparel"},
    {"query": "What is the classification for men's denim jeans?", "expected": "6203.42.40", "category": "Apparel"},
    {"query": "How are cotton blend shirts classified?", "expected": "6205.20.20", "category": "Apparel"},
    
    # Electronics queries
    {"query": "HTS code for wireless earbuds?", "expected": "8518.30.20", "category": "Electronics"},
    {"query": "What is the tariff classification for a smart watch?", "expected": "8517.62.00", "category": "Electronics"},
    {"query": "How are portable Bluetooth speakers classified?", "expected": "8518.22.00", "category": "Electronics"},
    
    # Plastic goods queries
    {"query": "How are plastic toys classified?", "expected": "9503.00.00", "category": "Plastics"},
    {"query": "What is the HTS code for plastic office supplies?", "expected": "3926.10.00", "category": "Plastics"},
    {"query": "Tariff classification for plastic food containers?", "expected": "3924.10.40", "category": "Plastics"},
    
    # Leather goods queries
    {"query": "What is the HTS code for leather wallets?", "expected": "4202.31.60", "category": "Leather"},
    {"query": "How are leather watch bands classified?", "expected": "9113.90.40", "category": "Leather"},
    
    # Edge cases and complex queries
    {"query": "What's the classification for a smart watch with leather band?", "expected": "8517.62.00", "category": "Complex"},
    {"query": "HTS code for wireless earbuds with leather case?", "expected": "8518.30.20", "category": "Complex"},
    {"query": "Classification for a portable speaker with leather exterior?", "expected": "8518.22.00", "category": "Complex"},
    
    # Stress tests
    {"query": "Is there a specific HTS code for men's cotton t-shirts with printed logos?", "expected": "6109.10.00", "category": "Stress"},
    {"query": "What about wireless earbuds with noise cancellation technology?", "expected": "8518.30.20", "category": "Stress"},
    {"query": "How would CBP classify a smartwatch that also measures blood oxygen?", "expected": "8517.62.00", "category": "Stress"},
    
    # Ambiguous queries
    {"query": "What is the tariff for wearable tech?", "expected": "8517.62.00", "category": "Ambiguous"},
    {"query": "Classification for containers?", "expected": None, "category": "Ambiguous"},
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
    
    # For None expected code (ambiguous queries), any valid code is acceptable
    if expected_code is None:
        return True, f"Returned a valid code for ambiguous query: {extracted_code}"
    
    # Remove dots for comparison
    extracted_clean = extracted_code.replace(".", "")
    expected_clean = expected_code.replace(".", "")
    
    # Check if the extracted code starts with the expected code
    # (allows for more specific codes)
    if extracted_clean.startswith(expected_clean) or expected_clean.startswith(extracted_clean):
        return True, f"Matched: {extracted_code} vs {expected_code}"
    
    return False, f"Mismatch: {extracted_code} vs {expected_code}"

def run_tests(test_set=None, shuffle=False, limit=None):
    """Run tests with options for subset, shuffling, and limiting"""
    if test_set is None:
        tests_to_run = test_queries
    else:
        tests_to_run = [t for t in test_queries if t["category"] == test_set]
    
    if shuffle:
        random.shuffle(tests_to_run)
    
    if limit and limit < len(tests_to_run):
        tests_to_run = tests_to_run[:limit]
    
    print(f"\n{Fore.CYAN}🧪 Running TariffWhisperer tests: {len(tests_to_run)} queries{Style.RESET_ALL}")
    if test_set:
        print(f"{Fore.CYAN}Category filter: {test_set}{Style.RESET_ALL}")
    
    results = {
        "success": 0,
        "failure": 0,
        "categories": {}
    }
    
    for idx, test in enumerate(tests_to_run, 1):
        query = test["query"]
        expected = test.get("expected")
        category = test.get("category", "Uncategorized")
        
        # Initialize category stats if not present
        if category not in results["categories"]:
            results["categories"][category] = {"success": 0, "failure": 0}
        
        print(f"\n{Fore.YELLOW}🧠 [{idx}/{len(tests_to_run)}] {category}: {query}{Style.RESET_ALL}")
        
        try:
            start_time = time.time()
            answer = ask_tariffwhisperer(query)
            elapsed = time.time() - start_time
            
            if not answer.strip():
                print(f"{Fore.RED}⚠️  No answer returned!{Style.RESET_ALL}")
                results["failure"] += 1
                results["categories"][category]["failure"] += 1
            else:
                correct, reason = evaluate_answer(answer, expected) if expected is not None else (True, "Ambiguous query")
                
                if correct:
                    print(f"{Fore.GREEN}✅ CORRECT: {reason} ({elapsed:.2f}s){Style.RESET_ALL}")
                    print(f"{Fore.WHITE}{answer.strip()[:200]}...{Style.RESET_ALL}\n")
                    results["success"] += 1
                    results["categories"][category]["success"] += 1
                else:
                    print(f"{Fore.RED}❌ INCORRECT: {reason} ({elapsed:.2f}s){Style.RESET_ALL}")
                    print(f"{Fore.WHITE}{answer.strip()[:200]}...{Style.RESET_ALL}\n")
                    results["failure"] += 1
                    results["categories"][category]["failure"] += 1
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Exception: {str(e)}{Style.RESET_ALL}")
            results["failure"] += 1
            results["categories"][category]["failure"] += 1
        
        time.sleep(2)  # Throttle between requests
    
    # Print summary statistics
    total = results["success"] + results["failure"]
    success_rate = (results["success"] / total * 100) if total > 0 else 0
    
    print(f"\n{Fore.CYAN}📊 Test Results Summary:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Successes: {results['success']}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ Failures: {results['failure']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🎯 Overall Success Rate: {success_rate:.1f}%{Style.RESET_ALL}")
    
    # Print category-specific results
    print(f"\n{Fore.CYAN}📋 Results by Category:{Style.RESET_ALL}")
    for category, stats in results["categories"].items():
        cat_total = stats["success"] + stats["failure"]
        cat_rate = (stats["success"] / cat_total * 100) if cat_total > 0 else 0
        print(f"{Fore.YELLOW}{category}: {stats['success']}/{cat_total} ({cat_rate:.1f}%){Style.RESET_ALL}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test the TariffWhisperer agent")
    parser.add_argument("--category", type=str, help="Filter tests by category")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle test order")
    parser.add_argument("--limit", type=int, help="Limit the number of tests to run")
    parser.add_argument("--list-categories", action="store_true", help="List all available test categories")
    
    args = parser.parse_args()
    
    if args.list_categories:
        categories = set(t.get("category", "Uncategorized") for t in test_queries)
        print(f"{Fore.CYAN}Available test categories:{Style.RESET_ALL}")
        for category in sorted(categories):
            count = sum(1 for t in test_queries if t.get("category") == category)
            print(f"{Fore.YELLOW}- {category} ({count} tests){Style.RESET_ALL}")
    else:
        run_tests(args.category, args.shuffle, args.limit)