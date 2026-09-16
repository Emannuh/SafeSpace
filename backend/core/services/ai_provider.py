"""
SafeSpace AI provider abstraction.

All LLM communication is isolated here.
No other module makes direct API calls.

Configuration via environment variables:
  AI_PROVIDER  — currently only 'openai' is supported
  AI_API_KEY   — provider secret key (never logged, never sent to frontend)
  AI_MODEL     — model name (default: gpt-4o-mini)

Provider failures return a ProviderResult with success=False.
The caller must handle this gracefully — AI unavailability must never
prevent access to deterministic verified content.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# System instruction — stored centrally, never duplicated across views.
# The model may only use the evidence supplied in the user turn.
SYSTEM_INSTRUCTION = """You are the explanation layer for SafeSpace, a rights-information platform for young people in Kenya.

Your role is to explain verified legal information in plain, age-appropriate language.

STRICT RULES:
1. Answer ONLY from the verified SafeSpace evidence supplied in this conversation.
2. Do NOT rely on your general legal knowledge.
3. Do NOT invent: laws, rights, procedures, institutions, phone numbers, URLs, deadlines, or penalties.
4. If the evidence does not support an answer, say: "SafeSpace does not yet have enough verified information to answer this reliably."
5. Do NOT determine guilt or innocence.
6. Do NOT present yourself as a lawyer, legal expert, or counsellor.
7. Do NOT replace emergency, legal, medical, or safeguarding professionals.
8. Do NOT alter source citations — reproduce them exactly as provided.
9. Do NOT infer facts the user did not provide.
10. Keep your answer concise, calm, and easy to understand for a young person.
11. Always acknowledge when your explanation is limited by the available evidence."""


@dataclass
class ProviderResult:
    success: bool
    answer: str
    error: Optional[str] = None


def _build_evidence_text(evidence_package) -> str:
    """
    Serialise the evidence package into a structured text block
    that forms the trusted context for the model.

    User-supplied text is clearly SEPARATED from this evidence block —
    the model sees evidence first, then the question.
    This separation is the prompt-injection boundary.
    """
    lines = ["=== VERIFIED SAFESPACE EVIDENCE ===", ""]

    if evidence_package.journey:
        lines.append(f"JOURNEY: {evidence_package.journey.name}")
        lines.append(f"JURISDICTION: {evidence_package.journey.risk_default and 'Kenya'}")
        lines.append("")

    if evidence_package.topic:
        lines.append(f"TOPIC: {evidence_package.topic.title}")
        lines.append("")

    if evidence_package.rights:
        lines.append("VERIFIED RIGHTS RECORDS:")
        for r in evidence_package.rights:
            lines.append(f"  [{r.record_code}] {r.title}")
            lines.append(f"  Summary: {r.plain_language_summary}")
            lines.append(f"  Legal reference: {r.legal_reference}")
            if r.section_reference:
                lines.append(f"  Section: {r.section_reference}")
            if r.next_step_text:
                lines.append(f"  Next step: {r.next_step_text}")
            if r.limitations:
                lines.append(f"  Limitations: {r.limitations}")
            lines.append("")

    if evidence_package.sources:
        lines.append("AUTHORITATIVE SOURCES:")
        for s in evidence_package.sources:
            lines.append(f"  - {s.title} ({s.source_type_display})")
            lines.append(f"    Publisher: {s.publisher}")
            lines.append(f"    URL: {s.url}")
            lines.append(f"    Last verified: {s.last_verified}")
            lines.append("")

    if evidence_package.actions:
        lines.append("VERIFIED ACTION STEPS:")
        for a in evidence_package.actions:
            lines.append(f"  Step {a.step_number}: {a.title}")
            lines.append(f"  {a.instruction}")
            lines.append("")

    if evidence_package.support_services:
        lines.append("VERIFIED SUPPORT SERVICES:")
        for svc in evidence_package.support_services:
            lines.append(f"  - {svc.name} ({svc.service_type_display})")
            if svc.phone:
                lines.append(f"    Phone: {svc.phone}")
            lines.append(f"    24/7: {'Yes' if svc.available_24_7 else 'No'}")
            lines.append("")

    lines.append("=== END OF VERIFIED EVIDENCE ===")
    return "\n".join(lines)


def call_provider(question: str, evidence_package) -> ProviderResult:
    """
    Call the configured AI provider with the evidence package + question.

    The question and evidence are clearly separated — evidence is provided
    as a structured context block before the user question is stated.
    This prevents user text from being interpreted as trusted evidence.

    Returns ProviderResult(success=False) on any failure.
    The caller must handle failure gracefully.
    """
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    api_key = os.getenv("AI_API_KEY", "")
    model = os.getenv("AI_MODEL", "gpt-4o-mini")

    if not api_key:
        return ProviderResult(
            success=False,
            answer="",
            error="AI_API_KEY is not configured.",
        )

    evidence_text = _build_evidence_text(evidence_package)

    # User turn: evidence block first, then the question.
    # The separation makes it structurally impossible for question text
    # to masquerade as verified evidence.
    user_message = (
        f"{evidence_text}\n\n"
        f"=== USER QUESTION ===\n"
        f"{question.strip()}\n"
        f"=== END OF USER QUESTION ===\n\n"
        f"Using ONLY the verified SafeSpace evidence above, provide a plain-language "
        f"explanation for the user's question. If the evidence does not fully support "
        f"an answer, say so clearly."
    )

    if provider == "openai":
        return _call_openai(api_key, model, user_message)

    return ProviderResult(
        success=False,
        answer="",
        error=f"Unsupported AI_PROVIDER: '{provider}'.",
    )


def _call_openai(api_key: str, model: str, user_message: str) -> ProviderResult:
    try:
        from openai import OpenAI, APIError, APITimeoutError, APIConnectionError  # noqa: PLC0415

        client = OpenAI(api_key=api_key, timeout=30.0)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user",   "content": user_message},
            ],
            max_tokens=600,
            temperature=0.1,  # low temperature for factual, consistent answers
        )
        answer = response.choices[0].message.content or ""
        return ProviderResult(success=True, answer=answer.strip())

    except APITimeoutError:
        logger.warning("SafeSpace AI: OpenAI request timed out.")
        return ProviderResult(success=False, answer="", error="AI provider timed out.")

    except APIConnectionError:
        logger.warning("SafeSpace AI: OpenAI connection error.")
        return ProviderResult(success=False, answer="", error="Could not connect to AI provider.")

    except APIError as exc:
        logger.warning("SafeSpace AI: OpenAI API error: %s", type(exc).__name__)
        return ProviderResult(success=False, answer="", error="AI provider returned an error.")

    except Exception as exc:  # noqa: BLE001
        logger.error("SafeSpace AI: Unexpected provider error: %s", type(exc).__name__)
        return ProviderResult(success=False, answer="", error="Unexpected AI provider error.")
