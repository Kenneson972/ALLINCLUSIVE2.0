#!/usr/bin/env python3
"""
Build db.json from CSV + backup JSON
- Reads Catalogue_Villas_*.csv if present
- Merges with backup_villas.json if present
- Normalizes fields and writes ../data/db.json
If inputs are missing, seeds 21 demo villas with placeholder images.
"""
import csv, json, re, sys, os, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '..', 'data', 'db.json')

CSV_FILES = glob.glob(os.path.join(ROOT, 'Catalogue_Villas_*.csv'))
BACKUP = os.path.join(ROOT, 'backup_villas.json')

villas = []

def slugify(s):
    s = (s or '').strip().lower()
    s = re.sub(r"[\s]+","-", s)
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s or 'villa'

if CSV_FILES:
    csv_path = CSV_FILES[0]
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for i,row in enumerate(r, start=1):
            name = row.get('name') or row.get('Nom') or f'Villa {i}'
            slug = slugify(row.get('slug') or name)
            price = float(row.get('pricePerNight') or row.get('Prix') or 0)
            images = [p for p in (row.get('images') or '').split('|') if p]
            villas.append({
                'id': row.get('id') or slug,
                'slug': slug,
                'name': name,
                'status': row.get('status') or 'active',
                'pricePerNight': price,
                'images': images,
                'location': row.get('location') or row.get('Ville') or '',
                'bedrooms': int(row.get('bedrooms') or 0),
                'bathrooms': int(row.get('bathrooms') or 0),
                'surface': int(row.get('surface') or 0),
                'amenities': (row.get('amenities') or '').split('|') if row.get('amenities') else []
            })

if os.path.exists(BACKUP):
    with open(BACKUP, encoding='utf-8') as f:
        try:
            arr = json.load(f)
            if isinstance(arr, list):
                villas.extend(arr)
        except Exception:
            pass

# Deduplicate by id/slug
seen = set()
normalized = []
for v in villas:
    key = v.get('id') or v.get('slug')
    if key in seen: continue
    seen.add(key)
    # Ensure images and placeholders
    imgs = v.get('images') or []
    v['images'] = imgs
    normalized.append(v)

# Seed if missing or too small
if len(normalized) < 21:
    base = len(normalized)
    for i in range(base+1, 22):
        normalized.append({
            'id': f'villa-{i:03d}',
            'slug': f'villa-{i:03d}',
            'name': f'Villa {i}',
            'status': 'active',
            'pricePerNight': 600 + (i*20),
            'images': [],
            'location': 'Martinique',
            'bedrooms': 3,
            'bathrooms': 2,
            'surface': 120 + i,
            'amenities': []
        })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False, indent=2)

print(f'[{datetime.now()}] Wrote {len(normalized)} villas to {OUT}')