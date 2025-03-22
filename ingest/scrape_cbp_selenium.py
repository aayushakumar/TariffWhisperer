import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

def init_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def scrape_cbp_rulings(term="cotton", max_rulings=30):
    driver = init_driver(headless=False)  # Keep visible for debugging
    driver.get("https://rulings.cbp.gov/search")
    
    print("[*] Loading search page...")
    results = []  # Initialize results here to avoid UnboundLocalError
    
    try:
        # Wait for the search input (increase timeout to 20s)
        search_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search Rulings']"))
        )
        print("[✓] Search input found")
        
        # Clear and input the search term
        search_input.clear()
        search_input.send_keys(term)
        print(f"[*] Entered search term: {term}")
        
        # Submit the search
        search_input.send_keys(Keys.ENTER)
        print("[*] Submitted search with Enter key")
        
        # Wait for results to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.search-result"))
        )
        print("[✓] Search results loaded")

        # Scroll to load more results
        scroll_pause = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while len(driver.find_elements(By.CSS_SELECTOR, "a.search-result")) < max_rulings:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("[*] No more results to load")
                break
            last_height = new_height

        ruling_cards = driver.find_elements(By.CSS_SELECTOR, "a.search-result")
        ruling_links = [card.get_attribute("href") for card in ruling_cards[:max_rulings] if card.get_attribute("href")]
        print(f"[✓] Found {len(ruling_links)} ruling links. Scraping content...")

        for url in ruling_links:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
                title = driver.find_element(By.TAG_NAME, "h1").text.strip()
                date = driver.find_element(By.CLASS_NAME, "ruling-date").text.strip()
                text = driver.find_element(By.CLASS_NAME, "ruling-text").text.strip()

                results.append({
                    "url": url,
                    "title": title,
                    "date": date,
                    "text": text
                })
                print(f"[✓] Scraped: {title}")
            except Exception as e:
                print(f"[!] Failed on {url}: {e}")
                continue

    except Exception as e:
        print(f"[!] Error during scraping: {e}")
        # Dump page source for debugging
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[!] Saved page source to debug_page.html for inspection")
    
    finally:
        driver.quit()
    
    return results

def save_results(data, path="data/cbp_rulings.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    print(f"[✓] Saved {len(data)} rulings to {path}")

if __name__ == "__main__":
    results = scrape_cbp_rulings(term="cotton", max_rulings=30)
    save_results(results)