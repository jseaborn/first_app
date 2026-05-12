"""
Threads post scraper -- run locally (not in a sandboxed environment).

Usage:
    pip install playwright playwright-stealth
    playwright install chromium
    python scrape_threads_local.py
"""
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth


TARGET_URL = "https://www.threads.com/@heuppity/post/DYNVenLGksR"


async def scrape_threads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        stealth = Stealth()
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        await stealth.apply_stealth_async(context)
        page = await context.new_page()

        print(f"Loading {TARGET_URL} ...")
        await page.goto(TARGET_URL, wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(3000)

        # Scroll and expand replies
        for _ in range(20):
            await page.evaluate("window.scrollBy(0, 600)")
            await page.wait_for_timeout(800)

            # Click any "Show replies" / "View more" buttons
            for btn in await page.query_selector_all('[role="button"]'):
                try:
                    txt = (await btn.inner_text()).lower()
                    if any(kw in txt for kw in ("view", "more", "repl", "show")):
                        await btn.click()
                        await page.wait_for_timeout(1500)
                except Exception:
                    pass

        # Scroll back up and down once more to trigger lazy loads
        await page.evaluate("window.scrollTo(0, 0)")
        await page.wait_for_timeout(1000)
        for _ in range(25):
            await page.evaluate("window.scrollBy(0, 600)")
            await page.wait_for_timeout(600)

        text = await page.evaluate("document.body.innerText")
        links = await page.evaluate("""
            Array.from(document.querySelectorAll('a'))
                .map(a => ({ text: a.innerText.trim(), href: a.href }))
                .filter(l => l.text.length > 0)
        """)

        print("\n=== POST + COMMENTS ===")
        print(text)
        print("\n=== LINKS ===")
        for lnk in links:
            print(f"  {lnk['text']}  ->  {lnk['href']}")

        # Save raw output
        with open("threads_output.txt", "w") as f:
            f.write(text)
            f.write("\n\n=== LINKS ===\n")
            for lnk in links:
                f.write(f"  {lnk['text']}  ->  {lnk['href']}\n")

        print("\nSaved to threads_output.txt")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(scrape_threads())
