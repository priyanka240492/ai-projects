import streamlit as st
from src.orchestrator import QueryOrchestrator
from src.config import ANTHROPIC_MODEL

st.set_page_config(page_title='NL-to-SQL Assistant', page_icon='🧠', layout='wide')
st.title('🧠 Natural Language to SQL')
st.caption(f'Intent-aware data assistant · Claude · {ANTHROPIC_MODEL}')

if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = QueryOrchestrator()

question = st.chat_input('Ask a question about the sample data...')
if question:
    st.chat_message('user').write(question)
    with st.chat_message('assistant'):
        with st.spinner('Classifying intent, generating and validating...'):
            try:
                result = st.session_state.orchestrator.run(question)
                st.caption(f"Intent: {result['intent']}")
                st.write(result['answer'])
                if result['sql']:
                    with st.expander('Generated SQL'):
                        st.code(result['sql'], language='sql')
                if result['rows']:
                    st.dataframe(result['rows'], use_container_width=True)
            except Exception as exc:
                st.error(str(exc))
