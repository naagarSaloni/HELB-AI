from typing import Literal

from app.services.llm import get_llm


Intent = Literal[
    "loan",
    "repayment",
    "knowledge",
]


def classify_question(
    question: str,
) -> str:

    llm = get_llm()

    prompt = f"""
You are the supervisor of a HELB AI Support Agent.

HELB means the Higher Education Loans Board of Kenya.

Classify the user's question into exactly ONE category.

Categories:

loan
- Applying for a HELB loan
- Loan eligibility
- Loan requirements
- Required documents
- Loan types
- Loan application process

repayment
- Repaying a HELB loan
- M-PESA repayment
- Repayment methods
- Loan statement
- Loan balance
- Payment instructions

knowledge
- General HELB information
- Scholarships
- Deadlines
- General FAQs
- Any HELB question that is not specifically about
  applying for a loan or repaying a loan

Return ONLY one word:

loan

OR

repayment

OR

knowledge

User question:
{question}
"""

    response = llm.invoke(prompt)

    intent = response.content.strip().lower()

    if intent not in {
        "loan",
        "repayment",
        "knowledge",
    }:

        return "knowledge"

    return intent