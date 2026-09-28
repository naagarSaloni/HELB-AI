from typing import Literal

Intent = Literal["loan", "repayment", "knowledge"]


LOAN_KEYWORDS = [
    "loan",
    "apply",
    "application",
    "undergraduate",
    "tvet",
    "eligibility",
    "eligible",
    "guarantor",
    "requirements",
    "documents",
    "degree",
    "bursary",
]


REPAYMENT_KEYWORDS = [
    "repay",
    "repayment",
    "repaying",
    "m-pesa",
    "mpesa",
    "payment",
    "paid",
    "balance",
    "statement",
    "check off",
    "employer",
]


def classify_question(question: str) -> str:
    """
    Fast deterministic supervisor.

    No LLM call is made here.
    """

    text = question.lower().strip()

    repayment_score = sum(
        1 for keyword in REPAYMENT_KEYWORDS
        if keyword in text
    )

    loan_score = sum(
        1 for keyword in LOAN_KEYWORDS
        if keyword in text
    )

    if repayment_score > loan_score and repayment_score > 0:
        return "repayment"

    if loan_score > 0:
        return "loan"

    return "knowledge"