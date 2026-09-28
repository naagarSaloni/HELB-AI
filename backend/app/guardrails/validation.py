FALLBACK_ANSWER = (
    "I couldn't find enough reliable information in the "
    "available official HELB information to answer that question. "
    "Your question has been escalated to human support."
)


INSUFFICIENT_INFORMATION_PHRASES = [
    "i couldn't find enough information",
    "i could not find enough information",
    "i couldn't find enough reliable information",
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
    sources: list,
) -> dict:
    """
    Validate whether the generated answer has
    supporting official HELB sources.

    If reliable official evidence is unavailable,
    the response is marked for human escalation.
    """

    # --------------------------------------------------
    # 1. No sources retrieved
    # --------------------------------------------------

    if not sources:
        return {
            "supported": False,
            "answer": FALLBACK_ANSWER,
            "sources": [],
            "reason": "No supporting HELB documents were retrieved.",
        }

    # --------------------------------------------------
    # 2. Keep only official HELB sources
    # --------------------------------------------------

    official_sources = []

    for source in sources:
        url = str(source.get("url", "")).lower()

        if "helb.co.ke" in url:
            official_sources.append(source)

    # --------------------------------------------------
    # 3. No official HELB source
    # --------------------------------------------------

    if not official_sources:
        return {
            "supported": False,
            "answer": FALLBACK_ANSWER,
            "sources": [],
            "reason": "No official HELB source was retrieved.",
        }

    # --------------------------------------------------
    # 4. Check whether the RAG answer itself says
    #    that information is unavailable
    # --------------------------------------------------

    normalized_answer = " ".join(
        str(answer).lower().split()
    )

    for phrase in INSUFFICIENT_INFORMATION_PHRASES:

        if phrase in normalized_answer:
            return {
                "supported": False,
                "answer": FALLBACK_ANSWER,
                "sources": official_sources,
                "reason": (
                    "The available official HELB "
                    "information does not contain enough "
                    "evidence to answer the question."
                ),
            }

    # --------------------------------------------------
    # 5. Evidence exists
    # --------------------------------------------------

    return {
        "supported": True,
        "answer": answer,
        "sources": official_sources,
        "reason": (
            "The response has supporting official "
            "HELB sources."
        ),
    }