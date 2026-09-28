from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


CHROMA_DIR = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "chroma"
)

COLLECTION_NAME = "helb_knowledge"


def get_vectorstore() -> Chroma:
    """
    Return the persistent HELB ChromaDB vector store.
    """

    embeddings = get_embeddings()

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    return vectorstore


def add_documents(
    documents: List[Document],
) -> None:
    """
    Add document chunks to ChromaDB.
    """

    vectorstore = get_vectorstore()

    vectorstore.add_documents(documents)


def get_retriever(
    k: int = 5,
):
    """
    Create a similarity retriever from ChromaDB.
    """

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        },
    )