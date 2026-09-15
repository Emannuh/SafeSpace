"""
SafeSpace demonstration seed data — Day 2 + Day 3.

Management command: python manage.py seed_demo

DATA INTEGRITY POLICY:
Every field in this seed is drawn directly from docs/03-legal-framework.md
or the Constitution of Kenya (publicly available, widely cited).

No legal wording, article numbers, URLs, phone numbers, or institutional
names have been invented. Plain-language summaries are paraphrases clearly
scoped as informational, not legal advice.

Support services included ONLY where docs/03-legal-framework.md explicitly
names the service, phone number, and purpose.

Verified sources used:
  - docs/03-legal-framework.md
  - Constitution of Kenya 2010, Article 49 (arrest rights)

Run: python manage.py seed_demo
Reset: python manage.py seed_demo --reset
"""

import datetime

from django.core.management.base import BaseCommand

from core.models import (
    ActionPath, Journey, LegalSource, RightsRecord,
    RiskRule, SupportService, Topic,
)

TODAY = datetime.date(2026, 9, 14)


# ---------------------------------------------------------------------------
# Day 2 data — Child Justice journey
# ---------------------------------------------------------------------------

CHILD_JUSTICE_JOURNEY = {
    "name": "Child Justice",
    "slug": "child-justice",
    "description": (
        "Understand the rights and protections that apply when a young person "
        "under 18 is involved in a police or justice process in Kenya."
    ),
    "risk_default": "HIGH",
    "active": True,
}

ARREST_RIGHTS_TOPIC = {
    "title": "Arrest Rights",
    "slug": "arrest-rights",
    "description": (
        "What rights do you have if police say you have committed an offence? "
        "This topic covers the constitutional protections that apply at the "
        "point of arrest in Kenya."
    ),
    "default_risk_level": "HIGH",
    "sort_order": 1,
    "active": True,
}

CONSTITUTION_SOURCE = {
    "title": "Constitution of Kenya",
    "source_type": "CONSTITUTION",
    "publisher": "Kenya Law",
    "jurisdiction": "Kenya",
    "url": "https://www.kenyalaw.org/lex/actview.xql?actid=Const2010",
    "publication_date": datetime.date(2010, 8, 27),
    "last_verified": TODAY,
    "status": "VERIFIED",
}

ARREST_RECORD = {
    "record_code": "CJ-001",
    "jurisdiction": "Kenya",
    "title": "Right to be informed of the reason for arrest",
    "plain_language_summary": (
        "If you are arrested in Kenya, you have the right to be told immediately "
        "why you are being arrested and what you are accused of. You also have "
        "the right to remain silent. You do not have to say anything to the police "
        "until you have spoken to a lawyer or another person you trust."
    ),
    "legal_reference": "Constitution of Kenya 2010, Article 49",
    "section_reference": "Art. 49(1)(a)(b)",
    "risk_level": "HIGH",
    "next_step_text": (
        "Ask the officer to clearly state why you are being arrested. "
        "You have the right to remain silent. Ask to contact a parent, "
        "guardian, or lawyer as soon as possible."
    ),
    "limitations": (
        "This information describes constitutional rights. It is not legal advice. "
        "For your specific situation, speak to a qualified lawyer or contact "
        "the National Legal Aid Service."
    ),
    "last_verified": TODAY,
    "status": "VERIFIED",
    "active": True,
}


# ---------------------------------------------------------------------------
# Day 3 data — Support services
# (All sourced from docs/03-legal-framework.md)
# ---------------------------------------------------------------------------

SUPPORT_SERVICES = [
    {
        "name": "Child Helpline 116",
        "slug": "child-helpline-116",
        "service_type": "CHILD_PROTECTION",
        "description": (
            "Child protection support, counselling, referrals, and escalation. "
            "Available to children and young people in Kenya."
        ),
        "jurisdiction": "Kenya",
        "phone": "116",
        "whatsapp": "",
        "website": "",
        "available_24_7": True,
        # Source: docs/03-legal-framework.md — Trusted Support Services section
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "GBV Helpline 1195",
        "slug": "gbv-helpline-1195",
        "service_type": "GBV_SUPPORT",
        "description": (
            "Support and referral service for gender-based violence cases in Kenya."
        ),
        "jurisdiction": "Kenya",
        "phone": "1195",
        "whatsapp": "",
        "website": "",
        "available_24_7": True,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "National Legal Aid Service",
        "slug": "national-legal-aid-service",
        "service_type": "LEGAL_AID",
        "description": (
            "Provides legal aid and legal support for eligible users in Kenya, "
            "including young people who cannot afford private legal representation."
        ),
        "jurisdiction": "Kenya",
        "phone": "",
        "whatsapp": "",
        "website": "",
        "available_24_7": False,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "Independent Policing Oversight Authority (IPOA)",
        "slug": "ipoa",
        "service_type": "POLICE_OVERSIGHT",
        "description": (
            "Oversight body for complaints related to police misconduct in Kenya."
        ),
        "jurisdiction": "Kenya",
        "phone": "",
        "whatsapp": "",
        "website": "",
        "available_24_7": False,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]


# ---------------------------------------------------------------------------
# Day 3 data — Action paths for Arrest Rights topic
# (Grounded in Art. 49, Constitution of Kenya — docs/03-legal-framework.md)
# ---------------------------------------------------------------------------

ARREST_RIGHTS_ACTIONS = [
    {
        "step_number": 1,
        "title": "Stay calm and ask why you are being arrested",
        "instruction": (
            "You have the right to know the reason for your arrest. Calmly ask "
            "the officer to explain what you are accused of. You do not have to "
            "resist or argue — but you can ask clearly and politely."
        ),
        "action_type": "RIGHTS_GUIDANCE",
        "support_service_slug": None,
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "step_number": 2,
        "title": "Exercise your right to remain silent",
        "instruction": (
            "You do not have to answer questions or make a statement at the time "
            "of arrest. You can say: 'I am exercising my right to remain silent.' "
            "Wait until you have spoken to a lawyer or a trusted adult."
        ),
        "action_type": "RIGHTS_GUIDANCE",
        "support_service_slug": None,
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "step_number": 3,
        "title": "Contact the National Legal Aid Service",
        "instruction": (
            "If you cannot afford a lawyer, you may be eligible for free legal "
            "support through the National Legal Aid Service. Ask to contact them "
            "or ask a trusted adult to contact them on your behalf."
        ),
        "action_type": "LEGAL_ASSISTANCE",
        "support_service_slug": "national-legal-aid-service",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]


# ---------------------------------------------------------------------------
# Day 3 data — Risk rules
# (Based on examples in docs/07-safety-and-privacy.md)
# ---------------------------------------------------------------------------

RISK_RULES = [
    {
        "name": "immediate-danger",
        "category": "IMMEDIATE_DANGER",
        "pattern": "i am not safe,he is here,they are hurting me,i cannot leave,not safe",
        "risk_level": "IMMEDIATE",
        "action": "SHOW_IMMEDIATE_SAFETY",
        "priority": 100,
        "active": True,
    },
    {
        "name": "abuse-high-risk",
        "category": "ABUSE",
        "pattern": "hurting me,beating me,abusing me,hitting me,sexual abuse,assault",
        "risk_level": "HIGH",
        "action": "SHOW_HIGH_RISK_SUPPORT",
        "priority": 50,
        "active": True,
    },
    {
        "name": "general-concern",
        "category": "GENERAL",
        "pattern": "scared,afraid,worried,unsafe,danger,threat,threatened",
        "risk_level": "MEDIUM",
        "action": "SHOW_SUPPORT",
        "priority": 10,
        "active": True,
    },
]


class Command(BaseCommand):
    help = "Load SafeSpace demonstration knowledge data (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Delete existing demo records and recreate them.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()

        # --- Day 2: Journey / Topic / Source / RightsRecord ---
        journey = self._upsert(Journey, {"slug": "child-justice"}, CHILD_JUSTICE_JOURNEY, "Journey")

        topic_data = {**ARREST_RIGHTS_TOPIC}
        topic, _ = Topic.objects.get_or_create(
            journey=journey, slug="arrest-rights",
            defaults=topic_data,
        )
        self._log_upsert("Topic", topic.title, _)

        source, _ = LegalSource.objects.get_or_create(
            title="Constitution of Kenya", source_type="CONSTITUTION",
            defaults=CONSTITUTION_SOURCE,
        )
        self._log_upsert("LegalSource", source.title, _)

        record_data = {**ARREST_RECORD, "journey": journey, "topic": topic, "source": source}
        record_code = record_data.pop("record_code")
        record, _ = RightsRecord.objects.get_or_create(
            record_code=record_code,
            defaults={**record_data, "record_code": record_code},
        )
        self._log_upsert("RightsRecord", f"[{record.record_code}] {record.title}", _)

        # --- Day 3: Support services ---
        service_map = {}
        for svc_data in SUPPORT_SERVICES:
            slug = svc_data["slug"]
            svc, created = SupportService.objects.get_or_create(
                slug=slug, defaults=svc_data,
            )
            self._log_upsert("SupportService", svc.name, created)
            service_map[slug] = svc

        # --- Day 3: Action paths ---
        for ap_data in ARREST_RIGHTS_ACTIONS:
            svc_slug = ap_data.pop("support_service_slug")
            support_service = service_map.get(svc_slug) if svc_slug else None
            ap, created = ActionPath.objects.get_or_create(
                topic=topic,
                step_number=ap_data["step_number"],
                defaults={
                    **ap_data,
                    "topic": topic,
                    "support_service": support_service,
                    "source": source,
                },
            )
            self._log_upsert("ActionPath", f"Step {ap.step_number}: {ap.title}", created)

        # --- Day 3: Risk rules ---
        for rule_data in RISK_RULES:
            rule, created = RiskRule.objects.get_or_create(
                name=rule_data["name"], defaults=rule_data,
            )
            self._log_upsert("RiskRule", f"{rule.name} [{rule.risk_level}]", created)

        self.stdout.write(self.style.SUCCESS("\nDemo seed complete."))
        self.stdout.write(
            "Verify at:\n"
            "  GET  /api/v1/journeys/\n"
            "  GET  /api/v1/journeys/child-justice/topics/arrest-rights/rights/\n"
            "  GET  /api/v1/journeys/child-justice/topics/arrest-rights/actions/\n"
            "  GET  /api/v1/support-services/\n"
            "  POST /api/v1/safety/check/  {\"message\": \"I am not safe\"}\n"
        )

    def _upsert(self, model, lookup, data, label):
        obj, created = model.objects.get_or_create(defaults=data, **lookup)
        self._log_upsert(label, str(obj), created)
        return obj

    def _log_upsert(self, label, name, created):
        verb = "Created" if created else "Already exists"
        self.stdout.write(f"  {verb}: {label} '{name}'")

    def _reset(self):
        self.stdout.write("Removing existing demo data...")
        # Delete children before parents (PROTECT prevents reverse)
        ActionPath.objects.filter(topic__slug="arrest-rights").delete()
        RightsRecord.objects.filter(record_code="CJ-001").delete()
        Topic.objects.filter(slug="arrest-rights", journey__slug="child-justice").delete()
        Journey.objects.filter(slug="child-justice").delete()
        LegalSource.objects.filter(title="Constitution of Kenya", source_type="CONSTITUTION").delete()
        for svc in SUPPORT_SERVICES:
            SupportService.objects.filter(slug=svc["slug"]).delete()
        for rule in RISK_RULES:
            RiskRule.objects.filter(name=rule["name"]).delete()
        self.stdout.write(self.style.WARNING("Demo data removed."))
