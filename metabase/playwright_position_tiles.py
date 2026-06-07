"""
Playwright script to automatically position dashboard tiles by dragging them.

Usage (run locally, headed):
  pip install playwright
  python -m playwright install
  $env:METABASE_USER='you@example.com'
  $env:METABASE_PASS='yourpass'
  python metabase\playwright_position_tiles.py

This script reads `metabase/dashboard_layout.json` for target positions (percent of dashboard container).
It will enter Edit mode, find tiles by their visible title text, and drag them to the target location.

Note: Dashboard DOM varies between Metabase versions; this is a best-effort script and may need small selectors tweaks.
"""
from playwright.sync_api import sync_playwright
import os
import json
import time

DASHBOARD_URL = os.getenv('METABASE_URL', 'http://localhost:3000') + '/dashboard/4'
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')

LAYOUT_PATH = os.path.join(os.path.dirname(__file__), 'dashboard_layout.json')

def load_layout():
    if not os.path.exists(LAYOUT_PATH):
        raise SystemExit(f'Layout file not found: {LAYOUT_PATH}')
    with open(LAYOUT_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def ensure_login(page):
    # attempt to login if form present
    if page.query_selector('input[placeholder*="email"], input[type="email"]'):
        if not USER or not PASS:
            raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')
        page.fill('input[type="email"], input[name="username"], input[placeholder*="email"]', USER)
        page.fill('input[type="password"]', PASS)
        btn = page.query_selector('button:has-text("Entrar"), button:has-text("Sign in"), button[type="submit"]')
        if btn:
            btn.click()
            page.wait_for_load_state('networkidle')

def main():
    layout = load_layout()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(DASHBOARD_URL)
        time.sleep(1)
        ensure_login(page)
        page.goto(DASHBOARD_URL)
        page.wait_for_timeout(1200)

        # Enter edit mode
        edit = page.query_selector('button:has-text("Editar"), button:has-text("Edit")')
        if edit:
            edit.click()
            page.wait_for_timeout(800)

        # locate dashboard container to compute coordinates
        container = page.query_selector('[data-testid="dashboard-root"], .Dashboard')
        if not container:
            container = page.query_selector('body')
        box = container.bounding_box()
        if not box:
            raise SystemExit('Could not determine dashboard container bounding box')

        for title, pos in layout.items():
            try:
                # find tile by title text
                el = page.query_selector(f'text="{title}"')
                if not el:
                    el = page.query_selector(f'text={title}')
                if not el:
                    print('Tile not found:', title)
                    continue
                tile = el.evaluate_handle('e => e.closest("[data-testid=\"dashboard-card\"], .card, .dashboard-card")')
                if not tile:
                    # fallback: use element handle itself
                    tile_box = el.bounding_box()
                else:
                    tile_box = tile.bounding_box()

                if not tile_box:
                    print('Could not determine box for', title)
                    continue

                # compute target coordinates
                tx = box['x'] + box['width'] * (pos.get('x_pct', 0.1) / 100.0)
                ty = box['y'] + box['height'] * (pos.get('y_pct', 0.1) / 100.0)

                sx = tile_box['x'] + tile_box['width'] / 2
                sy = tile_box['y'] + tile_box['height'] / 2

                page.mouse.move(sx, sy)
                page.mouse.down()
                page.mouse.move(tx, ty, steps=20)
                page.mouse.up()
                print(f'Moved {title} to ({pos.get("x_pct")},{pos.get("y_pct")})')
                page.wait_for_timeout(600)
            except Exception as e:
                print('Error moving', title, e)

        # click Save
        save = page.query_selector('button:has-text("Salvar"), button:has-text("Done"), button:has-text("Save")')
        if save:
            save.click()
            page.wait_for_timeout(800)

        print('Done. Review dashboard visually.')
        ctx.close()
        browser.close()

if __name__ == '__main__':
    main()
