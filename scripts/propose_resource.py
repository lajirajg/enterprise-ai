"""Maintainer-dispatched proposal; all subprocess arguments are fixed or validated."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
try:
    from .catalogue import ROOT, render, validate, require
    from .intake import parse_issue
except ImportError:
    from catalogue import ROOT, render, validate, require
    from intake import parse_issue

def run(*args):
    return subprocess.check_output(args,cwd=ROOT,text=True).strip()

def main():
    number=os.environ.get('ISSUE_NUMBER','')
    require(re.fullmatch(r'[1-9][0-9]{0,9}',number), 'Issue number must be a positive integer')
    repo=os.environ.get('GITHUB_REPOSITORY','')
    require(re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo), 'Invalid repository')
    branch='resource-intake/'+number
    existing=json.loads(run('gh','pr','list','--repo',repo,'--head',branch,'--state','all','--json','url'))
    if existing:
        print('A proposal already exists: '+existing[0]['url']);return
    remote=run('git','ls-remote','--heads','origin','refs/heads/'+branch)
    require(not remote, 'Candidate branch already exists; inspect it and open a PR manually or remove it before retrying')
    issue=json.loads(run('gh','api',f'repos/{repo}/issues/{number}'))
    require(issue.get('state')=='open', 'Issue is closed')
    resource=parse_issue(issue, root=ROOT)
    path=ROOT/'catalogue/resources'/(resource['id']+'.json')
    require(not path.exists(), 'Candidate ID already exists')
    path.write_text(json.dumps(resource,indent=2)+'\n')
    render(ROOT);validate(ROOT)
    run('git','switch','-c',branch)
    run('git','config','user.name','github-actions[bot]')
    run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    run('git','add',str(path),str(ROOT/'docs/catalogues/resources.md'))
    run('git','commit','-m','Add resource candidate from issue #'+number)
    # gh uses GH_TOKEN as its credential helper; no token is put in a URL or logs.
    run('gh','auth','setup-git')
    run('git','push','origin','HEAD:refs/heads/'+branch)
    body='Candidate from #'+number+'. Review the public source, title, summary, capability mapping and publication rights. This is not curated and will not appear in the recommended list. Add review metadata and regenerate catalogue pages before marking it curated. No automatic merge or approval.'
    with tempfile.TemporaryDirectory() as directory:
        bodyfile=Path(directory)/'body.md';bodyfile.write_text(body+'\n')
        print(run('gh','pr','create','--repo',repo,'--base','main','--head',branch,'--draft','--title','Review resource candidate #'+number,'--body-file',str(bodyfile)))

if __name__=='__main__':
    main()
