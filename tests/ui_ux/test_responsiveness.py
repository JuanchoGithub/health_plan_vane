# Test File: test_responsiveness.py
# Description: Test the responsiveness of the app on different screen sizes.
# JIRA Ticket: UIUX-001
# Instructions: Implement tests for verifying the app's layout and usability on various devices.

from playwright.sync_api import sync_playwright

def test_responsiveness():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Test responsiveness for different screen sizes
        screen_sizes = [(1920, 1080), (1366, 768), (375, 667)]
        for width, height in screen_sizes:
            page.set_viewport_size({"width": width, "height": height})
            assert page.locator(".responsive-element").is_visible(), f"UI is not responsive for {width}x{height}."

        browser.close()