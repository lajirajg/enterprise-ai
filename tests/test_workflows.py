"""Security boundaries that must survive future workflow edits."""
from pathlib import Path
import re
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[1]
class WorkflowTests(unittest.TestCase):
    def load(self,name):
        return yaml.load((ROOT/'.github/workflows'/name).read_text(),Loader=yaml.BaseLoader)
    def test_issue_job_cannot_write_or_interpolate_body_into_shell(self):
        w=self.load('resource-intake.yml')
        self.assertEqual(w['permissions'],{'contents':'read'})
        self.assertNotIn('pull_request_target',w['on'])
        for step in w['jobs']['validate']['steps']:
            if 'run' in step:self.assertNotIn('${{',step['run'])
    def test_actions_are_pinned_and_checkout_has_no_persistent_credentials(self):
        for p in (ROOT/'.github/workflows').glob('*.yml'):
            w=self.load(p.name)
            for job in w['jobs'].values():
                for step in job['steps']:
                    if 'uses' in step:
                        self.assertRegex(step['uses'],r'^[\w/-]+@[a-f0-9]{40}$')
                        if step['uses'].startswith('actions/checkout@'):
                            self.assertEqual(step['with']['persist-credentials'],'false')
    def test_review_is_manual_and_default_branch_only(self):
        w=self.load('review-resource.yml')
        self.assertEqual(set(w['on']),{'workflow_dispatch'})
        job=w['jobs']['propose']
        self.assertEqual(job['if'],"github.ref == 'refs/heads/main'")
        self.assertEqual(job['steps'][0]['with']['ref'],'main')
    def test_pages_has_separate_deploy_permissions(self):
        w=self.load('pages.yml')
        self.assertEqual(w['permissions'],{'contents':'read'})
        self.assertEqual(w['jobs']['deploy']['permissions'],{'pages':'write','id-token':'write'})
