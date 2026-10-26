"""Parse issue data as data only. Never fetch submitted URLs or execute submitted text."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
try:
    from .catalogue import ROOT, normalize_url, validate, validate_resource, require
except ImportError:
    from catalogue import ROOT, normalize_url, validate, validate_resource, require

def parse_issue(issue, root=ROOT):
    require(type(issue.get('number')) is int and issue['number']>0, 'Invalid issue number')
    require('pull_request' not in issue, 'Expected an issue, not a pull request')
    body=issue.get('body') or ''
    require(isinstance(body,str) and len(body)<=12000, 'Invalid issue body')
    parts=re.split(r'^### (.+)\s*$',body,flags=re.M)
    fields={}
    for i in range(1,len(parts),2):
        name=parts[i].strip()
        require(name not in fields, 'Duplicate form field')
        fields[name]=parts[i+1].strip()
    require(set(fields)<= {'Resource URL','Why it matters','Capability IDs (optional)'}, 'Unexpected form field; use the resource issue form')
    url=normalize_url(fields.get('Resource URL',''))
    summary=fields.get('Why it matters','')
    if summary in ('','_No response_'): summary='Awaiting maintainer summary and relevance review.'
    refs=fields.get('Capability IDs (optional)','')
    caps=[] if refs in ('','_No response_') else [x.strip() for x in refs.split(',')]
    _,known,existing=validate(root)
    require(url not in {x['url'] for x in existing}, 'This normalized URL is already in the catalogue')
    r={'id':f"intake-{issue['number']}",'title':url.split('/')[2], 'url':url,'summary':summary,'capabilities':caps,'status':'candidate','added':dt.date.today().isoformat(),'reviewed_by':'','reviewed_on':'','retirement_reason':'','source_issue':issue['number']}
    validate_resource(r,{c['id'] for c in known})
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('event');p.add_argument('--output',required=True);p.add_argument('--issue-json',action='store_true');args=p.parse_args()
    try:
        data=json.loads(Path(args.event).read_text());r=parse_issue(data if args.issue_json else data['issue'])
        out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
        (out/(r['id']+'.json')).write_text(json.dumps(r,indent=2)+'\n')
        print('Validated candidate metadata; human review required before curation.')
    except (ValueError,KeyError,TypeError) as e:
        # Error messages are fixed validation strings, not untrusted issue content.
        p.exit(1,f'Intake validation failed: {e}\n')
