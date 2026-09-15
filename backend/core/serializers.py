"""
SafeSpace read-only serializers.

Design principles:
- Source provenance is always visible (FR-07, FR-08, ADR-002).
- Internal-only fields (created_at/updated_at) are excluded from user-facing output.
- Nested source/service detail is inlined so clients never need extra requests.
- All serializers are read-only (no write methods).
"""

from rest_framework import serializers

from .models import ActionPath, Journey, LegalSource, RightsRecord, SupportService, Topic


# ---------------------------------------------------------------------------
# Journey
# ---------------------------------------------------------------------------

class JourneySerializer(serializers.ModelSerializer):
    """Public representation of a Journey."""

    class Meta:
        model  = Journey
        fields = ("id", "name", "slug", "description", "risk_default")


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

class TopicSerializer(serializers.ModelSerializer):
    """Public representation of a Topic within a Journey."""

    journey_slug = serializers.SlugRelatedField(
        source="journey", slug_field="slug", read_only=True
    )

    class Meta:
        model  = Topic
        fields = ("id", "title", "slug", "journey_slug", "description",
                  "default_risk_level", "sort_order")


# ---------------------------------------------------------------------------
# LegalSource (nested inside RightsRecord and ActionPath)
# ---------------------------------------------------------------------------

class LegalSourceSerializer(serializers.ModelSerializer):
    """
    Source provenance embedded inside RightsRecord and ActionPath responses.
    Provides title, publisher, URL, last_verified and status for every citation.
    """

    source_type_display = serializers.CharField(
        source="get_source_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model  = LegalSource
        fields = ("id", "title", "source_type", "source_type_display",
                  "publisher", "jurisdiction", "url", "publication_date",
                  "last_verified", "status", "status_display")


# ---------------------------------------------------------------------------
# RightsRecord
# ---------------------------------------------------------------------------

class RightsRecordSerializer(serializers.ModelSerializer):
    """
    Public representation of a single verified rights proposition.
    Source detail is nested inline for full citation in every response.
    """

    source         = LegalSourceSerializer(read_only=True)
    journey_slug   = serializers.SlugRelatedField(
        source="journey", slug_field="slug", read_only=True
    )
    topic_slug     = serializers.SlugRelatedField(
        source="topic", slug_field="slug", read_only=True
    )
    risk_level_display = serializers.CharField(
        source="get_risk_level_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model  = RightsRecord
        fields = ("id", "record_code", "journey_slug", "topic_slug",
                  "jurisdiction", "title", "plain_language_summary",
                  "legal_reference", "section_reference", "source",
                  "risk_level", "risk_level_display", "next_step_text",
                  "limitations", "last_verified", "status", "status_display")


# ---------------------------------------------------------------------------
# SupportService
# ---------------------------------------------------------------------------

class SupportServiceSerializer(serializers.ModelSerializer):
    """
    Public representation of a verified support service.
    Contact fields are included only where documentation provides them.
    No personal data is collected or returned.
    """

    service_type_display = serializers.CharField(
        source="get_service_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )

    class Meta:
        model  = SupportService
        fields = ("id", "name", "slug", "service_type", "service_type_display",
                  "description", "jurisdiction", "phone", "whatsapp", "website",
                  "available_24_7", "last_verified", "status", "status_display")


# ---------------------------------------------------------------------------
# ActionPath
# ---------------------------------------------------------------------------

class ActionPathSerializer(serializers.ModelSerializer):
    """
    Public representation of a structured next-step action.
    Inline support service and source provenance — no extra requests needed.
    """

    action_type_display = serializers.CharField(
        source="get_action_type_display", read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display", read_only=True
    )
    support_service = SupportServiceSerializer(read_only=True)
    source          = LegalSourceSerializer(read_only=True)
    topic_slug      = serializers.SlugRelatedField(
        source="topic", slug_field="slug", read_only=True
    )

    class Meta:
        model  = ActionPath
        fields = ("id", "topic_slug", "title", "step_number", "instruction",
                  "action_type", "action_type_display", "support_service",
                  "source", "last_verified", "status", "status_display")
