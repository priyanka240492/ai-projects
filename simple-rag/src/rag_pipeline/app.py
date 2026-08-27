import argparse
from rag_pipeline.rag import load_retriever, build_rag_chain, ask


def main():
    parser = argparse.ArgumentParser(description='Local RAG CLI')
    parser.add_argument('-q', '--question')
    args = parser.parse_args()
    retriever = load_retriever()
    chain = build_rag_chain(retriever)
    if args.question:
        result = ask(args.question, chain, retriever)
        print(result['answer'])
        print('Sources:', ', '.join(result['sources']))
        return
    while True:
        question = input('You: ').strip()
        if question.lower() in {'quit', 'exit', 'q'}:
            break
        if question:
            result = ask(question, chain, retriever)
            print('\nAssistant:', result['answer'])
            print('Sources:', ', '.join(result['sources']))


if __name__ == '__main__':
    main()
