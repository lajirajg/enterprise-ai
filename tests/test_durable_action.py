import sqlite3
import tempfile
import unittest
from pathlib import Path
from labs.durable_action import complete

class DurableActionTests(unittest.TestCase):
    def test_replay_after_reopen_has_one_effect(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'work.db'
            self.assertEqual(complete(p,'case-1','synthetic invoice'),complete(p,'case-1','synthetic invoice'))
            with sqlite3.connect(p) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM actions').fetchone()[0],1)
            with self.assertRaises(ValueError): complete(p,'case-1','different invoice')
            complete(p,'case-2','second invoice')
            with sqlite3.connect(p) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM actions').fetchone()[0],2)
