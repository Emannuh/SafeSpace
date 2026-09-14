"""
SafeSpace read-only serializers.

These serializers expose the knowledge-base layer to the API.
Design principles:
- Source provenance is always visible (FR-07, FR-08, ADR-002).
- Internal-only fields (created_at/updated_at) are excluded from user-facing output.
- Nested source detail is inlined in RightsRecord so the client never needs a
  separate request to show "where this came from".
- All serializers are read-only (no write methods).
"""

from rest_framework import serializers

from .models import Journey, LegalSource, RightsRecord, Topic


# ---------------------------------------------------------------------------
# Journey
# ---------------------------------------------------------------------------

class JourneySerializer(serializers.ModelSerializer):
    """
    Public representation of a Journey.
    Omits internal timestamps; exposes risk_default so the frontend can
    signal the safety baseline before the user selects a topic.
    """

    class Meta:
        model  = Journey
        fields = (
            "id",
            "name",
            "slug",
            "description",
            "risk_default",
        )


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

class TopicSerializer(serializers.ModelSerializer):
    """
    Public representation of a Topic within a Journey.
    journey_slug is included so the client can construct navigation links
    without an extra request.
    """

    journey_slug = serializers.SlugRelatedField(
        source="journey",
        slug_field="slug",
        read_only=True,
    )

    class Meta:
        model  = Topic
        fields = (
            "id",
            "title",
            "slug",
            "journey_slug",
            "description",
            "default_risk_level",
            "sort_order",
        )


# ---------------------------------------------------------------------------
# LegalSource (nested, used inside RightsRecord)
# ---------------------------------------------------------------------------

class LegalSourceSerializer(serializers.ModelSerializer):
    """
    Source provenance detail embedded inside RightsRecord responses.
    Provides title, publisher, URL, last_verified and status so that every
    rights response carries a complete, traceable citation (FR-07, FR-08).
    """

    source_type_display = serializers.CharField(
        source="get_source_type_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model  = LegalSource
        fields = (
            "id",
            "title",
            "source_type",
            "source_type_display",
            "publisher",
            "jurisdiction",
            "url",
            "publication_date",
            "last_verified",
            "status",
            "status_display",
        )


# ---------------------------------------------------------------------------
# RightsRecord
# ---------------------------------------------------------------------------

class RightsRecordSerializer(serializers.ModelSerializer):
    """
    Public representation of a single verified rights proposition.

    Source detail is nested inline — the client always receives a complete
    citation without additional requests. This enforces the architecture rule
    that every AI explanation is grounded in a citable, human-verifiable source
    (ADR-002, ADR-006).

    journey_slug and topic_slug are included to support navigation and
    front-end breadcrumb rendering.
    """

    source         = LegalSourceSerializer(read_only=True)
    journey_slug   = serializers.SlugRelatedField(
        source="journey",
        slug_field="slug",
        read_only=True,
    )
    topic_slug     = serializers.SlugRelatedField(
        source="topic",
        slug_field="slug",
        read_only=True,
    )
    risk_level_display = serializers.CharField(
        source="get_risk_level_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model  = RightsRecord
        fields = (
            "id",
            "record_code",
            "journey_slug",
            "topic_slug",
            "jurisdiction",
            "title",
            "plain_language_summary",
            "legal_reference",
            "section_reference",
            "source",
            "risk_level",
            "risk_level_display",
            "next_step_text",
            "limitations",
            "last_verified",
            "status",
            "status_display",
        )
