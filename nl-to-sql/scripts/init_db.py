import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'data' / 'app.db'
SEED = ROOT / 'data' / 'seed.sql'

DB.parent.mkdir(parents=True, exist_ok=True)
connection = sqlite3.connect(DB)
connection.executescript(SEED.read_text(encoding='utf-8'))
connection.commit()
connection.close()
print(f'Initialized {DB}')
