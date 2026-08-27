from .llm_client import ClaudeClient
from .prompt_builder import sql_prompt


def generate_sql(question: str, schema: str, client: ClaudeClient) -> str:
    sql = client.generate(sql_prompt(question, schema), max_tokens=1000)
    return sql.replace('```sql', '').replace('```', '').strip()
