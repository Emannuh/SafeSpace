"""
SafeSpace read-only API views + deterministic safety endpoint.

All knowledge/support/action endpoints are GET-only.
The safety endpoint accepts POST but does not persist user messages.

Trust filtering rules:
  - Journeys, Topics: active=True
  - RightsRecords, ActionPaths: active=True AND status=VERIFIED
  - SupportServices: active=True AND status=VERIFIED
  - Unverified/inactive content never appears in public responses.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as http_status

from .models import Journey, RightsRecord, RiskRule, SupportService, Topic, ActionPath
from .serializers import (
    ActionPathSerializer,
    JourneySerializer,
    RightsRecordSerializer,
    SupportServiceSerializer,
    TopicSerializer,
)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def journey_list(request):
    """Return all active Journeys."""
    journeys = Journey.objects.filter(active=True)
    return Response(JourneySerializer(journeys, many=True).data)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/<journey_slug>/topics/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def topic_list(request, journey_slug):
    """Return active Topics for a given active Journey."""
    journey = get_object_or_404(Journey, slug=journey_slug, active=True)
    topics  = Topic.objects.filter(journey=journey, active=True)
    return Response(TopicSerializer(topics, many=True).data)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/<journey_slug>/topics/<topic_slug>/rights/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def rights_list(request, journey_slug, topic_slug):
    """
    Return verified active RightsRecords for a topic within a journey.
    Topic is resolved using journey+slug to respect the unique-per-journey
    slug constraint.
    """
    journey = get_object_or_404(Journey, slug=journey_slug, active=True)
    topic   = get_object_or_404(Topic, slug=topic_slug, journey=journey, active=True)
    rights  = RightsRecord.objects.filter(
        topic=topic, journey=journey, active=True, status="VERIFIED"
    ).select_related("journey", "topic", "source")
    return Response(RightsRecordSerializer(rights, many=True).data)


# ---------------------------------------------------------------------------
# GET /api/v1/rights/<record_code>/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def rights_detail(request, record_code):
    """
    Return a single verified active RightsRecord by record_code.
    Returns 404 for non-existent, inactive, or unverified records.
    """
    record = get_object_or_404(
        RightsRecord.objects.select_related("journey", "topic", "source"),
        record_code=record_code,
        active=True,
        status="VERIFIED",
    )
    return Response(RightsRecordSerializer(record).data)


# ---------------------------------------------------------------------------
# GET /api/v1/support-services/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def support_service_list(request):
    """
    Return all active VERIFIED support services.
    Unverified, archived, expired and inactive services are excluded.
    """
    services = SupportService.objects.filter(active=True, status="VERIFIED")
    return Response(SupportServiceSerializer(services, many=True).data)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/<journey_slug>/topics/<topic_slug>/actions/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def action_list(request, journey_slug, topic_slug):
    """
    Return verified active ActionPaths for a topic within a journey,
    ordered by step_number.

    Journey and topic must both be active. Linked SupportService is
    exposed only when it is itself active and VERIFIED.
    """
    journey = get_object_or_404(Journey, slug=journey_slug, active=True)
    topic   = get_object_or_404(Topic, slug=topic_slug, journey=journey, active=True)
    actions = ActionPath.objects.filter(
        topic=topic, active=True, status="VERIFIED"
    ).select_related("topic", "support_service", "source").order_by("step_number")
    return Response(ActionPathSerializer(actions, many=True).data)


# ---------------------------------------------------------------------------
# POST /api/v1/safety/check/
# ---------------------------------------------------------------------------

_RISK_ORDER = {"IMMEDIATE": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}

_DEFAULT_RESPONSE = {
    "risk_level": "LOW",
    "action":     "NORMAL_FLOW",
    "matched_rule": None,
}


@api_view(["POST"])
def safety_check(request):
    """
    Deterministic safety classification.

    Accepts: { "message": "..." }
    Returns: { "risk_level": "...", "action": "...", "matched_rule": "..." }

    Process:
    1. Validates that a non-empty message string is provided.
    2. Evaluates all active RiskRules ordered by priority (highest first).
    3. Among matching rules, selects the one with the highest risk severity.
    4. Returns the result without persisting the message.

    The message is NOT logged or stored. No user record is created.
    This endpoint does not make legal determinations.
    """
    message = request.data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return Response(
            {"error": "A non-empty 'message' string is required."},
            status=http_status.HTTP_400_BAD_REQUEST,
        )

    # Evaluate active rules, highest priority first
    active_rules = RiskRule.objects.filter(active=True).order_by("-priority", "name")

    best_match = None
    best_severity = 0

    for rule in active_rules:
        if rule.matches(message):
            severity = _RISK_ORDER.get(rule.risk_level, 0)
            if severity > best_severity:
                best_severity = severity
                best_match = rule

    if best_match is None:
        return Response(_DEFAULT_RESPONSE)

    return Response({
        "risk_level":    best_match.risk_level,
        "action":        best_match.action,
        "matched_rule":  best_match.name,
    })


# ---------------------------------------------------------------------------
# POST /api/v1/ask/
# ---------------------------------------------------------------------------

@api_view(["POST"])
def ask(request):
    """
    Controlled AI question-answering endpoint.

    Accepts: { "question": "..." }
    Returns structured JSON including answer, evidence, sources, actions, support.

    Pipeline (enforced order):
      1. Validate input
      2. Deterministic safety (RiskRules) — AI cannot bypass or downgrade this
      3. Topic classification
      4. VERIFIED evidence retrieval
      5. AI explanation (only when evidence is sufficient)
      6. Output validation
      7. Structured response

    The user question is NOT persisted. No user model is created.
    An external AI provider may process the question when AI_API_KEY is set.
    """
    from core.services.answer_service import process_question

    question = request.data.get("question", "")

    if not isinstance(question, str) or not question.strip():
        return Response(
            {"error": "A non-empty 'question' string is required."},
            status=http_status.HTTP_400_BAD_REQUEST,
        )

    result = process_question(question)

    return Response({
        "answer":          result.answer,
        "evidence_status": result.evidence_status,
        "risk_level":      result.risk_level,
        "risk_action":     result.risk_action,
        "ai_used":         result.ai_used,
        "ai_disclosure":   result.ai_disclosure,
        "journey":         result.journey,
        "topic":           result.topic,
        "rights":          result.rights,
        "sources":         result.sources,
        "actions":         result.actions,
        "support_services": result.support_services,
    })


# ---------------------------------------------------------------------------
# GET /api/v1/health/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def health(request):
    """
    Minimal health/readiness endpoint.

    Returns {"status": "ok"} when the application is running.
    Exposes no secrets, credentials, environment details, or AI configuration.
    Requires no database query or AI call.
    """
    return Response({"status": "ok"})
