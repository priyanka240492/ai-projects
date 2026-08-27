import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = Path(os.getenv('DATABASE_PATH', str(ROOT_DIR / 'data' / 'app.db')))
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-haiku-4-5-20251001')
MAX_SQL_RETRIES = int(os.getenv('MAX_SQL_RETRIES', '2'))
