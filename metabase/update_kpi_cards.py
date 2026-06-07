import os
import requests

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')

if not USER or not PASS:
    raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')

cards_to_update = {
    49: 'kpi_total_vendas.sql',
    50: 'kpi_num_pedidos.sql',
    51: 'kpi_ticket_medio.sql',
}


def auth():
    s = requests.Session()
    r = s.post(f"{METABASE_URL}/api/session", json={"username": USER, "password": PASS})
    r.raise_for_status()
    return s


def read_sql(name):
    path = os.path.join(os.path.dirname(__file__), 'questions', name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def update_card(s, card_id, sql):
    # fetch existing card
    r = s.get(f"{METABASE_URL}/api/card/{card_id}")
    r.raise_for_status()
    card = r.json()
    # replace dataset_query.native (try both shapes)
    dq = card.get('dataset_query') or {}
    if isinstance(dq, dict) and 'stages' in dq:
        # mbql form
        dq['stages'] = [{'lib/type': 'mbql.stage/native', 'native': sql}]
    else:
        # try native shape
        dq = {'native': {'query': sql}, 'database': card.get('database_id')}
    card['dataset_query'] = dq
    # update
    r2 = s.put(f"{METABASE_URL}/api/card/{card_id}", json=card)
    print(card_id, r2.status_code, r2.text[:200])


def main():
    s = auth()
    for cid, fname in cards_to_update.items():
        sql = read_sql(fname)
        print('Updating', cid)
        update_card(s, cid, sql)


if __name__ == '__main__':
    main()
