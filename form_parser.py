
from playwright.async_api import async_playwright

async def parse_form_fields(url):
    fields = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        form = await page.query_selector("form")
        if not form:
            await browser.close()
            return {"error": "No form found on the page."}

        inputs = await form.query_selector_all("input, select, textarea")
        for input_el in inputs:
            tag = await input_el.evaluate("e => e.tagName.toLowerCase()")
            name = await input_el.get_attribute("name") or ""
            placeholder = await input_el.get_attribute("placeholder") or ""
            input_type = await input_el.get_attribute("type") or tag

            if tag == "select":
                options = await input_el.query_selector_all("option")
                option_values = [await opt.inner_text() for opt in options if await opt.inner_text()]
                fields.append({
                    "name": name,
                    "type": "dropdown",
                    "label": placeholder or name,
                    "options": option_values
                })
            else:
                fields.append({
                    "name": name,
                    "type": input_type,
                    "label": placeholder or name
                })

        await browser.close()
        return fields
