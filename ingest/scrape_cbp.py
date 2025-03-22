import requests
import json
import os

def fetch_cbp_rulings(query="cotton", max_results=50, page=1):
    """
    Fetches rulings from CBP CROSS API for a given query.
    """
    url = f"https://rulings.cbp.gov/api/rulings/search?q={query}&size={max_results}&page={page}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    print(f"[+] Requesting rulings for: '{query}' (page {page})")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[!] Failed with status code: {response.status_code}")
        return []

    json_data = response.json()
    return json_data.get("rulings", [])


def simplify_ruling(r):
    """
    Extracts and formats important fields from raw API response.
    """
    return {
        "url": f"https://rulings.cbp.gov/rulings/{r.get('slug', '')}",
        "title": r.get("title", "").strip(),
        "date": r.get("dateIssued", ""),
        "text": r.get("summary", "").strip(),
        "hts_no": r.get("htsNo", ""),
        "document_number": r.get("documentNumber", "")
    }


def save_rulings(rulings, path="data/cbp_rulings.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rulings:
            f.write(json.dumps(r) + "\n")
    print(f"[✓] Saved {len(rulings)} rulings to {path}")


if __name__ == "__main__":
    query = "cotton"
    max_results = 50
    page = 1

    raw_rulings = fetch_cbp_rulings(query=query, max_results=max_results, page=page)
    simplified = [simplify_ruling(r) for r in raw_rulings if r.get("summary")]
    save_rulings(simplified)
