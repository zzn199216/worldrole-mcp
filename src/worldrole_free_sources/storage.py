"""Private per-user state, separate from the repository and hosted WorldRole."""
import os
import sqlite3
from pathlib import Path


def data_dir():
    base = Path(os.environ.get('WORLDROLE_DATA_DIR') or
                (Path(os.environ.get('LOCALAPPDATA') or Path.home() / '.local/share') / 'WorldRole'))
    if not base.is_absolute():
        raise ValueError('WORLDROLE_DATA_DIR must be an absolute private directory')
    base.mkdir(parents=True, exist_ok=True, mode=0o700)
    return base


def connect():
    path = data_dir() / 'companion.sqlite3'
    db = sqlite3.connect(path, timeout=30)
    if os.name != 'nt':
        path.chmod(0o600)
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, at REAL, payload TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS applications (id TEXT PRIMARY KEY, job_url TEXT UNIQUE, payload TEXT)')
    return db
