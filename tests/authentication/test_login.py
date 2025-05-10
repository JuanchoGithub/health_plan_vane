from playwright.sync_api import sync_playwright

def test_login():
    username = "new_user"
    password = "new_password"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Interact with the sidebar for login
        page.fill("[aria-label='Nombre de Usuario']", username)
        page.fill("[aria-label='Contraseña']", password)
        page.click("text=Iniciar Sesión")

        # Wait for the welcome message to appear
        page.wait_for_selector(f"text=¡Bienvenido/a, {username}!", timeout=5000)

        # Verify successful login
        assert page.locator(f"text=¡Bienvenido/a, {username}!").is_visible(), "Login failed or user not authenticated."

        browser.close()