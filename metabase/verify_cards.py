import os
import requests
import json

METABASE_URL = os.getenv('METABASE_URL', 'http://localhost:3000')
USER = os.getenv('METABASE_USER')
PASS = os.getenv('METABASE_PASS')

if not USER or not PASS:
    raise SystemExit('Set METABASE_USER and METABASE_PASS env vars')

def auth_session():
    s = requests.Session()
    r = s.post(f"{METABASE_URL}/api/session", json={"username": USER, "password": PASS})
    r.raise_for_status()
    return s

def query_card(s, card_id):
    r = s.post(f"{METABASE_URL}/api/card/{card_id}/query/json")
    return r.status_code, r.text[:4000]

def main():
    s = auth_session()
    ids = list(range(46,54))
    results = {}
    for cid in ids:
        try:
            st, txt = query_card(s, cid)
            results[cid] = {'status': st, 'sample': txt}
            print(f'Card {cid}:', st)
        except Exception as e:
            results[cid] = {'error': str(e)}
            print(f'Card {cid} error:', e)

    # save short report
    with open(os.path.join(os.path.dirname(__file__), 'verify_report.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('Report saved to metabase/verify_report.json')

if __name__ == '__main__':
    main()
