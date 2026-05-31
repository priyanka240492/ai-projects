"""
app.py
Interactive CLI to query your local RAG pipeline.

Usage:
    python -m rag_pipeline.app           # via module
    rag-chat                             # via installed CLI (pyproject.toml)
    rag-chat -q "What is the employee ID?"  # single question mode
"""
import argparse

from rag_pipeline.rag import load_retriever, build_rag_chain, ask


def cli_loop(chain, retriever) -> None:
    """Interactive question-answer loop."""
    print("\nReady! Type your questions below (type 'quit' to exit)\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not question:
            continue
        result = ask(question, chain, retriever)
        print(f"\nAssistant: {result['answer']}")
        print(f"Source   : {', '.join(result['sources'])}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local RAG CLI")
    parser.add_argument("-q", "--question", help="Single question mode")
    args = parser.parse_args()

    print("\n[rag] Loading retriever and building chain...")
    retriever = load_retriever()
    chain     = build_rag_chain(retriever)

    if args.question:
        result = ask(args.question, chain, retriever)
        print(f"\nAssistant: {result['answer']}")
        print(f"Source   : {', '.join(result['sources'])}")
    else:
        cli_loop(chain, retriever)


if __name__ == "__main__":
    main()
