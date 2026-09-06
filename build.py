#!/usr/bin/env python3
"""Build the NeetCode C++ Desk site.

Steps:
  1. Fetch the problem list (with NeetCode's own slugs and list membership) from neetcode.io's JS bundle.
  2. Clone or update the MIT-licensed neetcode-gh/leetcode repo, which holds the articles served on neetcode.io.
  3. Parse every article's C++ approaches and complexities.
  4. Write data.json, problems/*.md, INDEX.md and index.html.

Usage:
  python3 build.py                 # full build (network required)
  python3 build.py --offline       # rebuild index.html and markdown from the cached data in .cache/
"""
import argparse, json, os, re, subprocess, sys, urllib.request, collections, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, '.cache')
NC_REPO = os.path.join(CACHE, 'neetcode')
SITE = 'https://neetcode.io'
UA = {'User-Agent': 'Mozilla/5.0 (neetcode-cpp-desk build script)'}

PREMIUM = [271, 252, 253, 286, 323, 261, 269, 277, 505, 694, 1197, 549, 340, 159, 1650, 1762, 1229, 1060, 1197, 1245]

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode('utf-8', 'ignore')

def repo_url():
    env = os.environ.get('REPO_URL')
    if env: return env
    try:
        r = subprocess.check_output(['git', '-C', ROOT, 'remote', 'get-url', 'origin'], text=True).strip()
        r = re.sub(r'^git@github\.com:', 'https://github.com/', r)
        return re.sub(r'\.git$', '', r)
    except Exception:
        return 'https://github.com/neetcode-gh/leetcode'

# ---------- 1. problem list from the site bundle ----------
def fetch_problem_list():
    html = fetch(SITE + '/practice')
    m = re.search(r'src="(main\.[0-9a-f]+\.js)"', html)
    if not m: sys.exit('Could not find main.*.js in neetcode.io/practice')
    js = fetch(f'{SITE}/{m.group(1)}')
    objs = re.findall(r'\{problem:"[^"]*",pattern:"[^"]*",link:"[^"]*"[^{}]*\}', js)
    out, seen = [], set()
    for o in objs:
        d = {}
        for k, v in re.findall(r'(\w+):("(?:[^"\\]|\\.)*"|!0|!1|\d+)', o):
            d[k] = json.loads(v) if v.startswith('"') else (v == '!0')
        if d['link'] in seen: continue
        seen.add(d['link']); out.append(d)
    if len(out) < 500: sys.exit(f'Only found {len(out)} problems in the bundle; the site format probably changed.')
    return out

# ---------- 2. solutions repo ----------
def sync_repo():
    os.makedirs(CACHE, exist_ok=True)
    if os.path.isdir(os.path.join(NC_REPO, '.git')):
        subprocess.check_call(['git', '-C', NC_REPO, 'pull', '-q', '--ff-only'])
    else:
        subprocess.check_call(['git', 'clone', '-q', '--depth', '1', 'https://github.com/neetcode-gh/leetcode.git', NC_REPO])
    return subprocess.check_output(['git', '-C', NC_REPO, 'log', '-1', '--format=%cd', '--date=short'], text=True).strip()

# ---------- 3. article parsing ----------
def parse_article(path):
    t = open(path, encoding='utf-8').read()
    parts = re.split(r'^## (\d+)\. (.+)$', t, flags=re.M)
    approaches = []
    for i in range(1, len(parts), 3):
        title = parts[i + 1].strip()
        body = re.split(r'^## (?!Intuition|Algorithm|Time)', parts[i + 2], flags=re.M)[0]
        code = re.search(r'^```cpp\n(.*?)^```', body, flags=re.M | re.S)
        intu = re.search(r'^##+ Intuition\s*\n(.*?)(?=^##+ |^::tabs-start)', body, flags=re.M | re.S)
        comp = re.search(r'^##+ Time & Space Complexity\s*\n(.*?)(?=^---|^##+ |\Z)', body, flags=re.M | re.S)
        approaches.append(dict(title=title, cpp=code.group(1).rstrip('\n') if code else None,
                               intuition=intu.group(1).strip() if intu else '',
                               complexity=comp.group(1).strip() if comp else ''))
    return approaches

def lists_of(d):
    return [n for k, n in [('blind75', 'Blind 75'), ('neetcode150', 'NeetCode 150'), ('neetcode250', 'NeetCode 250')] if d.get(k)]

def build_records(site):
    arts = {f[:-3] for f in os.listdir(f'{NC_REPO}/articles')}
    cpps = {f[:-4] for f in os.listdir(f'{NC_REPO}/cpp')}
    rows = []
    for d in site:
        if d.get('pattern') == 'JavaScript': continue
        slug = (d.get('ncLink') or d['link']).strip('/')
        has_art, has_cpp = slug in arts, d['code'] in cpps
        if not has_art and not has_cpp: continue
        num = int(d['code'].split('-')[0])
        rows.append(dict(
            id=num, title=d['problem'], difficulty=d['difficulty'], pattern=d['pattern'], lists=lists_of(d),
            leetcode=f"https://leetcode.com/problems/{d['link'].strip('/')}/",
            neetcode=f'https://neetcode.io/problems/{slug}',
            video=f"https://www.youtube.com/watch?v={d['video']}" if d.get('video') else None,
            code=d['code'],
            approaches=parse_article(f'{NC_REPO}/articles/{slug}.md') if has_art else [],
            repo_cpp=open(f"{NC_REPO}/cpp/{d['code']}.cpp", encoding='utf-8').read().rstrip('\n') if has_cpp else None))
    return rows

# ---------- 4. outputs ----------
def write_markdown(rows):
    out = os.path.join(ROOT, 'problems')
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    for r in rows:
        L = [f"# {r['id']}. {r['title']}", '',
             f"- **Difficulty:** {r['difficulty']}  ", f"- **Pattern:** {r['pattern']}  ",
             f"- **Lists:** {', '.join(r['lists']) or 'NeetCode All'}  ",
             f"- **LeetCode:** <{r['leetcode']}>  ", f"- **NeetCode:** <{r['neetcode']}>  "]
        if r['video']: L.append(f"- **Video:** <{r['video']}>  ")
        L += ['', '[← Back to index](../INDEX.md)', '']
        for i, a in enumerate(r['approaches']):
            L += [f"## {i + 1}. {a['title']}", '']
            if a['intuition']: L += [a['intuition'], '']
            L += ['```cpp', a['cpp'] or '// NeetCode has no C++ version of this approach yet.', '```', '']
            if a['complexity']: L += ['**Complexity**', '', a['complexity'], '']
        if r['repo_cpp']:
            L += [f"## Standalone solution file (`cpp/{r['code']}.cpp` in the NeetCode repo)", '', '```cpp', r['repo_cpp'], '```', '']
        open(f"{out}/{r['code']}.md", 'w', encoding='utf-8').write('\n'.join(L))

    def table(rs):
        t = ['| # | Problem | Diff | LeetCode | NeetCode | C++ approaches | Lists |', '|---|---|---|---|---|---|---|']
        for r in rs:
            n = len([a for a in r['approaches'] if a['cpp']])
            t.append(f"| {r['id']} | [{r['title']}](problems/{r['code']}.md) | {r['difficulty']} | [LC]({r['leetcode']}) | [NC]({r['neetcode']}) | {n or '—'} | {', '.join(x.replace('NeetCode ', 'NC') for x in r['lists']) or '—'} |")
        return t
    patterns = list(dict.fromkeys(r['pattern'] for r in rows))
    R = ['# Problem index', '', 'One markdown file per problem, generated by `build.py`. The interactive version is `index.html`.', '']
    for heading, pred in [('NeetCode 150 (includes Blind 75)', lambda r: 'NeetCode 150' in r['lists']),
                          ('NeetCode 250 — the extra 100', lambda r: 'NeetCode 250' in r['lists'] and 'NeetCode 150' not in r['lists']),
                          ('Other problems from NeetCode All', lambda r: 'NeetCode 250' not in r['lists'])]:
        R += [f'# {heading}', '']
        for p in patterns:
            rs = [r for r in rows if r['pattern'] == p and pred(r)]
            if rs: R += [f'## {p}', ''] + table(rs) + ['']
    open(os.path.join(ROOT, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(R))

def write_site(rows, updated):
    tpl = open(os.path.join(ROOT, 'template.html'), encoding='utf-8').read()
    data = json.dumps(rows, separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
    meta = json.dumps(dict(updated=updated, premium=sorted(set(PREMIUM))))
    html = tpl.replace('__DATA__', data).replace('__META__', meta).replace('__REPO_URL__', repo_url())
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
    # Body-only fragment, for hosts that supply their own document wrapper.
    frag = html.split('<!-- HEAD-END -->', 1)[1]
    frag = frag.replace('</head>\n<body>', '').replace('</body>\n</html>', '')
    open(os.path.join(CACHE, 'fragment.html'), 'w', encoding='utf-8').write(frag)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--offline', action='store_true', help='use cached data, no network')
    args = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    cache_json = os.path.join(CACHE, 'site-problems.json')
    if args.offline:
        site = json.load(open(cache_json)); updated = json.load(open(os.path.join(CACHE, 'meta.json')))['updated']
    else:
        site = fetch_problem_list(); json.dump(site, open(cache_json, 'w'), indent=1)
        updated = sync_repo(); json.dump(dict(updated=updated), open(os.path.join(CACHE, 'meta.json'), 'w'))
    rows = build_records(site)
    json.dump(rows, open(os.path.join(ROOT, 'data.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    write_markdown(rows)
    write_site(rows, updated)
    n_app = sum(len(r['approaches']) for r in rows)
    n_cpp = sum(1 for r in rows for a in r['approaches'] if a['cpp'])
    c = collections.Counter(tuple(r['lists']) for r in rows)
    print(f'{len(rows)} problems, {n_app} approaches ({n_cpp} with C++). NeetCode 150: {sum(v for k, v in c.items() if "NeetCode 150" in k)}, '
          f'NeetCode 250: {sum(v for k, v in c.items() if "NeetCode 250" in k)}. Solutions repo as of {updated}.')

if __name__ == '__main__':
    main()
