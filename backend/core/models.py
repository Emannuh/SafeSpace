"""
SafeSpace core models.

Knowledge-base layer: Journey → Topic → RightsRecord, grounded in LegalSource.

Architecture reference: docs/05-architecture.md
Data model reference:   docs/06-data-model.md
"""

from django.db import models


# ---------------------------------------------------------------------------
# Shared choice definitions (used across multiple models)
# ---------------------------------------------------------------------------

class RiskLevel(models.TextChoices):
    LOW       = "LOW",       "Low"
    MEDIUM    = "MEDIUM",    "Medium"
    HIGH      = "HIGH",      "High"
    IMMEDIATE = "IMMEDIATE", "Immediate"


class VerificationStatus(models.TextChoices):
    VERIFIED           = "VERIFIED",           "Verified"
    REVIEW_REQUIRED    = "REVIEW_REQUIRED",    "Review Required"
    EXPIRED            = "EXPIRED",            "Expired"
    ARCHIVED           = "ARCHIVED",           "Archived"


# ---------------------------------------------------------------------------
# Journey
# ---------------------------------------------------------------------------

class Journey(models.Model):
    """
    A top-level SafeSpace journey (e.g. 'Domestic Violence', 'Child Rights').

    Journeys are the primary navigation entry points. Each Journey carries a
    default risk level so that the safety engine can apply a baseline before
    any user interaction is assessed.
    """

    name        = models.CharField(max_length=150)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    risk_default = models.CharField(
        max_length=10,
        choices=RiskLevel.choices,
        default=RiskLevel.LOW,
    )
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Journey"
        verbose_name_plural = "Journeys"
        ordering            = ["name"]

    def __str__(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

class Topic(models.Model):
    """
    A specific information topic within a Journey.

    Topics are the mid-level grouping between a Journey and individual
    RightsRecords. A slug is unique per Journey, not globally, so two
    different Journeys can both have a topic with the slug 'overview'.
    """

    journey    = models.ForeignKey(
        Journey,
        on_delete=models.PROTECT,
        related_name="topics",
    )
    title      = models.CharField(max_length=150)
    slug       = models.SlugField()
    description         = models.TextField()
    default_risk_level  = models.CharField(
        max_length=10,
        choices=RiskLevel.choices,
        default=RiskLevel.LOW,
    )
    sort_order = models.PositiveIntegerField(default=0)
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Topic"
        verbose_name_plural = "Topics"
        ordering            = ["journey", "sort_order", "title"]
        constraints         = [
            models.UniqueConstraint(
                fields=["journey", "slug"],
                name="unique_topic_slug_per_journey",
            )
        ]

    def __str__(self) -> str:
        return f"{self.journey.name} › {self.title}"


# ---------------------------------------------------------------------------
# LegalSource
# ---------------------------------------------------------------------------

class SourceType(models.TextChoices):
    CONSTITUTION         = "CONSTITUTION",         "Constitution"
    LEGISLATION          = "LEGISLATION",          "Legislation"
    POLICY               = "POLICY",               "Policy"
    REGULATION           = "REGULATION",           "Regulation"
    GOVERNMENT_GUIDANCE  = "GOVERNMENT_GUIDANCE",  "Government Guidance"
    JUDICIAL_DECISION    = "JUDICIAL_DECISION",    "Judicial Decision"
    INSTITUTIONAL_GUIDANCE = "INSTITUTIONAL_GUIDANCE", "Institutional Guidance"


class LegalSource(models.Model):
    """
    An authoritative legal, policy, or institutional source document.

    Every RightsRecord must point to a LegalSource so that the AI layer
    always has a citable, human-verifiable reference rather than generating
    its own legal authority.
    """

    title            = models.CharField(max_length=255)
    source_type      = models.CharField(max_length=30, choices=SourceType.choices)
    publisher        = models.CharField(max_length=255)
    jurisdiction     = models.CharField(max_length=100, default="Kenya")
    url              = models.URLField()
    publication_date = models.DateField(null=True, blank=True)
    last_verified    = models.DateField()
    status           = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Legal Source"
        verbose_name_plural = "Legal Sources"
        ordering            = ["jurisdiction", "title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.get_source_type_display()})"


# ---------------------------------------------------------------------------
# RightsRecord
# ---------------------------------------------------------------------------

class RightsRecord(models.Model):
    """
    A single, verifiable rights proposition.

    This is the atomic unit of the SafeSpace knowledge base. Each record
    represents one right or protection, expressed in plain language, tied to a
    specific legal source, and categorised by risk level. The AI layer
    explains these records — it does not generate them.

    record_code provides a stable human-readable identifier (e.g. 'DV-001')
    that can be cited in support conversations and translated content.
    """

    record_code           = models.CharField(max_length=50, unique=True)
    journey               = models.ForeignKey(
        Journey,
        on_delete=models.PROTECT,
        related_name="rights_records",
    )
    topic                 = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name="rights_records",
    )
    jurisdiction          = models.CharField(max_length=100, default="Kenya")
    title                 = models.CharField(max_length=255)
    plain_language_summary = models.TextField()
    legal_reference       = models.CharField(max_length=255)
    section_reference     = models.CharField(max_length=150, blank=True)
    source                = models.ForeignKey(
        LegalSource,
        on_delete=models.PROTECT,
        related_name="rights_records",
    )
    risk_level            = models.CharField(
        max_length=10,
        choices=RiskLevel.choices,
        default=RiskLevel.LOW,
    )
    next_step_text        = models.TextField(blank=True)
    limitations           = models.TextField(blank=True)
    last_verified         = models.DateField()
    status                = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED,
    )
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Rights Record"
        verbose_name_plural = "Rights Records"
        ordering            = ["journey", "topic", "record_code"]

    def __str__(self) -> str:
        return f"[{self.record_code}] {self.title}"
