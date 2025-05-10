from playwright.sync_api import sync_playwright

def test_registration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:8501")

        # Log the start of the test
        print("Navigating to the application...")

        # Wait for the application to load
        print("Waiting for the application to load...")
        page.wait_for_selector("text=Iniciar Sesión / Registrarse")
        print("Application loaded.")

        # Debugging: Log all matching elements for the 'Registrarse' radio button
        print("Debugging: Locating 'Registrarse' radio button...")
        matching_radio_buttons = page.locator("[data-testid='stRadio'] >> text=Registrarse").all()
        print(f"Found {len(matching_radio_buttons)} matching elements for 'Registrarse' radio button.")

        # Ensure the 'Registrarse' radio button is uniquely identified
        assert len(matching_radio_buttons) == 1, "'Registrarse' radio button is not uniquely identified."

        # Click on the 'Registrarse' radio button
        print("Clicking on the 'Registrarse' radio button...")
        matching_radio_buttons[0].click()
        print("'Registrarse' radio button clicked.")

        # Adding a wait condition for the 'Registrarse' button to ensure it is fully rendered
        print("Waiting for the 'Registrarse' button to be rendered with increased timeout...")
        page.wait_for_selector("[data-testid='register_button']", timeout=60000)
        print("'Registrarse' button rendered.")

        # Debugging: Log all matching elements for the 'Registrarse' button
        print("Debugging: Locating 'Registrarse' button...")
        matching_buttons = page.locator("[data-testid='register_button']").all()
        print(f"Found {len(matching_buttons)} matching elements for 'Registrarse' button.")

        # Ensure the 'Registrarse' button is uniquely identified
        assert len(matching_buttons) == 1, "'Registrarse' button is not uniquely identified."

        # Click on the 'Registrarse' button
        print("Clicking on the 'Registrarse' button...")
        matching_buttons[0].click()
        print("'Registrarse' button clicked.")

        # Debugging: Log all matching elements for the 'Registrarse' option
        print("Debugging: Locating 'Registrarse' option in the radio group...")
        matching_elements = page.locator("[data-testid='stRadio'] >> text=Registrarse").all()
        print(f"Found {len(matching_elements)} matching elements for 'Registrarse'.")

        # Ensure the 'Registrarse' option is uniquely identified
        assert len(matching_elements) == 1, "'Registrarse' option is not uniquely identified."

        # Use a specific locator for the 'Registrarse' option in the radio group
        print("Selecting 'Registrarse' option in the radio group...")
        page.locator("[data-testid='stRadio'] >> text=Registrarse").click()
        print("'Registrarse' option selected.")

        # Fill in registration details
        print("Filling in registration details...")
        page.fill("[aria-label='Nombre de Usuario']", "new_user")
        page.fill("[aria-label='Contraseña']", "new_password")
        page.fill("[aria-label='Fecha de Inicio del Plan']", "2025-05-01")
        page.fill("[aria-label='Peso Actual (kg)']", "70")
        print("Details filled. Clicking on 'Registrarse' button...")
        page.click("text=Registrarse")

        # Wait for the success message to appear
        print("Waiting for success message...")
        page.wait_for_selector("text=¡Registro exitoso! Por favor, inicie sesión.")
        print("Success message appeared.")

        # Verify successful registration
        assert page.locator("text=¡Registro exitoso! Por favor, inicie sesión.").is_visible(), "Registration failed or success message not displayed."
        print("Test completed successfully.")

        browser.close()