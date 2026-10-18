
import json
from datetime import datetime, timezone
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def extract_website(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            if response is None or not response.ok:
                raise RuntimeError("Website could not be loaded.")

            data = {
                "url": page.url,
                "title": page.title(),
                "headings": page.locator("h1, h2").all_inner_texts(),
                "content": page.locator("body").inner_text()[:5000],
                "extracted_at": datetime.now(timezone.utc).isoformat()
            }

            return data

        finally:
            browser.close()


if __name__ == "__main__":
    result = extract_website("https://example.com")

    with open("research_data.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("Research extracted successfully!")
    print("Saved to research_data.json")
