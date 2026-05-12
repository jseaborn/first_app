import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def scrape_threads():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--ignore-certificate-errors",
                "--ignore-certificate-errors-spki-list",
                "--disable-features=IsolateOrigins,site-per-process",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            ignore_https_errors=True,
            bypass_csp=True,
        )
        stealth = Stealth()
        await stealth.apply_stealth_async(context)
        page = await context.new_page()

        url = "https://www.threads.com/@heuppity/post/DYNVenLGksR"
        print(f"Navigating to {url}...")

        try:
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            print(f"Status: {resp.status if resp else 'None'}")
            print(f"URL after nav: {page.url}")
        except Exception as e:
            print(f"Navigation error: {e}")

        await page.wait_for_timeout(3000)

        # Check what we got
        title = await page.title()
        print(f"Title: {title}")

        body_text = await page.evaluate("document.body.innerText.substring(0, 500)")
        print(f"Body preview: {body_text}")

        # If we see "allowlist", try going through the embed endpoint
        if "allowlist" in body_text.lower() or len(body_text.strip()) < 50:
            print("\nDirect access blocked. Trying embed endpoint...")

            embed_url = f"https://www.threads.com/embed/post/DYNVenLGksR"
            try:
                resp = await page.goto(embed_url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(2000)
                body_text = await page.evaluate("document.body.innerText.substring(0, 500)")
                print(f"Embed body: {body_text}")
            except Exception as e:
                print(f"Embed error: {e}")

            # Try via Google cache
            print("\nTrying Google cache...")
            cache_url = "https://webcache.googleusercontent.com/search?q=cache:https://www.threads.com/@heuppity/post/DYNVenLGksR"
            try:
                resp = await page.goto(cache_url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(2000)
                body_text = await page.evaluate("document.body.innerText.substring(0, 1000)")
                print(f"Cache body: {body_text}")
            except Exception as e:
                print(f"Cache error: {e}")

            # Try via archive.today
            print("\nTrying archive.today...")
            archive_url = "https://archive.ph/newest/https://www.threads.com/@heuppity/post/DYNVenLGksR"
            try:
                resp = await page.goto(archive_url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(2000)
                body_text = await page.evaluate("document.body.innerText.substring(0, 1000)")
                print(f"Archive body: {body_text}")
            except Exception as e:
                print(f"Archive error: {e}")

        # Full page text if we got anything useful
        full_text = await page.evaluate("document.body.innerText")
        if len(full_text.strip()) > 100 and "allowlist" not in full_text.lower():
            print("\n=== FULL PAGE TEXT ===")
            print(full_text)
            print("=== END ===")

        await browser.close()

asyncio.run(scrape_threads())
