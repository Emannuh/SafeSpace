"""
SafeSpace retrieval service.

Deterministic retrieval of VERIFIED SafeSpace evidence.
All filters are enforced here — the AI layer receives only pre-vetted content.

Trust constraints (mandatory, non-negotiable):
  RightsRecord:   active=True AND status=VERIFIED
  ActionPath:     active=True AND status=VERIFIED
  SupportService: active=True AND status=VERIFIED
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from django.db.models import Q

from core.models import (
    ActionPath,
    Journey,
    LegalSource,
    RightsRecord,
    SupportService,
    Topic,
)


# ---------------------------------------------------------------------------
# Evidence dataclass — the structured package passed to the AI layer
# ---------------------------------------------------------------------------

@dataclass
class EvidencePackage:
    """
    A fully assembled, pre-vetted evidence package.

    Every record in this package has been retrieved from the database with
    active=True AND status=VERIFIED filters applied.  The AI layer must use
    ONLY the content of this package — it may not reach beyond it.
    """

    journey: Optional[Journey] = None
    topic: Optional[Topic] = None
    rights: list[RightsRecord] = field(default_factory=list)
    actions: list[ActionPath] = field(default_factory=list)
    support_services: list[SupportService] = field(default_factory=list)
    sources: list[LegalSource] = field(default_factory=list)

    # Classification confidence
    classified: bool = False           # True if journey/topic were identified
    classification_note: str = ""      # human-readable reason if unclassified

    @property
    def has_sufficient_evidence(self) -> bool:
        """True when at least one verified rights record exists."""
        return len(self.rights) > 0

    @property
    def evidence_status(self) -> str:
        if not self.classified:
            return "INSUFFICIENT"
        if len(self.rights) == 0:
            return "INSUFFICIENT"
        if len(self.rights) >= 2:
            return "SUPPORTED"
        return "PARTIAL"


# ---------------------------------------------------------------------------
# Topic classification (deterministic keyword matching)
# ---------------------------------------------------------------------------

# Maps slug → keyword signals.  Extend as journeys grow.
_JOURNEY_KEYWORDS: dict[str, list[str]] = {
    "child-justice": [
        "arrest", "arrested", "police", "offence", "offense", "charge",
        "court", "detention", "custody", "accused", "crime", "suspect",
        "rights if arrested", "right to remain silent", "legal representation",
        "bail", "remand", "juvenile", "child justice",
    ],
    "teenage-pregnancy": [
        "pregnant", "pregnancy", "school re-entry", "re-entry", "education rights",
        "teenage pregnancy", "maternity", "reproductive", "return to school",
        "school after pregnancy", "learner pregnancy",
    ],
    "sexual-exploitation": [
        "sexual", "exploitation", "abuse", "assault", "rape", "defilement",
        "grooming", "trafficking", "underage sex", "gbv", "gender based violence",
        "sexual violence", "sexual offence",
    ],
}

_TOPIC_KEYWORDS: dict[str, list[str]] = {
    "arrest-rights": [
        "arrest", "arrested", "custody", "detention", "right to remain silent",
        "right to know reason", "inform reason", "article 49",
    ],
}


def classify_question(question: str) -> tuple[Optional[str], Optional[str]]:
    """
    Deterministically classify a question into a (journey_slug, topic_slug).

    Returns (None, None) if classification is not confident.
    Matches are case-insensitive and based on keyword presence.
    """
    q_lower = question.lower()

    best_journey: Optional[str] = None
    best_topic: Optional[str] = None
    best_score = 0

    for journey_slug, keywords in _JOURNEY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q_lower)
        if score > best_score:
            best_score = score
            best_journey = journey_slug

    # Require at least one keyword match
    if best_score == 0:
        return None, None

    # Topic classification within the identified journey
    for topic_slug, keywords in _TOPIC_KEYWORDS.items():
        if any(kw in q_lower for kw in keywords):
            best_topic = topic_slug
            break

    return best_journey, best_topic


# ---------------------------------------------------------------------------
# Evidence retrieval
# ---------------------------------------------------------------------------

def retrieve_evidence(journey_slug: Optional[str], topic_slug: Optional[str]) -> EvidencePackage:
    """
    Build a verified evidence package for the given journey/topic.

    All database queries enforce active=True AND status=VERIFIED.
    Returns an EvidencePackage with classified=False if journey is unknown.
    """
    pkg = EvidencePackage()

    if not journey_slug:
        pkg.classification_note = "Could not identify a relevant SafeSpace journey for this question."
        return pkg

    # Fetch journey
    try:
        journey = Journey.objects.get(slug=journey_slug, active=True)
    except Journey.DoesNotExist:
        pkg.classification_note = f"Journey '{journey_slug}' is not available."
        return pkg

    pkg.journey = journey
    pkg.classified = True

    # Fetch topic
    topic = None
    if topic_slug:
        try:
            topic = Topic.objects.get(slug=topic_slug, journey=journey, active=True)
            pkg.topic = topic
        except Topic.DoesNotExist:
            pass  # topic not found — still return journey-level evidence

    # Fetch verified rights records
    rights_qs = RightsRecord.objects.filter(
        journey=journey,
        active=True,
        status="VERIFIED",
    ).select_related("source", "topic")

    if topic:
        rights_qs = rights_qs.filter(topic=topic)

    pkg.rights = list(rights_qs)

    # Collect unique legal sources
    source_ids = {r.source_id for r in pkg.rights}
    pkg.sources = list(LegalSource.objects.filter(id__in=source_ids))

    # Fetch verified action paths
    if topic:
        pkg.actions = list(
            ActionPath.objects.filter(
                topic=topic,
                active=True,
                status="VERIFIED",
            ).select_related("support_service", "source")
            .order_by("step_number")
        )

    # Collect verified support services from actions + general journey pool
    svc_ids_from_actions = {
        a.support_service_id
        for a in pkg.actions
        if a.support_service_id is not None
    }
    general_svcs = SupportService.objects.filter(
        active=True,
        status="VERIFIED",
    )
    if svc_ids_from_actions:
        pkg.support_services = list(
            general_svcs.filter(
                Q(id__in=svc_ids_from_actions) |
                Q(service_type__in=["CHILD_PROTECTION", "LEGAL_AID"])
            ).distinct()
        )
    else:
        pkg.support_services = list(
            general_svcs.filter(
                service_type__in=["CHILD_PROTECTION", "LEGAL_AID"]
            )
        )

    if not pkg.has_sufficient_evidence:
        pkg.classification_note = (
            "SafeSpace has identified a relevant journey and topic, "
            "but does not yet have enough verified records to answer reliably."
        )

    return pkg
