import json
import os
import base64

ROOT = os.path.dirname(os.path.dirname(__file__))
INPUT = os.path.join(ROOT, 'dashboard', 'dashboard_4_with_images.json')
OUT_DIR = os.path.join(ROOT, 'dashboard')

def find_svgs(obj, path=()):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith('data:image/svg+xml'):
                results.append((k, v))
            else:
                results.extend(find_svgs(v, path + (k,)))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            results.extend(find_svgs(item, path + (str(i),)))
    return results

def decode_and_write(name, datauri):
    # data:image/svg+xml;base64,AAAA
    if ',' not in datauri:
        return False
    header, payload = datauri.split(',', 1)
    if header.endswith(';base64'):
        data = base64.b64decode(payload)
    else:
        # assume URL-encoded or raw utf-8
        data = payload.encode('utf-8')
    outpath = os.path.join(OUT_DIR, name)
    with open(outpath, 'wb') as f:
        f.write(data)
    return outpath

def main():
    if not os.path.exists(INPUT):
        print('Input file not found:', INPUT)
        return
    with open(INPUT, 'r', encoding='utf-8') as f:
        j = json.load(f)
    svgs = find_svgs(j)
    if not svgs:
        print('No embedded SVGs found')
        return
    written = []
    for name, datauri in svgs:
        # sanitize name
        name_clean = name.replace('/', '_')
        if not name_clean.lower().endswith('.svg'):
            name_clean += '.svg'
        out = decode_and_write(name_clean, datauri)
        if out:
            written.append(out)
            print('Wrote', out)
    print('Done. Wrote', len(written), 'files to', OUT_DIR)

if __name__ == '__main__':
    main()
