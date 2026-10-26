import copy
import json
from pathlib import Path
import tempfile
import shutil
import unittest
from scripts.catalogue import ROOT, normalize_url, validate, validate_resource, render, escape
from scripts.intake import parse_issue

class CatalogueTests(unittest.TestCase):
    def issue(self,url='https://www.python.org/about/'):
        return {'number':42,'body':f'### Resource URL\n\n{url}\n\n### Why it matters\n\n_No response_\n\n### Capability IDs (optional)\n\n_No response_'}
    def test_repository_valid(self):
        validate();render(check=True)
    def test_url_normalization(self):
        self.assertEqual(normalize_url('https://EXAMPLE.com:443/%7Eguide?utm_source=x&b=2&a=1#part'),'https://example.com/~guide?a=1&b=2')
    def test_reject_unsafe_urls(self):
        for url in ['http://example.com','javascript:alert(1)','file:///tmp/a','https://127.0.0.1','https://[::1]','https://a.local','https://localhost','https://2130706433','https://127.1','https://user:pass@example.com','https://example.com:444','https://example.com/a\nb','https://example.com/?token=secret','https://example.com\\@evil.com']:
            with self.subTest(url=url),self.assertRaises(ValueError):normalize_url(url)
    def test_url_only_intake_is_candidate(self):
        r=parse_issue(self.issue());self.assertEqual(r['status'],'candidate');self.assertEqual(r['capabilities'],[])
    def test_duplicate_normalized_url(self):
        _,_,resources=validate()
        with self.assertRaises(ValueError):parse_issue(self.issue(resources[0]['url']+'#fragment'))
    def test_unknown_capability_and_duplicate_field(self):
        issue=self.issue();issue['body']=issue['body'].rsplit('_No response_',1)[0]+'missing-capability'
        with self.assertRaises(ValueError):parse_issue(issue)
        issue=self.issue();issue['body']+='\n### Resource URL\nhttps://evil.com/'
        with self.assertRaises(ValueError):parse_issue(issue)
    def test_untrusted_text_stays_data(self):
        issue=self.issue();issue['body']=issue['body'].replace('_No response_','$(touch /tmp/should-not-exist) <script>alert(1)</script>',1)
        r=parse_issue(issue)
        self.assertIn('$(touch',r['summary']);self.assertNotIn('<script>',escape(r['summary']))
    def test_review_required(self):
        r=parse_issue(self.issue());r['status']='curated'
        with self.assertRaises(ValueError):validate_resource(r,set())
    def test_unknown_fields_and_path_injection(self):
        r=parse_issue(self.issue());r['id']='../../escape'
        with self.assertRaises(ValueError):validate_resource(r,set())
        r=parse_issue(self.issue());r['execute']='shell'
        with self.assertRaises(ValueError):validate_resource(r,set())
    def test_candidate_not_published_and_stale_page_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copytree(ROOT/'catalogue',root/'catalogue');shutil.copytree(ROOT/'docs',root/'docs')
            r=parse_issue(self.issue());r['title']='UNREVIEWED_SENTINEL'
            (root/'catalogue/resources/intake-42.json').write_text(json.dumps(r))
            render(root)
            self.assertNotIn('UNREVIEWED_SENTINEL',(root/'docs/catalogues/resources.md').read_text())
            (root/'docs/catalogues/resources.md').write_text('stale')
            with self.assertRaises(ValueError):render(root,check=True)
    def test_invalid_review_date(self):
        _,caps,resources=validate();r=copy.deepcopy(resources[0]);r['reviewed_on']='2026-02-30'
        with self.assertRaises(ValueError):validate_resource(r,{c['id'] for c in caps})
