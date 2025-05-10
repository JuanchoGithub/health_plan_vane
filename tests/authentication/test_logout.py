from playwright.sync_api import sync_playwright

def test_logout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Perform login first
        page.fill("[aria-label='Nombre de Usuario']", "new_user")
        page.fill("[aria-label='Contraseña']", "new_password")
        page.click("text=Iniciar Sesión")

        # Perform logout
        page.click("text=Cerrar Sesión")

        # Verify successful logout
        assert page.locator("text=Iniciar Sesión / Registrarse").is_visible(), "Logout failed or user still authenticated."

        browser.close()