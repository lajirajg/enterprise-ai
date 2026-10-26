import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from scripts import propose_resource as proposal
from scripts.catalogue import ROOT

class ProposalTests(unittest.TestCase):
    def test_invalid_issue_number_never_calls_git_or_github(self):
        with patch.dict('os.environ',{'ISSUE_NUMBER':'1; echo unsafe','GITHUB_REPOSITORY':'owner/repo'}), patch.object(proposal,'run') as run:
            with self.assertRaises(ValueError):proposal.main()
            run.assert_not_called()
    def test_repeat_dispatch_does_not_overwrite_reviewed_branch(self):
        with patch.dict('os.environ',{'ISSUE_NUMBER':'12','GITHUB_REPOSITORY':'owner/repo'}), patch.object(proposal,'run',return_value='[{"url":"https://github.com/owner/repo/pull/1"}]') as run:
            proposal.main();self.assertEqual(run.call_count,1)
    def test_candidate_proposal_with_untrusted_summary(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);shutil.copytree(ROOT/'catalogue',root/'catalogue');shutil.copytree(ROOT/'docs',root/'docs')
            issue={'number':12,'state':'open','body':'### Resource URL\n\nhttps://www.python.org/about/\n\n### Why it matters\n\n$(echo injected) <script>not executable</script>'}
            calls=[]
            def fake_run(*args):
                calls.append(args)
                if args[:3]==('gh','pr','list'):return '[]'
                if args[:2]==('gh','api'):return json.dumps(issue)
                if args[:3]==('gh','pr','create'):return 'https://github.com/owner/repo/pull/1'
                return ''
            with patch.dict('os.environ',{'ISSUE_NUMBER':'12','GITHUB_REPOSITORY':'owner/repo'}),patch.object(proposal,'ROOT',root),patch.object(proposal,'run',side_effect=fake_run):
                proposal.main()
            candidate=json.loads((root/'catalogue/resources/intake-12.json').read_text())
            self.assertEqual(candidate['status'],'candidate')
            self.assertIn('$(echo injected)',candidate['summary'])
            self.assertTrue(any(args[:3]==('gh','pr','create') and '--draft' in args for args in calls))
            self.assertFalse(any('injected' in arg for args in calls for arg in args))
            self.assertFalse(any('--force' in args or '--force-with-lease' in args for args in calls))
