from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[1] / 'prompts'


def _load(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding='utf-8')


def intent_prompt(question: str) -> str:
    return _load('intent_classification.txt').format(question=question)


def sql_prompt(question: str, schema: str) -> str:
    return _load('sql_generation.txt').format(question=question, schema=schema)


def non_data_prompt(question: str) -> str:
    return _load('non_data_response.txt').format(question=question)
