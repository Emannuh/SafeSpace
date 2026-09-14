"""
SafeSpace read-only API views.

All endpoints are GET-only. No write operations are exposed.

Filtering rules enforce the trust model:
  - Only active Journeys and Topics are returned.
  - Only active AND VERIFIED RightsRecords are returned.
  - Archived, expired, and review-required records never appear in
    normal user-facing responses (ADR-002, FR-19, FR-20).

URL design note:
  Topic slugs are unique within a Journey, not globally (see the
  unique_topic_slug_per_journey constraint). The rights-list endpoint
  therefore uses the full journey+topic path to resolve topics
  unambiguously, consistent with the data model design.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Journey, RightsRecord, Topic
from .serializers import (
    JourneySerializer,
    RightsRecordSerializer,
    TopicSerializer,
)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def journey_list(request):
    """
    Return all active Journeys.

    Only active journeys are returned — inactive journeys are hidden from
    users while remaining manageable in the admin.
    """
    journeys = Journey.objects.filter(active=True)
    serializer = JourneySerializer(journeys, many=True)
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/<journey_slug>/topics/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def topic_list(request, journey_slug):
    """
    Return all active Topics for a given Journey slug.

    Returns 404 if the Journey does not exist or is not active.
    Topics are ordered by sort_order then title (defined in Topic.Meta).
    """
    journey = get_object_or_404(Journey, slug=journey_slug, active=True)
    topics  = Topic.objects.filter(journey=journey, active=True)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# GET /api/v1/journeys/<journey_slug>/topics/<topic_slug>/rights/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def rights_list(request, journey_slug, topic_slug):
    """
    Return all verified and active RightsRecords for a topic within a journey.

    Both journey and topic must be active. The topic is resolved using the
    combination of journey_slug + topic_slug, which matches the database
    constraint (unique_topic_slug_per_journey). This prevents ambiguity when
    the same topic slug exists in multiple journeys.

    Filtering is strict:
      active=True       — unpublished records are excluded
      status=VERIFIED   — review-required, expired, archived records excluded
    """
    journey = get_object_or_404(Journey, slug=journey_slug, active=True)
    topic   = get_object_or_404(Topic, slug=topic_slug, journey=journey, active=True)
    rights  = RightsRecord.objects.filter(
        topic=topic,
        journey=journey,
        active=True,
        status="VERIFIED",
    ).select_related("journey", "topic", "source")
    serializer = RightsRecordSerializer(rights, many=True)
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# GET /api/v1/rights/<record_code>/
# ---------------------------------------------------------------------------

@api_view(["GET"])
def rights_detail(request, record_code):
    """
    Return a single verified and active RightsRecord by its stable record_code.

    Returns 404 if:
      - the record_code does not exist
      - the record is inactive
      - the record status is not VERIFIED

    Knowing a record_code cannot be used to retrieve unverified content.
    The nested LegalSource ensures every response carries a full citation.
    """
    record = get_object_or_404(
        RightsRecord.objects.select_related("journey", "topic", "source"),
        record_code=record_code,
        active=True,
        status="VERIFIED",
    )
    serializer = RightsRecordSerializer(record)
    return Response(serializer.data)
