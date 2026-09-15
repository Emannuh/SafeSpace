"""
SafeSpace admin registration.

The Django admin serves as the knowledge-base content management console
(ADR-004). Admin classes are designed around the editorial workflow:
adding/updating rights records (FR-16), updating verification dates (FR-17),
and deactivating outdated content (FR-18).
"""

from django.contrib import admin

from .models import Journey, LegalSource, RightsRecord, Topic


# ---------------------------------------------------------------------------
# Journey
# ---------------------------------------------------------------------------

@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display  = ("name", "slug", "risk_default", "active", "updated_at")
    list_filter   = ("risk_default", "active")
    search_fields = ("name", "slug", "description")
    ordering      = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields     = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "description"),
        }),
        ("Risk and Status", {
            "fields": ("risk_default", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display  = ("title", "journey", "default_risk_level", "sort_order", "active", "updated_at")
    list_filter   = ("journey", "default_risk_level", "active")
    search_fields = ("title", "slug", "description", "journey__name")
    ordering      = ("journey__name", "sort_order", "title")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields     = ("created_at", "updated_at")
    autocomplete_fields = ("journey",)

    fieldsets = (
        (None, {
            "fields": ("journey", "title", "slug", "description"),
        }),
        ("Display and Risk", {
            "fields": ("sort_order", "default_risk_level", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ---------------------------------------------------------------------------
# LegalSource
# ---------------------------------------------------------------------------

@admin.register(LegalSource)
class LegalSourceAdmin(admin.ModelAdmin):
    list_display  = ("title", "source_type", "publisher", "jurisdiction", "status", "last_verified")
    list_filter   = ("source_type", "jurisdiction", "status")
    search_fields = ("title", "publisher", "jurisdiction")
    ordering      = ("jurisdiction", "title")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy  = "last_verified"

    fieldsets = (
        (None, {
            "fields": ("title", "source_type", "publisher"),
        }),
        ("Location and Reference", {
            "fields": ("jurisdiction", "url"),
        }),
        ("Verification", {
            "fields": ("publication_date", "last_verified", "status"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ---------------------------------------------------------------------------
# RightsRecord
# ---------------------------------------------------------------------------

@admin.register(RightsRecord)
class RightsRecordAdmin(admin.ModelAdmin):
    list_display  = (
        "record_code", "title", "journey", "topic",
        "risk_level", "status", "active", "last_verified",
    )
    list_filter   = ("journey", "risk_level", "status", "active", "jurisdiction")
    search_fields = (
        "record_code", "title", "plain_language_summary",
        "legal_reference", "journey__name", "topic__title",
    )
    ordering        = ("journey__name", "topic__title", "record_code")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("journey", "topic", "source")
    date_hierarchy  = "last_verified"

    fieldsets = (
        ("Identity", {
            "fields": ("record_code", "journey", "topic", "jurisdiction"),
        }),
        ("Content", {
            "fields": ("title", "plain_language_summary", "next_step_text", "limitations"),
        }),
        ("Legal Reference", {
            "fields": ("legal_reference", "section_reference", "source"),
        }),
        ("Risk and Verification", {
            "fields": ("risk_level", "last_verified", "status", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

from .models import ActionPath, RiskRule, SupportService


# ---------------------------------------------------------------------------
# SupportService
# ---------------------------------------------------------------------------

@admin.register(SupportService)
class SupportServiceAdmin(admin.ModelAdmin):
    list_display  = ("name", "service_type", "jurisdiction", "phone", "available_24_7", "status", "last_verified", "active")
    list_filter   = ("service_type", "jurisdiction", "available_24_7", "status", "active")
    search_fields = ("name", "slug", "description", "phone")
    ordering      = ("service_type", "name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields     = ("created_at", "updated_at")
    date_hierarchy      = "last_verified"

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "service_type", "description", "jurisdiction"),
        }),
        ("Contact", {
            "fields": ("phone", "whatsapp", "website", "available_24_7"),
        }),
        ("Verification", {
            "fields": ("source_url", "last_verified", "status", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ---------------------------------------------------------------------------
# ActionPath
# ---------------------------------------------------------------------------

@admin.register(ActionPath)
class ActionPathAdmin(admin.ModelAdmin):
    list_display  = ("title", "topic", "step_number", "action_type", "status", "active", "last_verified")
    list_filter   = ("action_type", "status", "active", "topic__journey")
    search_fields = ("title", "instruction", "topic__title", "topic__journey__name")
    ordering      = ("topic__journey__name", "topic__title", "step_number")
    readonly_fields     = ("created_at", "updated_at")
    autocomplete_fields = ("topic", "support_service", "source")
    date_hierarchy      = "last_verified"

    fieldsets = (
        (None, {
            "fields": ("topic", "title", "step_number", "action_type"),
        }),
        ("Content", {
            "fields": ("instruction",),
        }),
        ("References", {
            "fields": ("support_service", "source"),
        }),
        ("Verification", {
            "fields": ("last_verified", "status", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ---------------------------------------------------------------------------
# RiskRule
# ---------------------------------------------------------------------------

@admin.register(RiskRule)
class RiskRuleAdmin(admin.ModelAdmin):
    list_display  = ("name", "category", "risk_level", "action", "priority", "active")
    list_filter   = ("category", "risk_level", "action", "active")
    search_fields = ("name", "pattern")
    ordering      = ("-priority", "name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": ("name", "category", "pattern"),
        }),
        ("Classification", {
            "fields": ("risk_level", "action", "priority", "active"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
