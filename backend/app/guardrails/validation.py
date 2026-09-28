from typing import Dict, Any, List


FALLBACK_ANSWER = (
    "I could not find enough reliable information in the available "
    "official HELB documents to answer this question. "
    "I recommend contacting HELB support for further assistance."
)


INSUFFICIENT_INFORMATION_PHRASES = [
    "i could not find enough information",
    "i could not find enough reliable information",
    "not enough information",
    "insufficient information",
    "information is not available",
    "not available in the provided documents",
    "not found in the provided documents",
    "not found in the available documents",
    "documents do not contain enough information",
]


def validate_evidence(
    answer: str,
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:

    # ---------------------------------------------------------
    # 1. No sources = unsupported
    # ---------------------------------------------------------
    if not sources:
        return {
            "supported": False,
            "answer": FALLBACK_ANSWER,
            "sources": [],
            "reason": "No supporting sources were retrieved.",
        }

    # ---------------------------------------------------------
    # 2. Remove duplicate sources
    # ---------------------------------------------------------
    unique_sources = []
    seen = set()

    for source in sources:
        name = source.get("name", "")
        url = source.get("url", "")

        key = (name, url)

        if key not in seen:
            seen.add(key)
            unique_sources.append(source)

    # ---------------------------------------------------------
    # 3. Keep only official HELB sources
    # ---------------------------------------------------------
    official_sources = []

    for source in unique_sources:
        url = source.get("url", "").lower()

        if "helb.co.ke" in url:
            official_sources.append(source)

    # ---------------------------------------------------------
    # 4. No official HELB source = unsupported
    # ---------------------------------------------------------
    if not official_sources:
        return {
            "supported": False,
            "answer": FALLBACK_ANSWER,
            "sources": [],
            "reason": "No official HELB source supports the response.",
        }

    # ---------------------------------------------------------
    # 5. Detect when the LLM itself says evidence is missing
    # ---------------------------------------------------------
    normalized_answer = " ".join(
        answer.lower().split()
    )

    for phrase in INSUFFICIENT_INFORMATION_PHRASES:

        if phrase in normalized_answer:

            return {
                "supported": False,
                "answer": FALLBACK_ANSWER,
                "sources": official_sources,
                "reason": (
                    "The retrieved official HELB documents do not "
                    "contain enough information to answer the question."
                ),
            }

    # ---------------------------------------------------------
    # 6. Evidence is available
    # ---------------------------------------------------------
    return {
        "supported": True,
        "answer": answer,
        "sources": official_sources,
        "reason": "Response has supporting official HELB sources.",
    }