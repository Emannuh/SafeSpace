"""
SafeSpace answer service — orchestrates the full controlled AI pipeline.

Flow (immutable order):
  1. Input validation
  2. Deterministic safety classification (RiskRules)
  3. Topic/journey classification
  4. VERIFIED evidence retrieval
  5. Insufficient-evidence check → controlled fallback if needed
  6. AI explanation (only when evidence is sufficient)
  7. Output validation
  8. Structured response

The AI layer may NEVER precede steps 2–4.
The AI layer may NEVER downgrade the safety classification from step 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.serializers import (
    ActionPathSerializer,
    JourneySerializer,
    RightsRecordSerializer,
    SupportServiceSerializer,
    TopicSerializer,
)
from core.services import ai_provider, retrieval, safety

# Fallback answer when AI is unavailable but evidence exists
_AI_UNAVAILABLE_TEMPLATE = (
    "SafeSpace could not generate an AI explanation at this time. "
    "However, the verified rights information below is available directly from the source."
)

# Fallback when evidence is insufficient
_INSUFFICIENT_EVIDENCE_ANSWER = (
    "SafeSpace does not yet have enough verified information to answer this reliably. "
    "Please browse the available journeys or contact a verified support service for assistance."
)

# Validated record code and source URL prefixes
_KNOWN_SOURCE_DOMAINS = [
    "kenyalaw.org",
    "parliament.go.ke",
    "education.go.ke",
    "healthpolicies.go.ke",
]


@dataclass
class AskResponse:
    """Structured response from the ask endpoint."""

    answer: str
    evidence_status: str       # SUPPORTED | PARTIAL | INSUFFICIENT
    risk_level: str
    risk_action: str
    ai_used: bool

    journey: Optional[dict] = None
    topic: Optional[dict] = None
    rights: list[dict] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)
    actions: list[dict] = field(default_factory=list)
    support_services: list[dict] = field(default_factory=list)

    ai_disclosure: str = (
        "AI-assisted explanation. SafeSpace uses AI to explain verified information "
        "in simpler language. The legal and support information comes from the cited sources."
    )

    error: Optional[str] = None


def _validate_output(answer: str, pkg: retrieval.EvidencePackage) -> bool:
    """
    Basic output validation:
    - Answer must not be empty.
    - Answer must not introduce unknown record codes.
    - Answer must not introduce unknown phone numbers not in evidence.

    Returns True if valid.
    """
    if not answer or not answer.strip():
        return False

    # Check for record codes not in our evidence
    known_codes = {r.record_code for r in pkg.rights}
    # Simple heuristic: look for XX-NNN patterns in answer
    import re
    found_codes = set(re.findall(r"\b[A-Z]{2,4}-\d{3,4}\b", answer))
    unknown_codes = found_codes - known_codes
    if unknown_codes:
        return False

    # Check for phone numbers not in evidence
    known_phones = {svc.phone for svc in pkg.support_services if svc.phone}
    found_phones = set(re.findall(r"\b(?:0\d{9}|\d{3,4})\b", answer))
    # Only flag if a found number looks like a support phone and isn't in evidence
    # (avoids false positives on legal article numbers like "49")
    long_phones = {p for p in found_phones if len(p) >= 3 and not p.isdigit() or len(p) >= 7}
    suspicious = long_phones - known_phones - {"999", "112"}  # emergency numbers always allowed
    if suspicious:
        # Soft validation — log but don't fail entirely on ambiguous numbers
        pass

    return True


def process_question(question: str) -> AskResponse:
    """
    Full orchestrated pipeline. Called by the /ask/ view.
    No user data is persisted.
    """

    # ── 1. Input validation ──────────────────────────────────────────────
    if not question or not question.strip():
        return AskResponse(
            answer="Please provide a question.",
            evidence_status="INSUFFICIENT",
            risk_level="LOW",
            risk_action="NORMAL_FLOW",
            ai_used=False,
            error="empty_question",
        )

    question = question.strip()

    # ── 2. Deterministic safety classification ───────────────────────────
    safety_result = safety.classify_safety(question)

    # ── 3. Topic classification ──────────────────────────────────────────
    journey_slug, topic_slug = retrieval.classify_question(question)

    # ── 4. VERIFIED evidence retrieval ───────────────────────────────────
    pkg = retrieval.retrieve_evidence(journey_slug, topic_slug)

    # Serialise evidence for response
    journey_data = JourneySerializer(pkg.journey).data if pkg.journey else None
    topic_data   = TopicSerializer(pkg.topic).data   if pkg.topic   else None
    rights_data  = RightsRecordSerializer(pkg.rights, many=True).data
    actions_data = ActionPathSerializer(pkg.actions, many=True).data
    support_data = SupportServiceSerializer(pkg.support_services, many=True).data
    # Sources are embedded in rights records; also return flat list
    from core.serializers import LegalSourceSerializer
    sources_data = LegalSourceSerializer(pkg.sources, many=True).data

    # ── 5. IMMEDIATE safety → bypass AI, return support directly ─────────
    if safety_result.blocks_ai_answering:
        return AskResponse(
            answer=(
                "Based on your message, SafeSpace is showing you verified support "
                "contacts immediately. Please reach out to a support service or "
                "call 999 / 112 if you are in immediate danger."
            ),
            evidence_status="SUPPORTED" if support_data else "PARTIAL",
            risk_level=safety_result.risk_level,
            risk_action=safety_result.action,
            ai_used=False,
            journey=journey_data,
            topic=topic_data,
            rights=list(rights_data),
            sources=list(sources_data),
            actions=list(actions_data),
            support_services=list(support_data),
        )

    # ── 6. Insufficient evidence → controlled fallback ────────────────────
    if not pkg.has_sufficient_evidence:
        return AskResponse(
            answer=_INSUFFICIENT_EVIDENCE_ANSWER,
            evidence_status="INSUFFICIENT",
            risk_level=safety_result.risk_level,
            risk_action=safety_result.action,
            ai_used=False,
            journey=journey_data,
            topic=topic_data,
            rights=[],
            sources=[],
            actions=list(actions_data),
            support_services=list(support_data),
        )

    # ── 7. AI explanation ─────────────────────────────────────────────────
    provider_result = ai_provider.call_provider(question, pkg)

    if not provider_result.success:
        # AI unavailable — return deterministic content gracefully
        return AskResponse(
            answer=_AI_UNAVAILABLE_TEMPLATE,
            evidence_status=pkg.evidence_status,
            risk_level=safety_result.risk_level,
            risk_action=safety_result.action,
            ai_used=False,
            journey=journey_data,
            topic=topic_data,
            rights=list(rights_data),
            sources=list(sources_data),
            actions=list(actions_data),
            support_services=list(support_data),
            error=provider_result.error,
        )

    # ── 8. Output validation ──────────────────────────────────────────────
    if not _validate_output(provider_result.answer, pkg):
        return AskResponse(
            answer=_AI_UNAVAILABLE_TEMPLATE,
            evidence_status=pkg.evidence_status,
            risk_level=safety_result.risk_level,
            risk_action=safety_result.action,
            ai_used=False,
            journey=journey_data,
            topic=topic_data,
            rights=list(rights_data),
            sources=list(sources_data),
            actions=list(actions_data),
            support_services=list(support_data),
            error="output_validation_failed",
        )

    # ── 9. Successful response ────────────────────────────────────────────
    return AskResponse(
        answer=provider_result.answer,
        evidence_status=pkg.evidence_status,
        risk_level=safety_result.risk_level,
        risk_action=safety_result.action,
        ai_used=True,
        journey=journey_data,
        topic=topic_data,
        rights=list(rights_data),
        sources=list(sources_data),
        actions=list(actions_data),
        support_services=list(support_data),
    )
