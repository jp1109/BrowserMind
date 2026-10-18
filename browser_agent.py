
from playwright.sync_api import sync_playwright

def browse_website(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print(f"Opening: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)

            print(f"Page Title: {page.title()}")

            heading = page.locator("h1").first
            if heading.count() > 0:
                print(f"Main Heading: {heading.inner_text()}")

            text = page.locator("body").inner_text()
            print(f"\nPage Content:\n{text[:1000]}")

        finally:
            browser.close()


if __name__ == "__main__":
    browse_website("https://example.com")
