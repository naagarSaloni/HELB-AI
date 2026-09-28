from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


CHROMA_DIR = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "chroma"
)

COLLECTION_NAME = "helb_knowledge"


@lru_cache(maxsize=1)
def get_vectorstore():

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def add_documents(documents):

    vectorstore = get_vectorstore()

    vectorstore.add_documents(documents)


def get_retriever(k: int = 3):

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k
        },
    )