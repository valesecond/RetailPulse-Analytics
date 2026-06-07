import os
import base64
import json

dashboard_dir = os.path.join(os.path.dirname(__file__), '..', 'dashboard')
dashboard_json = os.path.join(dashboard_dir, 'dashboard_4.json')

if not os.path.exists(dashboard_json):
    raise SystemExit('Dashboard JSON not found. Run export_dashboard.py first.')

images = {}
svg_dir = os.path.join(os.path.dirname(__file__), '..', 'dashboard')
for fname in os.listdir(svg_dir):
    if not fname.lower().endswith('.svg'):
        continue
    path = os.path.join(svg_dir, fname)
    with open(path, 'rb') as f:
        b = f.read()
    b64 = base64.b64encode(b).decode('ascii')
    images[fname] = f'data:image/svg+xml;base64,{b64}'

with open(dashboard_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# attach images under a top-level metadata key
data.setdefault('metadata', {})
data['metadata']['embedded_images'] = images

out_path = os.path.join(dashboard_dir, 'dashboard_4_with_images.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Wrote', out_path)
