"""
Playwright automation to add and arrange Metabase cards to the dashboard.

Usage (run locally on your machine where you're logged in, headed):

1. Install dependencies:
   pip install playwright
   python -m playwright install

2. Run script (it will open a visible browser):
   python metabase/playwright_add_cards.py

Notes:
- This script assumes Metabase is reachable at http://localhost:3000.
- It attempts to sign in using environment vars METABASE_USER and METABASE_PASS if not already logged in.
- Run it in a headed environment so you can see and interact if needed.
"""
from playwright.sync_api import sync_playwright
import os
import time

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')
DASHBOARD_URL = METABASE_URL + '/dashboard/4'

NAMES = [
    'KPI - Total Vendas','KPI - Nº Pedidos','KPI - Ticket Médio',
    'Top10 - Produtos','Top10 - Clientes',
    'Vendas Mensais','Vendas por Categoria','Vendas por Regiao'
]

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(DASHBOARD_URL)
        time.sleep(1)

        # If login form present and credentials provided, sign in
        if page.query_selector('input[placeholder*="email"], input[placeholder*="Endereço de e-mail"], input[type="email"]'):
            if not USER or not PASS:
                raise SystemExit('Please set METABASE_USER and METABASE_PASS env vars')
            page.fill('input[type="email"], input[name="username"], input[placeholder*="email"]', USER)
            page.fill('input[type="password"]', PASS)
            # click Entrar
            btn = page.query_selector('button:has-text("Entrar"), button:has-text("Sign in"), button[type="submit"]')
            if btn:
                btn.click()
                page.wait_for_load_state('networkidle')

        # Ensure dashboard loaded
        page.goto(DASHBOARD_URL)
        page.wait_for_timeout(1500)

        # Enter edit mode
        edit = page.query_selector('button:has-text("Editar"), button:has-text("Edit")')
        if edit:
            edit.click()
            page.wait_for_timeout(800)

        # helper to dismiss modal overlays
        def dismiss_overlays():
            # press Escape and try clicking any modal close buttons
            try:
                page.keyboard.press('Escape')
            except Exception:
                pass
            # try to click common close selectors
            for sel in ["button[aria-label='Close']", "button:has-text('Fechar')", "button:has-text('Close')", "button[aria-label='Close modal']"]:
                try:
                    el = page.query_selector(sel)
                    if el:
                        el.click()
                except Exception:
                    pass

        # For each card name, search and add (with retries if overlay blocks clicks)
        for name in NAMES:
            search = page.query_selector('input[placeholder*="Pesquisar"], input[placeholder*="Search"], input[aria-label*="Search"]')
            if search:
                search.fill(name)
                page.wait_for_timeout(600)
                item = page.query_selector(f'text="{name}"')
                if item:
                    try:
                        item.click()
                    except Exception:
                        dismiss_overlays()
                        page.wait_for_timeout(300)
                        try:
                            item.click()
                        except Exception:
                            print('Could not click', name)
                    page.wait_for_timeout(700)
                    continue
            # fallback direct click with overlay handling
            item2 = page.query_selector(f'text={name}')
            if item2:
                try:
                    item2.click()
                except Exception:
                    dismiss_overlays()
                    page.wait_for_timeout(300)
                    try:
                        item2.click()
                    except Exception:
                        print('Could not click fallback', name)
                page.wait_for_timeout(700)

        # Save
        save = page.query_selector('button:has-text("Salvar"), button:has-text("Done"), button:has-text("Save")')
        if save:
            save.click()
            page.wait_for_timeout(500)

        print('Finished - inspect the dashboard and adjust positioning manually if needed.')
        # Keep browser open for review
        time.sleep(2)
        context.close()
        browser.close()

if __name__ == '__main__':
    run()
