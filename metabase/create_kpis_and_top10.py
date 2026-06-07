import os
import requests
import json

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')
DB_NAME = os.getenv('METABASE_DB_NAME', 'RetailPulse')
DASHBOARD_ID = int(os.getenv('METABASE_DASHBOARD_ID', '4'))

if not USER or not PASS:
    raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')


def auth():
    s = requests.Session()
    r = s.post(f"{METABASE_URL}/api/session", json={"username": USER, "password": PASS})
    r.raise_for_status()
    return s


def find_db_id(s):
    r = s.get(f"{METABASE_URL}/api/database")
    r.raise_for_status()
    data = r.json()
    # normalize possible shapes
    if isinstance(data, dict) and 'data' in data:
        items = data['data']
    elif isinstance(data, list):
        items = data
    else:
        items = [data]

    for d in items:
        if isinstance(d, dict) and d.get('name') == DB_NAME:
            return d.get('id')

    # fallback: try matching by substring
    for d in items:
        if isinstance(d, dict) and DB_NAME.lower() in str(d.get('name','')).lower():
            return d.get('id')

    raise SystemExit('Database not found: ' + DB_NAME + f' (api returned {type(data)})')


def read_sql(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def create_card(s, db_id, name, sql, display='table'):
    payload = {
        'name': name,
        'dataset_query': {
            'lib/type': 'mbql/query',
            'database': db_id,
            'stages': [
                {'lib/type': 'mbql.stage/native', 'native': sql}
            ]
        },
        'display': display,
        'visualization_settings': {}
    }
    r = s.post(f"{METABASE_URL}/api/card", json=payload)
    r.raise_for_status()
    return r.json().get('id')


def try_attach_card(s, dashboard_id, card_id):
    # try POST endpoint first
    r = s.post(f"{METABASE_URL}/api/dashboard/{dashboard_id}/cards", json={'cardId': card_id})
    return r.status_code, r.text


def main():
    s = auth()
    db_id = find_db_id(s)

    base = os.path.join(os.path.dirname(__file__), 'questions')
    files = [
        ('KPI - Total Vendas', 'kpi_total_vendas.sql', 'number'),
        ('KPI - Nº Pedidos', 'kpi_num_pedidos.sql', 'number'),
        ('KPI - Ticket Médio', 'kpi_ticket_medio.sql', 'number'),
        ('Top10 - Produtos', 'top10_produtos.sql', 'table'),
        ('Top10 - Clientes', 'top10_clientes.sql', 'table'),
    ]

    created = {}
    for name, fname, display in files:
        path = os.path.join(base, fname)
        sql = read_sql(path)
        print('Creating', name)
        cid = create_card(s, db_id, name, sql, display)
        created[name] = cid
        print(' Created id', cid)
        st, txt = try_attach_card(s, DASHBOARD_ID, cid)
        print(' Attach attempt', st, txt[:200])

    # save manifest
    manifest_path = os.path.join(os.path.dirname(__file__), 'dashboard_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump({'dashboard_id': DASHBOARD_ID, 'cards': created}, f, indent=2)
    print('Saved manifest to', manifest_path)


if __name__ == '__main__':
    main()
