
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


DATA_DIR = Path(__file__).resolve().parents[3] / "data"


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that are not useful knowledge
    remove_tags = [
        "script",
        "style",
        "noscript",
        "svg",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
        "button",
    ]

    for tag in remove_tags:
        for element in soup.find_all(tag):
            element.decompose()

    # Try to find the main page content
    main_content = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_=lambda x: x and "content" in str(x).lower())
    )

    if main_content:
        soup = main_content

    text = soup.get_text(separator="\n")

    cleaned_lines = []

    for line in text.splitlines():
        line = " ".join(line.split())

        if not line:
            continue

        # Remove common website navigation/UI text
        unwanted = {
            "twitter",
            "facebook-f",
            "youtube",
            "linkedin",
            "home",
            "quick links",
            "helb products",
            "helb loans",
            "leadership",
            "self serve",
            "get-in-touch",
            "compliance certificate",
        }

        if line.lower() in unwanted:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    for document in documents:
        document.metadata["source_type"] = "pdf"
        document.metadata["source"] = str(file_path)

    return documents


def load_text(file_path: str) -> List[Document]:
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    for document in documents:
        document.metadata["source_type"] = "text"
        document.metadata["source"] = str(file_path)

    return documents


def load_documents() -> List[Document]:
    documents = []

    pdf_directory = DATA_DIR / "raw" / "pdfs"
    text_directory = DATA_DIR / "raw" / "web_pages"

    if pdf_directory.exists():
        for file_path in pdf_directory.glob("*.pdf"):
            documents.extend(load_pdf(str(file_path)))

    if text_directory.exists():
        for file_path in text_directory.glob("*.txt"):
            documents.extend(load_text(str(file_path)))

    return documents
