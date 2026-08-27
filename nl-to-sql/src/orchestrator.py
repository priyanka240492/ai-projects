from .config import MAX_SQL_RETRIES
from .llm_client import ClaudeClient
from .prompt_builder import intent_prompt, non_data_prompt
from .schema_inspector import get_schema
from .sql_generator import generate_sql
from .sql_validator import validate_sql
from .sql_executor import execute_sql


class QueryOrchestrator:
    def __init__(self, client=None):
        self.client = client or ClaudeClient()

    def run(self, question: str) -> dict:
        intent = self.client.classify_intent(intent_prompt(question))
        kind = intent.get('intent', 'UNKNOWN')

        if kind == 'NON_DATA_QUERY':
            return {'intent': kind, 'sql': None, 'rows': [], 'answer': self.client.generate(non_data_prompt(question), max_tokens=500)}
        if kind in {'UNSAFE_QUERY', 'UNKNOWN'}:
            return {'intent': kind, 'sql': None, 'rows': [], 'answer': 'I can help with questions about the connected dataset, but I cannot execute unsafe or unsupported requests.'}

        schema = get_schema()
        last_error = ''
        for _ in range(MAX_SQL_RETRIES + 1):
            sql = generate_sql(question, schema, self.client)
            valid, message = validate_sql(sql, schema)
            if valid:
                try:
                    rows = execute_sql(sql)
                    return {'intent': kind, 'sql': sql, 'rows': rows, 'answer': f'Returned {len(rows)} row(s).'}
                except Exception as exc:
                    last_error = f'Execution error: {exc}'
            else:
                last_error = message
        return {'intent': kind, 'sql': sql, 'rows': [], 'answer': f'I could not produce a safe executable query. {last_error}'}
