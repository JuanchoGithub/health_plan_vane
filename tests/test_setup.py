from playwright.sync_api import sync_playwright

def test_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")
        assert "Streamlit" in page.title(), "The application did not load correctly."
        browser.close()

if __name__ == "__main__":
    test_setup()