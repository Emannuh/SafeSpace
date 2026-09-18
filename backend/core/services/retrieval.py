"""
SafeSpace retrieval service.

Deterministic retrieval of VERIFIED SafeSpace evidence.
All filters are enforced here — the AI layer receives only pre-vetted content.

Trust constraints (mandatory, non-negotiable):
  RightsRecord:   active=True AND status=VERIFIED
  ActionPath:     active=True AND status=VERIFIED
  SupportService: active=True AND status=VERIFIED

Day 6: classifier extended to cover all three MVP journeys and 12 topics.
No vector database or embeddings are used. Deterministic keyword matching
is appropriate for the current small, structured dataset.
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
# Evidence dataclass
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

    classified: bool = False
    classification_note: str = ""

    @property
    def has_sufficient_evidence(self) -> bool:
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
# Journey keyword signals
# ---------------------------------------------------------------------------
# Each list contains the phrases/words that indicate a question belongs to
# that journey.  Score = number of matching keywords (highest score wins).
# ---------------------------------------------------------------------------

_JOURNEY_KEYWORDS: dict[str, list[str]] = {
    # ── Teenage Pregnancy ────────────────────────────────────────────────
    "teenage-pregnancy": [
        "pregnant", "pregnancy", "learner pregnancy", "school pregnancy",
        "school while pregnant", "send me away", "expelled pregnant",
        "re-entry", "school re-entry", "return to school", "return after baby",
        "go back to school", "after delivery", "after giving birth", "after having baby",
        "exam", "exams", "examination", "sit my exam", "kcse", "kcpe",
        "maternity", "reproductive", "teenage pregnancy", "education rights",
        "continue school", "learner with child",
    ],

    # ── Sexual Exploitation / Abuse ──────────────────────────────────────
    "sexual-exploitation": [
        "sexual", "sexually", "exploitation", "exploiting", "exploited",
        "sexual abuse", "abuse", "abused", "defilement", "defiled",
        "rape", "raped", "assault", "assaulted",
        "grooming", "groomed", "trafficking",
        "gbv", "gender based violence", "gender-based violence",
        "sexual offence", "sexual violence",
        "someone is touching me", "adult is doing something sexual",
        "reporting abuse", "report abuse", "who can i tell", "who can i report to",
        "safe to tell", "protect me", "protection from abuse",
        "underage sex",
    ],

    # ── Child Justice ────────────────────────────────────────────────────
    "child-justice": [
        "arrest", "arrested", "police", "offence", "offense",
        "charge", "charged", "accused", "suspect",
        "court", "prosecution", "trial",
        "detention", "detained", "custody", "remand", "bail",
        "lawyer", "legal representation", "legal aid", "advocate",
        "parent or guardian", "guardian notified", "parent notified",
        "parent present", "guardian present",
        "held with adults", "child detention", "separate from adults",
        "diversion", "diverted", "caution", "community service order",
        "juvenile", "child justice", "young offender",
        "right to remain silent", "rights when arrested",
        "can my parent", "can my guardian",
    ],
}

# ---------------------------------------------------------------------------
# Topic keyword signals (checked only after journey is identified)
# ---------------------------------------------------------------------------
# Structure: {journey_slug: {topic_slug: [keywords]}}
# ---------------------------------------------------------------------------

_TOPIC_KEYWORDS: dict[str, dict[str, list[str]]] = {
    "teenage-pregnancy": {
        "staying-in-school": [
            "stay in school", "continue school", "while pregnant", "send me away",
            "expelled", "leave school", "school during pregnancy",
            "can school", "can my school",
        ],
        "school-reentry": [
            "re-entry", "reentry", "return to school", "go back to school",
            "after delivery", "after giving birth", "after having baby",
            "after having my baby", "back to school",
        ],
        "national-examinations": [
            "exam", "exams", "examination", "sit my exam", "national exam",
            "kcse", "kcpe", "sit exams while pregnant", "exam while pregnant",
        ],
        "getting-support": [
            "support", "help", "who can help", "need help", "where can i go",
            "child helpline", "counselling",
        ],
    },
    "sexual-exploitation": {
        "understanding-exploitation": [
            "what is exploitation", "what is sexual exploitation",
            "exploitation", "exploiting me", "someone using me",
            "older person", "adult doing something", "adult i depend on",
        ],
        "sexual-abuse-child": [
            "sexual abuse", "abuse", "abused", "defilement", "rape",
            "someone is abusing me", "adult is abusing", "what can i do",
        ],
        "safe-reporting": [
            "report", "reporting", "tell someone", "who can i tell",
            "who can report", "report on behalf", "report abuse",
            "how to report", "safe to report",
        ],
        "protection-support": [
            "protect", "protection", "safe", "safety", "help me",
            "get help", "support", "where can i get help",
        ],
    },
    "child-justice": {
        "arrest-rights": [
            "arrest", "arrested", "why arrested", "right to remain silent",
            "right to know reason", "inform reason", "article 49",
            "what happens when arrested", "rights if arrested",
        ],
        "legal-representation": [
            "lawyer", "legal representation", "legal aid", "advocate",
            "afford lawyer", "right to lawyer", "can i have a lawyer",
            "free lawyer", "national legal aid",
        ],
        "parent-guardian-involvement": [
            "parent notified", "guardian notified",
            "parent present", "guardian present",
            "parent or guardian", "can my parent", "can my guardian",
            "mum with me", "dad with me", "mother with me", "father with me",
            "parent be with me", "guardian be with me",
            "notify parent", "notify guardian",
            "parent during questioning", "guardian during court",
        ],
        "detention-protections": [
            "detention", "detained", "held", "custody", "remand",
            "held with adults", "separate from adults", "child detention",
            "conditions of detention", "24 hours", "rights in detention",
        ],
        "diversion": [
            "diversion", "diverted", "divert", "caution",
            "community service", "outside court", "not go to court",
            "what is diversion", "diversion eligible",
        ],
    },
}


def classify_question(question: str) -> tuple[Optional[str], Optional[str]]:
    """
    Deterministically classify a question into (journey_slug, topic_slug).

    Returns (None, None) when no confident match is found.
    Matching is case-insensitive; score = number of matching keyword phrases.
    The journey with the highest score wins (minimum score of 1 required).
    Within the winning journey, the topic with the first keyword match wins.
    """
    q_lower = question.lower()

    # ── Journey classification ────────────────────────────────────────────
    best_journey: Optional[str] = None
    best_score = 0

    for journey_slug, keywords in _JOURNEY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q_lower)
        if score > best_score:
            best_score = score
            best_journey = journey_slug

    if best_score == 0 or best_journey is None:
        return None, None

    # ── Topic classification within the winning journey ───────────────────
    best_topic: Optional[str] = None
    topic_map = _TOPIC_KEYWORDS.get(best_journey, {})

    # Score each topic and pick the best match
    best_topic_score = 0
    for topic_slug, keywords in topic_map.items():
        score = sum(1 for kw in keywords if kw in q_lower)
        if score > best_topic_score:
            best_topic_score = score
            best_topic = topic_slug

    return best_journey, best_topic


# ---------------------------------------------------------------------------
# Evidence retrieval
# ---------------------------------------------------------------------------

def retrieve_evidence(journey_slug: Optional[str], topic_slug: Optional[str]) -> EvidencePackage:
    """
    Build a verified evidence package for the given journey/topic.

    All database queries enforce active=True AND status=VERIFIED.
    Returns an EvidencePackage with classified=False if journey is unknown.

    Support services are selected in priority order:
    1. Services directly linked via ActionPath.support_service for this topic
    2. CHILD_PROTECTION services (always relevant for SafeSpace journeys)
    3. LEGAL_AID services (relevant for child justice)
    4. GBV_SUPPORT services (relevant for sexual exploitation journey)
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
            pass  # Topic not found — return journey-level evidence

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

    # Collect verified support services
    svc_ids_from_actions = {
        a.support_service_id
        for a in pkg.actions
        if a.support_service_id is not None
    }

    # Journey-appropriate service types
    journey_svc_types: list[str] = ["CHILD_PROTECTION"]
    if journey_slug == "child-justice":
        journey_svc_types.append("LEGAL_AID")
    if journey_slug == "sexual-exploitation":
        journey_svc_types.extend(["GBV_SUPPORT", "LEGAL_AID"])
    if journey_slug == "teenage-pregnancy":
        journey_svc_types.append("LEGAL_AID")

    general_svcs = SupportService.objects.filter(active=True, status="VERIFIED")

    if svc_ids_from_actions:
        pkg.support_services = list(
            general_svcs.filter(
                Q(id__in=svc_ids_from_actions) |
                Q(service_type__in=journey_svc_types)
            ).distinct()
        )
    else:
        pkg.support_services = list(
            general_svcs.filter(service_type__in=journey_svc_types)
        )

    if not pkg.has_sufficient_evidence:
        pkg.classification_note = (
            "SafeSpace has identified a relevant journey and topic, "
            "but does not yet have enough verified records to answer reliably."
        )

    return pkg
