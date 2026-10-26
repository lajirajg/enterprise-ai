"""Database-local synthetic side effect; not an external API exactly-once guarantee."""
import sqlite3

def complete(db_path, work_id, payload):
    with sqlite3.connect(db_path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS actions (id TEXT PRIMARY KEY, payload TEXT, result TEXT)')
        db.execute('BEGIN IMMEDIATE')
        prior=db.execute('SELECT payload,result FROM actions WHERE id=?',(work_id,)).fetchone()
        if prior:
            if prior[0]!=payload:
                raise ValueError('Work ID reused with a different payload')
            return prior[1]
        result='accepted: '+payload
        db.execute('INSERT INTO actions VALUES (?,?,?)',(work_id,payload,result))
        return result
