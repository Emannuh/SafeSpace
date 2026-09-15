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


# ---------------------------------------------------------------------------
# SupportService
# ---------------------------------------------------------------------------

class ServiceType(models.TextChoices):
    CHILD_PROTECTION  = "CHILD_PROTECTION",  "Child Protection"
    GBV_SUPPORT       = "GBV_SUPPORT",       "GBV Support"
    LEGAL_AID         = "LEGAL_AID",         "Legal Aid"
    POLICE_OVERSIGHT  = "POLICE_OVERSIGHT",  "Police Oversight"
    HEALTH_SUPPORT    = "HEALTH_SUPPORT",    "Health Support"
    GENERAL_SUPPORT   = "GENERAL_SUPPORT",   "General Support"


class SupportService(models.Model):
    """
    A verified support organisation, helpline, or official support pathway.

    SupportService is distinct from LegalSource: LegalSource holds authoritative
    legal documents; SupportService holds verified human support organisations
    that a user can actually contact. Both require verification, but they serve
    different purposes.

    Phone and contact fields are left blank where documentation does not provide
    them — we never fabricate contact information.
    """

    name          = models.CharField(max_length=200)
    slug          = models.SlugField(unique=True)
    service_type  = models.CharField(max_length=30, choices=ServiceType.choices)
    description   = models.TextField()
    jurisdiction  = models.CharField(max_length=100, default="Kenya")
    phone         = models.CharField(max_length=30, blank=True)
    whatsapp      = models.CharField(max_length=30, blank=True)
    website       = models.URLField(blank=True)
    available_24_7 = models.BooleanField(default=False)
    source_url    = models.URLField(
        help_text="URL of the official or published source confirming this service."
    )
    last_verified = models.DateField()
    status        = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED,
    )
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Support Service"
        verbose_name_plural = "Support Services"
        ordering            = ["service_type", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_service_type_display()})"


# ---------------------------------------------------------------------------
# ActionPath
# ---------------------------------------------------------------------------

class ActionType(models.TextChoices):
    RIGHTS_GUIDANCE   = "RIGHTS_GUIDANCE",   "Rights Guidance"
    SUPPORT_REFERRAL  = "SUPPORT_REFERRAL",  "Support Referral"
    LEGAL_ASSISTANCE  = "LEGAL_ASSISTANCE",  "Legal Assistance"
    REPORTING_OPTION  = "REPORTING_OPTION",  "Reporting Option"
    SAFETY_ACTION     = "SAFETY_ACTION",     "Safety Action"


class ActionPath(models.Model):
    """
    A structured next-step for a SafeSpace topic.

    ActionPath gives users concrete, source-traceable steps — not AI-generated
    suggestions. Each step is verified, ordered by step_number, and optionally
    linked to a SupportService (where a referral is relevant).

    The unique constraint on (topic, step_number) prevents duplicate step
    numbers within the same topic.
    """

    topic          = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name="action_paths",
    )
    title          = models.CharField(max_length=200)
    step_number    = models.PositiveIntegerField()
    instruction    = models.TextField()
    action_type    = models.CharField(max_length=25, choices=ActionType.choices)
    support_service = models.ForeignKey(
        SupportService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="action_paths",
    )
    source         = models.ForeignKey(
        LegalSource,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="action_paths",
        help_text="Legal basis for this action step, if applicable.",
    )
    last_verified  = models.DateField()
    status         = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.VERIFIED,
    )
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Action Path"
        verbose_name_plural = "Action Paths"
        ordering            = ["topic", "step_number"]
        constraints         = [
            models.UniqueConstraint(
                fields=["topic", "step_number"],
                name="unique_step_number_per_topic",
            )
        ]

    def __str__(self) -> str:
        return f"{self.topic} — Step {self.step_number}: {self.title}"


# ---------------------------------------------------------------------------
# RiskRule
# ---------------------------------------------------------------------------

class RiskCategory(models.TextChoices):
    GENERAL           = "GENERAL",           "General"
    ABUSE             = "ABUSE",             "Abuse"
    IMMEDIATE_DANGER  = "IMMEDIATE_DANGER",  "Immediate Danger"
    LAW_ENFORCEMENT   = "LAW_ENFORCEMENT",   "Law Enforcement"


class RiskAction(models.TextChoices):
    NORMAL_FLOW            = "NORMAL_FLOW",            "Normal Flow"
    SHOW_SUPPORT           = "SHOW_SUPPORT",           "Show Support"
    SHOW_HIGH_RISK_SUPPORT = "SHOW_HIGH_RISK_SUPPORT", "Show High Risk Support"
    SHOW_IMMEDIATE_SAFETY  = "SHOW_IMMEDIATE_SAFETY",  "Show Immediate Safety"


class RiskRule(models.Model):
    """
    A deterministic safety classification rule.

    RiskRules provide first-line classification without AI. Each rule holds a
    simple keyword/phrase pattern. The safety engine evaluates all active rules
    in priority order (highest priority number evaluated first) and returns the
    safest (highest severity) match.

    This is intentionally simple. AI-assisted classification comes later.
    Day 3 safety is deterministic and auditable.
    """

    name      = models.CharField(max_length=150)
    category  = models.CharField(max_length=25, choices=RiskCategory.choices)
    pattern   = models.TextField(
        help_text=(
            "Comma-separated keywords or phrases. A message matches this rule "
            "if it contains any of these terms (case-insensitive)."
        )
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RiskLevel.choices,
        default=RiskLevel.LOW,
    )
    action    = models.CharField(
        max_length=30,
        choices=RiskAction.choices,
        default=RiskAction.NORMAL_FLOW,
    )
    priority  = models.PositiveIntegerField(
        default=0,
        help_text="Higher number = evaluated first. Use to control rule precedence.",
    )
    active     = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Risk Rule"
        verbose_name_plural = "Risk Rules"
        ordering            = ["-priority", "name"]

    def __str__(self) -> str:
        return f"{self.name} [{self.risk_level}]"

    def matches(self, message: str) -> bool:
        """
        Return True if the message contains any pattern term (case-insensitive).
        """
        message_lower = message.lower()
        terms = [t.strip().lower() for t in self.pattern.split(",") if t.strip()]
        return any(term in message_lower for term in terms)
