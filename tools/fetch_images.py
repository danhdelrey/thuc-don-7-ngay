#!/usr/bin/env python3
"""Find freely licensed dish photos on Wikimedia Commons.
Lists candidate photo URLs (with author/license) per dish into review/candidates.json,
plus contact sheets so the right photo can be picked. The app only links to the URLs.
"""
import json, os, re, subprocess, sys, urllib.parse, urllib.request, html
UA = 'thuc-don-7-ngay/1.0 (https://github.com/danhdelrey/thuc-don-7-ngay)'
API = 'https://commons.wikimedia.org/w/api.php'
FREE = re.compile(r'^(CC0|CC BY|CC-BY|Public domain|PD|Attribution|No restrictions)', re.I)

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()

def api(params):
    params.update(format='json', formatversion='2')
    return json.loads(get(API + '?' + urllib.parse.urlencode(params)))

def strip(t): return html.unescape(re.sub(r'<[^>]+>', '', t or '')).strip()

def info(pages):
    res = []
    for p in pages:
        ii = (p.get('imageinfo') or [{}])[0]
        if not ii.get('thumburl') or ii.get('mime') not in ('image/jpeg', 'image/png', 'image/webp'): continue
        m = ii.get('extmetadata', {})
        lic = strip(m.get('LicenseShortName', {}).get('value'))
        if not FREE.match(lic) or 'NC' in lic or 'ND' in lic: continue
        res.append(dict(title=p['title'], thumb=ii['thumburl'], page=ii.get('descriptionurl'),
                        author=strip(m.get('Artist', {}).get('value'))[:80] or 'Không rõ', license=lic,
                        idx=p.get('index', 0)))
    return sorted(res, key=lambda r: r['idx'])

IIP = dict(prop='imageinfo', iiprop='url|mime|extmetadata', iiurlwidth='480')

def search(q, n=6):
    d = api(dict(action='query', generator='search', gsrnamespace='6', gsrlimit=str(n), gsrsearch=q + ' filetype:bitmap', **IIP))
    return info(d.get('query', {}).get('pages', []))

def by_title(t):
    d = api(dict(action='query', titles=t, **IIP))
    return info(d.get('query', {}).get('pages', []))

def save(url, path):
    raw = path + '.raw'
    open(raw, 'wb').write(get(url))
    subprocess.run(['convert', raw, '-auto-orient', '-resize', '320x320^', '-gravity', 'center',
                    '-extent', '320x320', '-strip', '-quality', '72', path], check=True)
    os.remove(raw)

def main(mode):
    D = json.load(open('tools/images.json', encoding='utf-8'))
    if mode == 'review':
        os.makedirs('review', exist_ok=True); allc = {}
        for k, d in D.items():
            seen, cands = set(), []
            for q in d['q']:
                try:
                    for c in search(q):
                        if c['title'] not in seen: seen.add(c['title']); cands.append(c)
                except Exception as e: print('ERR', k, q, e)
                if len(cands) >= 8: break
            cands = cands[:8]; allc[k] = cands; files = []
            for i, c in enumerate(cands):
                f = f'review/{k}-{i}.jpg'
                try: save(c['thumb'], f); files.append(f)
                except Exception as e: print('ERR dl', k, e)
            if files:
                subprocess.run(['montage', *[x for i, f in enumerate(files) for x in ('-label', str(i), f)],
                                '-tile', '4x', '-geometry', '200x200+4+4', '-pointsize', '28',
                                '-title', k, f'review/sheet-{k}.jpg'], check=False)
            print(k, len(cands))
        json.dump(allc, open('review/candidates.json', 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else 'review')
