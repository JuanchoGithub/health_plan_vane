# Test File: test_ui_rendering.py
# Description: Test the correct rendering of UI components.
# JIRA Ticket: UIUX-002
# Instructions: Implement tests for verifying the display of buttons, forms, and charts.

from playwright.sync_api import sync_playwright

def test_ui_rendering():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Verify buttons are rendered
        assert page.locator("button").count() > 0, "No buttons are rendered."

        # Verify forms are rendered
        assert page.locator("form").count() > 0, "No forms are rendered."

        # Verify charts are rendered
        assert page.locator(".chart-container").count() > 0, "No charts are rendered."

        browser.close()