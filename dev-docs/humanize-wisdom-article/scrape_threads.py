import asyncio
from playwright.async_api import async_playwright

async def scrape_threads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        page = await context.new_page()

        print("Loading page...")
        await page.goto("https://www.threads.com/@heuppity/post/DYNVenLGksR", wait_until="networkidle", timeout=30000)

        await page.wait_for_timeout(3000)

        # Scroll down to load comments
        for i in range(15):
            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(1000)

        # Try clicking "View more replies" or similar expand buttons
        for attempt in range(3):
            try:
                more_buttons = await page.query_selector_all('[role="button"]')
                for btn in more_buttons:
                    txt = await btn.inner_text()
                    if any(kw in txt.lower() for kw in ["view", "more", "replies", "reply", "show"]):
                        try:
                            await btn.click()
                            await page.wait_for_timeout(2000)
                        except:
                            pass
            except:
                pass

            # Scroll more
            for i in range(5):
                await page.evaluate("window.scrollBy(0, 800)")
                await page.wait_for_timeout(800)

        # Get all text content
        text = await page.evaluate("document.body.innerText")
        print("=== PAGE TEXT ===")
        print(text)
        print("=== END ===")

        # Get all links
        links = await page.evaluate("""
            Array.from(document.querySelectorAll('a')).map(a => ({
                text: a.innerText.trim(),
                href: a.href
            })).filter(l => l.text.length > 0)
        """)
        print("\n=== LINKS ===")
        for link in links:
            print(f"{link['text']} -> {link['href']}")

        await browser.close()

asyncio.run(scrape_threads())
