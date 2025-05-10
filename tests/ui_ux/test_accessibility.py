# Test File: test_accessibility.py
# Description: Test the accessibility of the app.
# JIRA Ticket: UIUX-003
# Instructions: Implement tests for verifying keyboard navigation and screen reader compatibility.

from playwright.sync_api import sync_playwright

def test_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Test keyboard navigation
        page.keyboard.press("Tab")
        assert page.locator(":focus").count() > 0, "Keyboard navigation is not working."

        # Test screen reader compatibility (using ARIA roles as a proxy)
        assert page.locator("[role='button']").count() > 0, "No ARIA roles found for buttons."

        browser.close()