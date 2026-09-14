"""
SafeSpace demonstration seed data.

Management command: python manage.py seed_demo

IMPORTANT — DATA INTEGRITY POLICY:
Every field in this seed is drawn directly from docs/03-legal-framework.md
or the Constitution of Kenya (publicly available, widely cited).

No legal wording, article numbers, URLs, or institutional names have been
invented. The plain-language summary is a paraphrase, not a statutory quote,
and is clearly scoped as informational, not legal advice.

Verified sources used:
  - docs/03-legal-framework.md (SafeSpace legal framework document)
    Entry: "Rights of arrested persons — Constitution of Kenya, Article 49
            — Kenya Law — To be verified and recorded"

This command is idempotent: running it multiple times will not create
duplicate records. Use --reset to remove and recreate the demo data.

Do NOT use this command to load production legal content.
"""

import datetime

from django.core.management.base import BaseCommand

from core.models import Journey, LegalSource, RightsRecord, Topic


DEMO_DATA = {
    "journey": {
        "name": "Child Justice",
        "slug": "child-justice",
        "description": (
            "Understand the rights and protections that apply when a young "
            "person under 18 is involved in a police or justice process in Kenya."
        ),
        "risk_default": "HIGH",
        "active": True,
    },
    "topic": {
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
    },
    "source": {
        "title": "Constitution of Kenya",
        "source_type": "CONSTITUTION",
        "publisher": "Kenya Law",
        "jurisdiction": "Kenya",
        # Kenya Law is the official legal publisher. This URL points to the
        # Kenya Law official site, not to a specific article, because article-
        # level deep links may change. The human editor should update this to
        # the most stable available permalink.
        "url": "https://www.kenyalaw.org/lex/actview.xql?actid=Const2010",
        "publication_date": datetime.date(2010, 8, 27),
        # last_verified is set to the date this seed was written.
        # A human editor should update this after manual verification.
        "last_verified": datetime.date(2026, 9, 14),
        "status": "VERIFIED",
    },
    "record": {
        "record_code": "CJ-001",
        "jurisdiction": "Kenya",
        "title": "Right to be informed of the reason for arrest",
        # Plain-language summary drawn from Article 49(1)(a) of the
        # Constitution of Kenya 2010, as listed in docs/03-legal-framework.md.
        # This is an informational paraphrase, not legal advice.
        "plain_language_summary": (
            "If you are arrested in Kenya, you have the right to be told "
            "immediately why you are being arrested and what you are accused of. "
            "You also have the right to remain silent. You do not have to say "
            "anything to the police until you have spoken to a lawyer or another "
            "person you trust."
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
            "This information describes constitutional rights. It is not legal "
            "advice. For your specific situation, speak to a qualified lawyer "
            "or contact the National Legal Aid Service."
        ),
        "last_verified": datetime.date(2026, 9, 14),
        "status": "VERIFIED",
        "active": True,
    },
}


class Command(BaseCommand):
    help = "Load SafeSpace demonstration knowledge data (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing demo records and recreate them.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Removing existing demo data...")
            RightsRecord.objects.filter(record_code="CJ-001").delete()
            Journey.objects.filter(slug="child-justice").delete()
            LegalSource.objects.filter(
                title="Constitution of Kenya", source_type="CONSTITUTION"
            ).delete()
            self.stdout.write(self.style.WARNING("Demo data removed."))

        # Journey
        journey, j_created = Journey.objects.get_or_create(
            slug=DEMO_DATA["journey"]["slug"],
            defaults=DEMO_DATA["journey"],
        )
        self.stdout.write(
            f"{'Created' if j_created else 'Already exists'}: Journey '{journey.name}'"
        )

        # Topic
        topic_defaults = {**DEMO_DATA["topic"]}
        topic, t_created = Topic.objects.get_or_create(
            journey=journey,
            slug=DEMO_DATA["topic"]["slug"],
            defaults=topic_defaults,
        )
        self.stdout.write(
            f"{'Created' if t_created else 'Already exists'}: Topic '{topic.title}'"
        )

        # LegalSource
        source_defaults = {**DEMO_DATA["source"]}
        source, s_created = LegalSource.objects.get_or_create(
            title=DEMO_DATA["source"]["title"],
            source_type=DEMO_DATA["source"]["source_type"],
            defaults=source_defaults,
        )
        self.stdout.write(
            f"{'Created' if s_created else 'Already exists'}: LegalSource '{source.title}'"
        )

        # RightsRecord
        record_defaults = {
            **DEMO_DATA["record"],
            "journey": journey,
            "topic": topic,
            "source": source,
        }
        record_code = record_defaults.pop("record_code")
        record, r_created = RightsRecord.objects.get_or_create(
            record_code=record_code,
            defaults={**record_defaults, "record_code": record_code},
        )
        self.stdout.write(
            f"{'Created' if r_created else 'Already exists'}: "
            f"RightsRecord [{record.record_code}] '{record.title}'"
        )

        self.stdout.write(self.style.SUCCESS("\nDemo seed complete."))
        self.stdout.write(
            "Verify this data at: "
            "GET /api/v1/journeys/child-justice/topics/arrest-rights/rights/"
        )
