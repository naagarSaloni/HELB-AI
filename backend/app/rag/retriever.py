from typing import List

from langchain_core.documents import Document

from app.rag.vectorstore import get_retriever


def retrieve_documents(
    query: str,
    k: int = 5,
) -> List[Document]:
    """
    Retrieve the most relevant HELB documents
    for a user query.
    """

    retriever = get_retriever(k=k)

    documents = retriever.invoke(query)

    return documents