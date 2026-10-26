"""Canonical catalogue validation and deterministic, escaped documentation rendering."""
import argparse
import datetime as dt
import html
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode, quote

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'candidate', 'curated', 'retired'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def plain(value, name, maximum=1200):
    require(isinstance(value, str) and 0 < len(value) <= maximum, f'Invalid {name}')
    require(not any(ord(c) < 32 or ord(c) == 127 for c in value), f'Control character in {name}')
    return value

def normalize_url(value):
    plain(value, 'URL', 2048)
    require(not any(c.isspace() for c in value) and '\\' not in value, 'URL contains whitespace or backslash')
    u = urlsplit(value)
    require(u.scheme == 'https' and u.hostname is not None, 'Use a public HTTPS URL')
    require(u.username is None and u.password is None, 'URL credentials are forbidden')
    require(u.port in (None, 443), 'Only the default HTTPS port is allowed')
    host = u.hostname.lower().rstrip('.')
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError('IP address URLs are not accepted')
    require(len(host) <= 253 and '.' in host and all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', x) for x in host.split('.')), 'Use a public DNS hostname')
    require(not host.endswith(('.local', '.localhost', '.internal', '.test', '.invalid', '.example', '.lan', '.home', '.onion')), 'Private or special-use hostname is forbidden')
    require(not host.split('.')[-1].isdigit(), 'Numeric hostnames are forbidden')
    query = parse_qsl(u.query, keep_blank_values=True)
    sensitive = {'token', 'access_token', 'api_key', 'key', 'signature', 'sig', 'password', 'auth'}
    require(not any(k.lower() in sensitive or k.lower().startswith('x-amz-') for k, _ in query), 'Do not submit signed or credential-bearing URLs')
    query = sorted((k, v) for k, v in query if not k.lower().startswith('utm_') and k.lower() not in {'fbclid', 'gclid'})
    # Normalize escaped unreserved characters, then encode delimiters unsafe in Markdown/HTML.
    path = re.sub(r'%([0-9a-fA-F]{2})', lambda m: chr(int(m[1],16)) if chr(int(m[1],16)) in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~' else '%'+m[1].upper(), u.path or '/')
    path = quote(path, safe='/%:@!$&*+,;=-._~')
    return urlunsplit(('https', host, path, urlencode(query), ''))

def load_base(root=ROOT):
    areas = json.loads((root/'catalogue/areas.json').read_text())
    caps = json.loads((root/'catalogue/capabilities.json').read_text())
    require(isinstance(areas,list) and isinstance(caps,list), 'Catalogues must be arrays')
    require({a['id'] for a in areas} == {'L1','L2','L3','L4','L5','A','B','C','IC','DD'}, 'Architecture areas must preserve the five layers, three spines and two cores')
    require(len(areas)==10, 'Duplicate architecture area')
    ids=set()
    for a in areas:
        require((root/'docs'/a['page']).is_file(), 'Missing area page')
    for c in caps:
        require(set(c)=={'id','name','area','definition','acceptance','status','page'}, 'Invalid capability fields')
        require(re.fullmatch(r'[a-z][a-z0-9-]{2,80}',c['id']) and c['id'] not in ids, 'Invalid or duplicate capability ID')
        ids.add(c['id'])
        require(c['area'] in {a['id'] for a in areas}, 'Unknown area')
        require(c['status'] in {'planned','in-progress','complete'}, 'Invalid capability status')
        for key in ('name','definition','acceptance'): plain(c[key],key)
        require(c['page']==f"capabilities/{c['id']}.md" and (root/'docs'/c['page']).is_file(), 'Invalid capability page')
        page=(root/'docs'/c['page']).read_text()
        require(page.startswith('# '+c['name']+'\n') and c['definition'] in page and c['acceptance'] in page, 'Capability page differs from canonical definition')
    return areas,caps

def validate_resource(r, cap_ids):
    require(isinstance(r,dict), 'Resource must be an object')
    required={'id','title','url','summary','capabilities','status','added','reviewed_by','reviewed_on','retirement_reason'}
    require(set(r)==required or set(r)==required|{'source_issue'}, 'Invalid resource fields')
    require(isinstance(r['id'],str) and re.fullmatch(r'[a-z][a-z0-9-]{2,80}',r['id']), 'Invalid resource ID')
    for field in ('title','summary'): plain(r[field],field)
    require(r['url']==normalize_url(r['url']), 'URL must be normalized')
    require(isinstance(r['capabilities'],list) and len(r['capabilities'])<=20 and all(isinstance(x,str) for x in r['capabilities']), 'Invalid capability references')
    require(len(set(r['capabilities']))==len(r['capabilities']) and set(r['capabilities'])<=cap_ids, 'Unknown or duplicate capability reference')
    require(r['status'] in STATUSES, 'Invalid resource status')
    require(isinstance(r['added'],str) and dt.date.fromisoformat(r['added']).isoformat()==r['added'], 'Invalid added date')
    require(dt.date.fromisoformat(r['added'])<=dt.date.today(), 'Future added date')
    for field in ('reviewed_by','reviewed_on','retirement_reason'):
        require(isinstance(r[field],str), 'Invalid review field')
    if r['status'] in {'curated','retired'}:
        plain(r['reviewed_by'],'reviewer',100)
        require(r['capabilities'], 'Classify a resource before curation')
        require(r['added']<=r['reviewed_on']<=dt.date.today().isoformat(), 'Invalid review chronology')
        require(dt.date.fromisoformat(r['reviewed_on']).isoformat()==r['reviewed_on'], 'Invalid review date')
    else:
        require(not r['reviewed_by'] and not r['reviewed_on'], 'Candidate cannot claim review')
    if r['status']=='retired': plain(r['retirement_reason'],'retirement reason')
    else: require(not r['retirement_reason'], 'Only retired resources have retirement reasons')
    if 'source_issue' in r: require(type(r['source_issue']) is int and r['source_issue']>0,'Invalid issue number')

def validate(root=ROOT):
    areas,caps=load_base(root)
    resources=[]; ids=set(); urls=set()
    for p in sorted((root/'catalogue/resources').glob('*.json')):
        r=json.loads(p.read_text());validate_resource(r,{c['id'] for c in caps})
        require(p.stem==r['id'], 'Filename must match resource ID')
        require(r['id'] not in ids and r['url'] not in urls, 'Duplicate resource ID or normalized URL')
        ids.add(r['id']);urls.add(r['url']);resources.append(r)
    return areas,caps,resources

def escape(value):
    return re.sub(r'([\\`*_[\]{}()#!|>])',r'\\\1',html.escape(value,quote=True))

def render(root=ROOT, check=False):
    areas,caps,resources=validate(root)
    lines=['# Capability catalogue','','Generated from `catalogue/capabilities.json`. Edit canonical metadata and run `python scripts/catalogue.py render`.','']
    for a in areas:
        lines += [f"## {a['name']}",'','| ID | Capability | Definition | Status |','| --- | --- | --- | --- |']
        for c in caps:
            if c['area']==a['id']:
                lines.append(f"| `{c['id']}` | [{escape(c['name'])}](../{c['page']}) | {escape(c['definition'])} | {c['status']} |")
        lines.append('')
    rlines=['# Resource catalogue','','Generated from `catalogue/resources/*.json`. Each normalized URL is stored once. Only curated entries are recommended here; candidates await human review.','','[Submit a URL](../contributing/resource-intake.md) to add to the review queue.','']
    for r in resources:
        if r['status']!='curated': continue
        rlines += [f"## {escape(r['title'])}",'',f"[Open resource]({r['url']}) — {escape(r['summary'])}",'', 'Capabilities: '+', '.join(f'[{cid}](../capabilities/{cid}.md)' for cid in r['capabilities']), '',f"Reviewed: {r['reviewed_on']} by {escape(r['reviewed_by'])}. Public link; original content remains with its publisher.",'']
    rlines += ['## Review queue','',f"{sum(r['status']=='candidate' for r in resources)} candidate(s); {sum(r['status']=='retired' for r in resources)} retired resource(s). Inspect canonical records and pull requests for review history."]
    for path, content in [('docs/catalogues/capabilities.md',lines),('docs/catalogues/resources.md',rlines)]:
        p=root/path; text='\n'.join(content).strip()+'\n'
        if check: require(p.exists() and p.read_text()==text, f'Stale generated page: {path}')
        else: p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['validate','render']);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    try:
        if args.command=='validate':
            a,c,r=validate();print(f'Validated {len(a)} areas, {len(c)} capabilities and {len(r)} resources')
        else: render(check=args.check);print('Generated catalogue pages are current' if args.check else 'Rendered catalogue pages')
    except (ValueError, KeyError, TypeError) as e:
        parser.exit(1, f'Validation failed: {e}\n')
