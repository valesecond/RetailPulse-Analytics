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

def find_db_id():
    r = session.get(f"{METABASE_URL}/api/database")
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and 'data' in data:
        items = data['data']
    elif isinstance(data, list):
        items = data
    else:
        items = [data]
    # prefer the first non-null id
    for d in items:
        if isinstance(d, dict) and d.get('id'):
            return d.get('id')
    raise SystemExit('No database id found via API')

DB_ID = find_db_id()


dash_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', f'dashboard_{DASHBOARD_ID}_with_images.json')
if not os.path.exists(dash_path):
    dash_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', f'dashboard_{DASHBOARD_ID}.json')
    if not os.path.exists(dash_path):
        raise SystemExit('Exported dashboard JSON not found. Run export/embed scripts first.')

with open(dash_path, 'r', encoding='utf-8') as f:
    dash = json.load(f)

images = dash.get('metadata', {}).get('embedded_images', {})
if not images:
    raise SystemExit('No embedded images found in dashboard metadata.')

created = {}

def try_create_card(name, markdown):
    # Try several display types that could work for markdown/text
    displays = ['dashboard_text', 'text', 'notebook', 'card']
    for disp in displays:
        payload = {
            'name': name,
            'display': disp,
            'visualization_settings': {'content': markdown, 'format': 'markdown'}
        }
        try:
            r = session.post(f"{METABASE_URL}/api/card", json=payload)
            if r.status_code in (200,201):
                return r.json().get('id'), r.status_code, r.text
            else:
                print('Attempt', disp, 'failed', r.status_code, r.text[:200])
        except Exception as e:
            print('Error for display', disp, e)
    return None, None, None

    for fname, datauri in images.items():
        name = f'Image - {fname}'
        md = f'![{fname}]({datauri})'
    print('Creating card for', fname)
    # use a minimal dataset_query to satisfy API requirements
    dq = {
        'lib/type': 'mbql/query',
        'database': DB_ID,
        'stages': [
            {'lib/type': 'mbql.stage/native', 'native': 'SELECT 1 as dummy'}
        ]
    }
    cid = None
    for disp in ['dashboard_text', 'text', 'notebook', 'card']:
        payload = {
            'name': name,
            'display': disp,
            'dataset_query': dq,
            'visualization_settings': {'content': md, 'format': 'markdown'}
        }
        r = session.post(f"{METABASE_URL}/api/card", json=payload)
        print('Attempt', disp, r.status_code)
        if r.status_code in (200,201):
            cid = r.json().get('id')
            break
        else:
            print('resp', r.text[:200])
    if cid:
        created[name] = cid
        print('Created', cid)
        # try attach to dashboard (best-effort)
        r = session.post(f"{METABASE_URL}/api/dashboard/{DASHBOARD_ID}/cards", json={'cardId': cid})
        print('Attach attempt', r.status_code, r.text[:200])
    else:
        print('Failed to create card for', fname)

with open(os.path.join(os.path.dirname(__file__), 'image_cards_manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(created, f, indent=2)

print('Done. Manifest saved to metabase/image_cards_manifest.json')
