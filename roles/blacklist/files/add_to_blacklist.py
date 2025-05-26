#!/usr/bin/env python3
import sys
import logging
from playwright.sync_api import sync_playwright, Error as PlaywrightError

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_to_blacklist(playwright, phone_number: str, description: str) -> None:
    browser = None
    context = None
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        logging.info(f"Acessando página de login...")
        page.goto("http://192.168.100.32/admin/config.php")

        logging.info(f"Realizando login...")
        page.locator("#login_admin").click()
        page.get_by_role("textbox", name="username").fill("jersonjunior")
        page.get_by_role("textbox", name="password").fill("@#in4008@#")
        page.get_by_role("button", name="Continue").click()

        page.wait_for_selector("text=Admin", timeout=10000)
        logging.info("Login realizado com sucesso.")

        page.get_by_role("button", name="Admin").click()
        page.get_by_role("link", name="Blacklist").click()
        page.get_by_role("link", name=" Blacklist Number").click()

        logging.info(f"Adicionando número {phone_number} com descrição '{description}'...")
        page.get_by_role("textbox", name="Number/CallerID").fill(phone_number)
        page.get_by_role("textbox", name="Description").fill(description)
        page.get_by_role("button", name="Save changes").click()

        page.wait_for_timeout(1000)
        logging.info("Número adicionado com sucesso.")

    except PlaywrightError as e:
        logging.error(f"Erro do Playwright: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        sys.exit(1)
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        logging.info("Recursos liberados.")

def main():
    if len(sys.argv) < 3:
        print("Uso: ./add_to_blacklist.py <numero_telefone> <descricao>")
        sys.exit(1)

    phone_number = sys.argv[1]
    description = sys.argv[2]

    with sync_playwright() as playwright:
        add_to_blacklist(playwright, phone_number, description)

if __name__ == "__main__":
    main()
