from src.orchestrator import QueryOrchestrator


class FakeClient:
    def classify_intent(self, prompt):
        return {'intent': 'NON_DATA_QUERY', 'confidence': 1.0}

    def generate(self, prompt, max_tokens=500):
        return 'This is a general response.'


def test_non_data_query_is_not_sent_to_sql():
    result = QueryOrchestrator(FakeClient()).run('What is Python?')
    assert result['intent'] == 'NON_DATA_QUERY'
    assert result['sql'] is None
    assert result['answer'] == 'This is a general response.'
