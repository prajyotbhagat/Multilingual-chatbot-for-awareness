import json
import asyncio
from playwright.async_api import async_playwright

SCHEME_URLS = [
    "https://www.myscheme.gov.in/schemes/pmkisan",
    "https://www.myscheme.gov.in/schemes/pmjay",
    "https://www.myscheme.gov.in/schemes/pmayg",
    "https://www.myscheme.gov.in/schemes/pmuy",
    "https://www.myscheme.gov.in/schemes/mgnrega",
    "https://www.myscheme.gov.in/schemes/ssa",
    "https://www.myscheme.gov.in/schemes/eshram",
    "https://www.myscheme.gov.in/schemes/pmsvanidhi"
]

async def extract_scheme_data(page, url):
    print(f"Scraping {url}...")
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Give it a second to render
        await page.wait_for_timeout(2000)

        # Basic extraction - we try to get the title and the main textual content
        # myscheme.gov.in usually has the content in a main container
        
        title_element = await page.query_selector('h1')
        title = await title_element.inner_text() if title_element else url.split('/')[-1]

        # Extract all text from the main body. 
        # For a robust RAG, getting the full text of the tabs is best.
        # We'll just grab the innerText of the body and clean it up.
        body_text = await page.evaluate('document.body.innerText')
        
        return {
            "url": url,
            "title": title.strip(),
            "content": body_text[:10000] # Limit to avoid massive payloads, but 10k chars is plenty
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for url in SCHEME_URLS:
            data = await extract_scheme_data(page, url)
            if data:
                results.append(data)
                
        await browser.close()

    with open("data/schemes.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully scraped {len(results)} schemes.")

if __name__ == "__main__":
    asyncio.run(main())
