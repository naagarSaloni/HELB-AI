
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.rag.retriever import retrieve_documents


def main():
    queries = [
        "How do I apply for a HELB loan?",
        "What are the requirements for an undergraduate loan?",
        "How do I repay my HELB loan?",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print(f"QUESTION: {query}")
        print("=" * 70)

        documents = retrieve_documents(query, k=3)

        if not documents:
            print("NO DOCUMENTS FOUND")
            continue

        for index, document in enumerate(documents, start=1):
            print(f"\n--- RESULT {index} ---")

            print("Source:", document.metadata.get("source_name"))
            print("URL:", document.metadata.get("source"))
            print("Chunk:", document.metadata.get("chunk_index"))

            print("\nContent:")
            print(document.page_content[:1000])


if __name__ == "__main__":
    main()
