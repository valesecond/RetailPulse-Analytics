import os
import json
import requests

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')
DASHBOARD_ID = int(os.getenv('METABASE_DASHBOARD_ID', '4'))

if not USER or not PASS:
    raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')

session = requests.Session()
session.post(f"{METABASE_URL}/api/session", json={"username": USER, "password": PASS}).raise_for_status()

src = os.path.join(os.path.dirname(__file__), '..', 'dashboard', f'dashboard_{DASHBOARD_ID}_with_images.json')
if not os.path.exists(src):
    src = os.path.join(os.path.dirname(__file__), '..', 'dashboard', f'dashboard_{DASHBOARD_ID}.json')
    if not os.path.exists(src):
        raise SystemExit('No dashboard export file found. Run export/embed scripts first.')

with open(src, 'r', encoding='utf-8') as f:
    new = json.load(f)

# Fetch current dashboard to preserve fields API expects
resp = session.get(f"{METABASE_URL}/api/dashboard/{DASHBOARD_ID}")
resp.raise_for_status()
current = resp.json()

# Replace metadata
current['metadata'] = new.get('metadata', current.get('metadata'))

# PUT updated dashboard
put = session.put(f"{METABASE_URL}/api/dashboard/{DASHBOARD_ID}", json=current)
print('PUT status:', put.status_code)
print(put.text[:1000])
put.raise_for_status()
print('Dashboard metadata updated successfully')
