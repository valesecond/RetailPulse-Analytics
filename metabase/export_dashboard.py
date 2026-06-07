import os
import requests
import json

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')
DASHBOARD_ID = int(os.getenv('METABASE_DASHBOARD_ID', '4'))

if not USER or not PASS:
    raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')

session = requests.Session()
session.post(f"{METABASE_URL}/api/session", json={"username": USER, "password": PASS}).raise_for_status()

resp = session.get(f"{METABASE_URL}/api/dashboard/{DASHBOARD_ID}")
resp.raise_for_status()
data = resp.json()

out_dir = os.path.join(os.path.dirname(__file__), '..', 'dashboard')
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, f'dashboard_{DASHBOARD_ID}.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# copy manifest if exists
manifest_src = os.path.join(os.path.dirname(__file__), 'dashboard_manifest.json')
if os.path.exists(manifest_src):
    with open(manifest_src, 'r', encoding='utf-8') as f:
        m = json.load(f)
    with open(os.path.join(out_dir, 'dashboard_manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2, ensure_ascii=False)

print('Exported dashboard to', out_path)
