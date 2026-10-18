
import json
from datetime import datetime, timezone
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://playwright.dev/python/"
]


def collect_research(urls):
    results = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            for url in urls:
                print(f"\nResearching: {url}")

                page = browser.new_page()

                try:
                    parsed = urlparse(url)
                    if parsed.scheme not in ("http", "https"):
                        raise ValueError("Unsupported URL scheme")

                    response = page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000
                    )

                    if response is None or not response.ok:
                        raise RuntimeError("Failed to load webpage")

                    data = {
                        "url": page.url,
                        "title": page.title(),
                        "headings": page.locator(
                            "h1, h2"
                        ).all_inner_texts()[:20],
                        "content": page.locator(
                            "body"
                        ).inner_text()[:5000],
                        "timestamp": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "status": "success"
                    }

                    results.append(data)
                    print("Extraction successful!")

                except Exception as error:
                    results.append({
                        "url": url,
                        "status": "failed",
                        "error": str(error)
                    })
                    print(f"Error: {error}")

                finally:
                    page.close()

        finally:
            browser.close()

    return results


if __name__ == "__main__":
    research = collect_research(URLS)

    with open(
        "multi_research_data.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            research,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResearch saved to multi_research_data.json")
