
from playwright.sync_api import sync_playwright

def parse_form_fields(url):
    fields = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Find the first form on the page
        form = page.query_selector("form")
        if not form:
            browser.close()
            return {"error": "No form found on the page."}

        inputs = form.query_selector_all("input, select, textarea")

        for input_el in inputs:
            tag = input_el.evaluate("e => e.tagName.toLowerCase()")
            name = input_el.get_attribute("name") or ""
            placeholder = input_el.get_attribute("placeholder") or ""
            input_type = input_el.get_attribute("type") or tag

            # Handle dropdowns
            if tag == "select":
                options = input_el.query_selector_all("option")
                option_values = [opt.inner_text().strip() for opt in options if opt.inner_text().strip()]
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

        browser.close()
        return fields
