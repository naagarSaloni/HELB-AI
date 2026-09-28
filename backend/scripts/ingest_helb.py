import hashlib
import sys
from pathlib import Path
from typing import List

import certifi
import requests
import urllib3
from bs4 import BeautifulSoup
from langchain_core.documents import Document


# ============================================================
# DISABLE SSL WARNING
# ============================================================

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ============================================================
# BACKEND PATH
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from app.rag.splitter import split_documents
from app.rag.vectorstore import get_vectorstore


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

PROJECT_DIR = BACKEND_DIR.parent

RAW_WEB_DIR = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "web_pages"
)


# ============================================================
# OFFICIAL HELB SOURCES
# ============================================================

HELB_SOURCES = [
    {
        "name": "HELB Home",
        "url": "https://www.helb.co.ke/",
    },
    {
        "name": "Students FAQs",
        "url": "https://www.helb.co.ke/faqs/students-faqs/",
    },
    {
        "name": "Loanees FAQs",
        "url": "https://www.helb.co.ke/faqs/loanees-faqs/",
    },
    {
        "name": "Undergraduate Loans",
        "url": "https://www.helb.co.ke/helb-products/helb-loans/undergraduate-loans/",
    },
    {
        "name": "TVET Loans",
        "url": "https://www.helb.co.ke/helb-products/helb-loans/tvet-loans/",
    },
    {
        "name": "HELB Loan Repayment",
        "url": "https://www.helb.co.ke/repay-loan/helb-loan-repayment/",
    },
    {
        "name": "Terms and Conditions",
        "url": "https://www.helb.co.ke/terms-and-conditions/",
    },
    {
        "name": "Post Graduate Scholarship",
        "url": "https://www.helb.co.ke/helb-products/helb-scholarships/post-graduate-scholarship/",
    },
    {
        "name": "Deadlines",
        "url": "https://www.helb.co.ke/deadlines/",
    },
]


# ============================================================
# HTTP HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,"
        "application/xhtml+xml,"
        "application/xml;q=0.9,"
        "image/avif,"
        "image/webp,"
        "image/apng,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


# ============================================================
# DOWNLOAD PAGE
# ============================================================

def fetch_page(url: str) -> str:

    print()
    print("-" * 80)
    print(f"Downloading: {url}")

    # --------------------------------------------------------
    # Attempt 1: normal SSL
    # --------------------------------------------------------

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        response.raise_for_status()

        print("Downloaded successfully.")

        return response.text

    except requests.exceptions.SSLError:

        print(
            "Normal SSL verification failed."
        )

    except requests.exceptions.RequestException as error:

        print(
            f"Normal request failed: {error}"
        )


    # --------------------------------------------------------
    # Attempt 2: certifi
    # --------------------------------------------------------

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
            verify=certifi.where(),
        )

        response.raise_for_status()

        print(
            "Downloaded successfully using certifi."
        )

        return response.text

    except requests.exceptions.SSLError:

        print(
            "Certifi SSL verification also failed."
        )

    except requests.exceptions.RequestException as error:

        print(
            f"Certifi request failed: {error}"
        )


    # --------------------------------------------------------
    # Attempt 3: controlled fallback
    # --------------------------------------------------------

    print(
        "Using controlled SSL fallback..."
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
        verify=False,
    )

    response.raise_for_status()

    print(
        "Downloaded successfully using SSL fallback."
    )

    return response.text


# ============================================================
# CLEAN HTML
# ============================================================

def clean_html(html: str) -> str:

    soup = BeautifulSoup(
        html,
        "html.parser",
    )


    # --------------------------------------------------------
    # Remove elements that are definitely not knowledge
    # --------------------------------------------------------

    tags_to_remove = [
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "canvas",
        "video",
        "audio",
        "form",
        "button",
        "input",
        "textarea",
        "select",
        "option",
    ]

    for tag in soup.find_all(tags_to_remove):

        try:
            tag.decompose()
        except Exception:
            pass


    # --------------------------------------------------------
    # Extract visible text
    # --------------------------------------------------------

    raw_text = soup.get_text(
        separator="\n"
    )


    # --------------------------------------------------------
    # Clean individual lines
    # --------------------------------------------------------

    cleaned_lines = []

    previous_line = ""

    for raw_line in raw_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue


        # Replace non-breaking spaces
        line = line.replace(
            "\xa0",
            " ",
        )


        # Normalize multiple spaces
        line = " ".join(
            line.split()
        )


        if not line:
            continue


        # Ignore pure symbols
        if line in {
            "|",
            "-",
            "—",
            "–",
            "•",
            "→",
            "←",
            "»",
            "«",
            ">",
            "<",
            "/",
        }:
            continue


        # Ignore lines containing no useful characters
        if not any(
            character.isalnum()
            for character in line
        ):
            continue


        # Remove immediately repeated lines
        if line == previous_line:
            continue


        cleaned_lines.append(line)

        previous_line = line


    # --------------------------------------------------------
    # Remove duplicate lines while preserving order
    # --------------------------------------------------------

    final_lines = []

    seen = set()

    for line in cleaned_lines:

        normalized = line.lower()

        if normalized in seen:
            continue

        seen.add(normalized)

        final_lines.append(line)


    return "\n".join(
        final_lines
    )


# ============================================================
# CREATE SAFE FILE NAME
# ============================================================

def create_file_name(
    source_name: str,
) -> str:

    filename = source_name.lower()

    filename = filename.replace(
        " ",
        "_",
    )

    filename = filename.replace(
        "/",
        "_",
    )

    filename = filename.replace(
        "\\",
        "_",
    )

    filename = filename.replace(
        ":",
        "_",
    )

    return (
        f"{filename}.txt"
    )


# ============================================================
# SAVE CLEAN CONTENT
# ============================================================

def save_clean_text(
    source_name: str,
    text: str,
) -> Path:

    RAW_WEB_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        RAW_WEB_DIR
        / create_file_name(
            source_name
        )
    )

    file_path.write_text(
        text,
        encoding="utf-8",
    )

    return file_path


# ============================================================
# CREATE LANGCHAIN DOCUMENT
# ============================================================

def create_document(
    source_name: str,
    url: str,
    text: str,
) -> Document:

    return Document(
        page_content=text,
        metadata={
            "source_name": source_name,
            "source": url,
            "source_type": "official_helb_website",
        },
    )


# ============================================================
# DOWNLOAD + CLEAN ALL SOURCES
# ============================================================

def download_sources() -> List[Document]:

    documents = []

    print()
    print("=" * 80)
    print("DOWNLOADING OFFICIAL HELB SOURCES")
    print("=" * 80)

    for source in HELB_SOURCES:

        name = source["name"]
        url = source["url"]

        try:

            # ----------------------------------------------
            # Download
            # ----------------------------------------------

            html = fetch_page(
                url
            )


            # ----------------------------------------------
            # Clean
            # ----------------------------------------------

            print(
                f"Cleaning: {name}"
            )

            cleaned_text = clean_html(
                html
            )


            # ----------------------------------------------
            # Validate
            # ----------------------------------------------

            if not cleaned_text.strip():

                print(
                    f"WARNING: "
                    f"No usable text found for {name}"
                )

                continue


            # ----------------------------------------------
            # Save cleaned text
            # ----------------------------------------------

            file_path = save_clean_text(
                name,
                cleaned_text,
            )

            print(
                f"Saved cleaned content: "
                f"{file_path}"
            )

            print(
                f"Characters: "
                f"{len(cleaned_text):,}"
            )


            # ----------------------------------------------
            # Create Document
            # ----------------------------------------------

            document = create_document(
                source_name=name,
                url=url,
                text=cleaned_text,
            )

            documents.append(
                document
            )

            print(
                f"SUCCESS: {name}"
            )

        except Exception as error:

            print()
            print(
                f"FAILED: {name}"
            )

            print(
                f"Reason: {error}"
            )


    print()
    print("=" * 80)
    print(
        f"Successfully loaded "
        f"{len(documents)} / "
        f"{len(HELB_SOURCES)} sources"
    )
    print("=" * 80)

    return documents


# ============================================================
# CREATE UNIQUE DOCUMENT ID
# ============================================================

def create_document_id(
    document: Document,
    index: int,
) -> str:

    source = document.metadata.get(
        "source",
        "",
    )

    content = document.page_content

    unique_text = (
        f"{source}|"
        f"{index}|"
        f"{content}"
    )

    return hashlib.sha256(
        unique_text.encode(
            "utf-8"
        )
    ).hexdigest()


# ============================================================
# CLEAR EXISTING CHROMA COLLECTION
# ============================================================

def clear_existing_collection():

    print()
    print("=" * 80)
    print("CLEARING OLD CHROMADB DATA")
    print("=" * 80)

    vectorstore = get_vectorstore()

    collection = vectorstore._collection

    existing = collection.get()

    existing_ids = existing.get(
        "ids",
        [],
    )

    if existing_ids:

        collection.delete(
            ids=existing_ids
        )

        print(
            f"Deleted "
            f"{len(existing_ids)} old chunks."
        )

    else:

        print(
            "No old chunks found."
        )


# ============================================================
# SPLIT + STORE DOCUMENTS
# ============================================================

def ingest_documents(
    documents: List[Document],
):

    if not documents:

        print()
        print(
            "No documents available for ingestion."
        )

        return


    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print("SPLITTING DOCUMENTS")
    print("=" * 80)

    chunks = split_documents(
        documents
    )

    print(
        f"Created "
        f"{len(chunks)} chunks."
    )


    # --------------------------------------------------------
    # Add metadata
    # --------------------------------------------------------

    for index, chunk in enumerate(chunks):

        chunk.metadata[
            "chunk_index"
        ] = index


    # --------------------------------------------------------
    # Clear old collection
    # --------------------------------------------------------

    clear_existing_collection()


    # --------------------------------------------------------
    # Create IDs
    # --------------------------------------------------------

    ids = []

    for index, chunk in enumerate(chunks):

        document_id = create_document_id(
            chunk,
            index,
        )

        ids.append(
            document_id
        )


    # --------------------------------------------------------
    # Add to Chroma
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print("ADDING DOCUMENTS TO CHROMADB")
    print("=" * 80)

    vectorstore = get_vectorstore()

    vectorstore.add_documents(
        documents=chunks,
        ids=ids,
    )

    print(
        f"Successfully stored "
        f"{len(chunks)} chunks."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("#" * 80)
    print("# HELB AI SUPPORT AGENT")
    print("# KNOWLEDGE INGESTION PIPELINE")
    print("#" * 80)


    # --------------------------------------------------------
    # Create directories
    # --------------------------------------------------------

    RAW_WEB_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    # --------------------------------------------------------
    # Download official sources
    # --------------------------------------------------------

    documents = download_sources()


    # --------------------------------------------------------
    # Ingest into Chroma
    # --------------------------------------------------------

    ingest_documents(
        documents
    )


    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print()
    print("#" * 80)
    print("# INGESTION COMPLETED")
    print("#" * 80)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()