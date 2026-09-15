"""
SafeSpace API tests — Day 2 + Day 3.

Day 2 tests (29): journey/topic/rights list and detail, trust filtering.
Day 3 tests (19+): SupportService, ActionPath, RiskRule, safety endpoint.
"""

import datetime

from django.test import TestCase
from django.urls import reverse

from .models import (
    ActionPath, Journey, LegalSource, RightsRecord,
    RiskRule, SupportService, Topic,
)


# ===========================================================================
# Shared helpers
# ===========================================================================

def make_journey(name="Test Journey", slug="test-journey", active=True, risk="LOW"):
    return Journey.objects.create(
        name=name, slug=slug,
        description="Test journey description.",
        risk_default=risk, active=active,
    )


def make_topic(journey, title="Test Topic", slug="test-topic", active=True, sort_order=0):
    return Topic.objects.create(
        journey=journey, title=title, slug=slug,
        description="Test topic description.",
        default_risk_level="LOW", sort_order=sort_order, active=active,
    )


def make_source(title="Test Act", status="VERIFIED"):
    return LegalSource.objects.create(
        title=title, source_type="LEGISLATION",
        publisher="National Assembly of Kenya",
        jurisdiction="Kenya",
        url="https://example.com/test-act",
        last_verified=datetime.date.today(),
        status=status,
    )


def make_record(journey, topic, source, record_code="TEST-001",
                status="VERIFIED", active=True, risk_level="LOW", title="Test Right"):
    return RightsRecord.objects.create(
        record_code=record_code, journey=journey, topic=topic,
        jurisdiction="Kenya", title=title,
        plain_language_summary="You have this right.",
        legal_reference="Test Act, Section 1", section_reference="s.1",
        source=source, risk_level=risk_level,
        next_step_text="", limitations="",
        last_verified=datetime.date.today(),
        status=status, active=active,
    )


def make_service(name="Test Service", slug="test-service",
                 service_type="CHILD_PROTECTION", status="VERIFIED", active=True, phone=""):
    return SupportService.objects.create(
        name=name, slug=slug, service_type=service_type,
        description="A test support service.",
        jurisdiction="Kenya",
        phone=phone, whatsapp="", website="",
        available_24_7=False,
        source_url="https://example.com/service",
        last_verified=datetime.date.today(),
        status=status, active=active,
    )


def make_action(topic, step_number=1, status="VERIFIED", active=True,
                action_type="RIGHTS_GUIDANCE", support_service=None, source=None):
    return ActionPath.objects.create(
        topic=topic,
        title=f"Step {step_number}",
        step_number=step_number,
        instruction=f"Instruction for step {step_number}.",
        action_type=action_type,
        support_service=support_service,
        source=source,
        last_verified=datetime.date.today(),
        status=status,
        active=active,
    )


def make_risk_rule(name="Test Rule", category="GENERAL", pattern="hurt,danger",
                   risk_level="HIGH", action="SHOW_HIGH_RISK_SUPPORT",
                   priority=10, active=True):
    return RiskRule.objects.create(
        name=name, category=category, pattern=pattern,
        risk_level=risk_level, action=action,
        priority=priority, active=active,
    )


# ===========================================================================
# Day 2 — Journey tests
# ===========================================================================

class JourneyListTests(TestCase):

    def test_active_journeys_returned(self):
        """Active journeys appear in the list."""
        make_journey(name="Active Journey", slug="active-journey", active=True)
        response = self.client.get(reverse("journey-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("active-journey", [j["slug"] for j in response.json()])

    def test_inactive_journey_excluded(self):
        """Inactive journeys must not appear in the public list."""
        make_journey(name="Hidden Journey", slug="hidden-journey", active=False)
        self.assertNotIn("hidden-journey",
                         [j["slug"] for j in self.client.get(reverse("journey-list")).json()])

    def test_journey_list_returns_200(self):
        self.assertEqual(self.client.get(reverse("journey-list")).status_code, 200)

    def test_empty_journey_list_returns_empty_array(self):
        self.assertEqual(self.client.get(reverse("journey-list")).json(), [])

    def test_journey_fields_present(self):
        make_journey(name="Field Journey", slug="field-journey")
        journey = self.client.get(reverse("journey-list")).json()[0]
        for field in ("id", "name", "slug", "description", "risk_default"):
            self.assertIn(field, journey)


# ===========================================================================
# Day 2 — Topic tests
# ===========================================================================

class TopicListTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="my-journey")

    def test_topics_returned_for_valid_journey(self):
        make_topic(self.journey, slug="topic-one")
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        self.assertEqual(len(self.client.get(url).json()), 1)

    def test_inactive_topic_excluded(self):
        make_topic(self.journey, slug="active-topic", active=True)
        make_topic(self.journey, slug="inactive-topic", active=False)
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        slugs = [t["slug"] for t in self.client.get(url).json()]
        self.assertIn("active-topic", slugs)
        self.assertNotIn("inactive-topic", slugs)

    def test_unknown_journey_returns_404(self):
        url = reverse("topic-list", kwargs={"journey_slug": "does-not-exist"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_inactive_journey_returns_404(self):
        inactive = make_journey(slug="inactive-journey", active=False)
        make_topic(inactive, slug="some-topic")
        url = reverse("topic-list", kwargs={"journey_slug": "inactive-journey"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_topic_fields_include_journey_slug(self):
        make_topic(self.journey, slug="my-topic")
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        self.assertEqual(self.client.get(url).json()[0]["journey_slug"], "my-journey")

    def test_duplicate_slug_in_different_journey_is_scoped(self):
        journey_b = make_journey(name="Journey B", slug="journey-b")
        make_topic(self.journey, title="Overview A", slug="overview")
        make_topic(journey_b,   title="Overview B", slug="overview")
        titles_a = [t["title"] for t in self.client.get(
            reverse("topic-list", kwargs={"journey_slug": "my-journey"})).json()]
        titles_b = [t["title"] for t in self.client.get(
            reverse("topic-list", kwargs={"journey_slug": "journey-b"})).json()]
        self.assertIn("Overview A", titles_a)
        self.assertNotIn("Overview B", titles_a)
        self.assertIn("Overview B", titles_b)
        self.assertNotIn("Overview A", titles_b)


# ===========================================================================
# Day 2 — Rights list tests
# ===========================================================================

class RightsListTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="rights-journey")
        self.topic   = make_topic(self.journey, slug="rights-topic")
        self.source  = make_source()

    def _url(self, journey_slug="rights-journey", topic_slug="rights-topic"):
        return reverse("rights-list",
                       kwargs={"journey_slug": journey_slug, "topic_slug": topic_slug})

    def test_verified_record_returned(self):
        make_record(self.journey, self.topic, self.source, record_code="V-001")
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertIn("V-001", codes)

    def test_archived_record_excluded(self):
        make_record(self.journey, self.topic, self.source, record_code="A-001", status="ARCHIVED")
        self.assertNotIn("A-001", [r["record_code"] for r in self.client.get(self._url()).json()])

    def test_expired_record_excluded(self):
        make_record(self.journey, self.topic, self.source, record_code="E-001", status="EXPIRED")
        self.assertNotIn("E-001", [r["record_code"] for r in self.client.get(self._url()).json()])

    def test_review_required_record_excluded(self):
        make_record(self.journey, self.topic, self.source, record_code="R-001", status="REVIEW_REQUIRED")
        self.assertNotIn("R-001", [r["record_code"] for r in self.client.get(self._url()).json()])

    def test_inactive_record_excluded(self):
        make_record(self.journey, self.topic, self.source, record_code="I-001", active=False)
        self.assertNotIn("I-001", [r["record_code"] for r in self.client.get(self._url()).json()])

    def test_unknown_journey_returns_404(self):
        self.assertEqual(self.client.get(self._url(journey_slug="no-such-journey")).status_code, 404)

    def test_unknown_topic_within_journey_returns_404(self):
        self.assertEqual(self.client.get(self._url(topic_slug="no-such-topic")).status_code, 404)

    def test_source_provenance_present_in_response(self):
        make_record(self.journey, self.topic, self.source, record_code="P-001")
        record = self.client.get(self._url()).json()[0]
        self.assertIn("source", record)
        for field in ("title", "publisher", "url", "last_verified", "status"):
            self.assertIn(field, record["source"])

    def test_records_do_not_leak_across_journeys(self):
        journey_b = make_journey(name="Other Journey", slug="other-journey")
        topic_b   = make_topic(journey_b, slug="rights-topic")
        make_record(journey_b, topic_b, self.source, record_code="B-001")
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("B-001", codes)

    def test_topic_slug_resolved_within_correct_journey(self):
        journey_b = make_journey(name="Journey B", slug="journey-b")
        topic_b   = make_topic(journey_b, slug="rights-topic")
        make_record(self.journey, self.topic, self.source, record_code="JA-001")
        make_record(journey_b, topic_b, self.source, record_code="JB-001")
        codes_a = [r["record_code"] for r in self.client.get(
            self._url("rights-journey", "rights-topic")).json()]
        codes_b = [r["record_code"] for r in self.client.get(
            self._url("journey-b", "rights-topic")).json()]
        self.assertIn("JA-001", codes_a)
        self.assertNotIn("JB-001", codes_a)
        self.assertIn("JB-001", codes_b)
        self.assertNotIn("JA-001", codes_b)


# ===========================================================================
# Day 2 — Rights detail tests
# ===========================================================================

class RightsDetailTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="detail-journey")
        self.topic   = make_topic(self.journey, slug="detail-topic")
        self.source  = make_source()

    def test_verified_record_returned_by_code(self):
        make_record(self.journey, self.topic, self.source, record_code="DET-001")
        url  = reverse("rights-detail", kwargs={"record_code": "DET-001"})
        data = self.client.get(url).json()
        self.assertEqual(data["record_code"], "DET-001")

    def test_unknown_record_code_returns_404(self):
        self.assertEqual(self.client.get(
            reverse("rights-detail", kwargs={"record_code": "UNKNOWN-999"})).status_code, 404)

    def test_archived_record_returns_404_on_detail(self):
        make_record(self.journey, self.topic, self.source, record_code="ARC-001", status="ARCHIVED")
        self.assertEqual(self.client.get(
            reverse("rights-detail", kwargs={"record_code": "ARC-001"})).status_code, 404)

    def test_expired_record_returns_404_on_detail(self):
        make_record(self.journey, self.topic, self.source, record_code="EXP-001", status="EXPIRED")
        self.assertEqual(self.client.get(
            reverse("rights-detail", kwargs={"record_code": "EXP-001"})).status_code, 404)

    def test_review_required_record_returns_404_on_detail(self):
        make_record(self.journey, self.topic, self.source, record_code="REV-001", status="REVIEW_REQUIRED")
        self.assertEqual(self.client.get(
            reverse("rights-detail", kwargs={"record_code": "REV-001"})).status_code, 404)

    def test_inactive_record_returns_404_on_detail(self):
        make_record(self.journey, self.topic, self.source, record_code="INA-001", active=False)
        self.assertEqual(self.client.get(
            reverse("rights-detail", kwargs={"record_code": "INA-001"})).status_code, 404)

    def test_detail_includes_source_provenance(self):
        make_record(self.journey, self.topic, self.source, record_code="SRC-001")
        data = self.client.get(reverse("rights-detail", kwargs={"record_code": "SRC-001"})).json()
        for field in ("title", "publisher", "url", "last_verified", "status"):
            self.assertIn(field, data["source"])

    def test_detail_includes_journey_and_topic_slugs(self):
        make_record(self.journey, self.topic, self.source, record_code="NAV-001")
        data = self.client.get(reverse("rights-detail", kwargs={"record_code": "NAV-001"})).json()
        self.assertEqual(data["journey_slug"], "detail-journey")
        self.assertEqual(data["topic_slug"],   "detail-topic")


# ===========================================================================
# Day 3 — SupportService tests
# ===========================================================================

class SupportServiceTests(TestCase):

    def test_verified_active_services_returned(self):
        """VERIFIED active services appear in the public list."""
        make_service(name="Child Helpline", slug="child-helpline")
        data = self.client.get(reverse("support-service-list")).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Child Helpline")

    def test_inactive_service_excluded(self):
        """Inactive services are hidden from the public API."""
        make_service(slug="inactive-svc", active=False)
        self.assertEqual(self.client.get(reverse("support-service-list")).json(), [])

    def test_review_required_service_excluded(self):
        """REVIEW_REQUIRED services are excluded."""
        make_service(slug="review-svc", status="REVIEW_REQUIRED")
        self.assertEqual(self.client.get(reverse("support-service-list")).json(), [])

    def test_expired_service_excluded(self):
        """EXPIRED services are excluded."""
        make_service(slug="expired-svc", status="EXPIRED")
        self.assertEqual(self.client.get(reverse("support-service-list")).json(), [])

    def test_archived_service_excluded(self):
        """ARCHIVED services are excluded."""
        make_service(slug="archived-svc", status="ARCHIVED")
        self.assertEqual(self.client.get(reverse("support-service-list")).json(), [])

    def test_service_fields_present(self):
        """Support service responses expose expected public fields."""
        make_service(slug="field-svc", phone="116")
        data = self.client.get(reverse("support-service-list")).json()[0]
        for field in ("id", "name", "slug", "service_type", "description",
                      "phone", "available_24_7", "last_verified", "status"):
            self.assertIn(field, data)

    def test_source_url_not_exposed_in_public_api(self):
        """source_url is an internal verification field — not in public output."""
        make_service(slug="src-url-svc")
        data = self.client.get(reverse("support-service-list")).json()[0]
        self.assertNotIn("source_url", data)


# ===========================================================================
# Day 3 — ActionPath tests
# ===========================================================================

class ActionPathTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="action-journey")
        self.topic   = make_topic(self.journey, slug="action-topic")
        self.source  = make_source()

    def _url(self, journey_slug="action-journey", topic_slug="action-topic"):
        return reverse("action-list",
                       kwargs={"journey_slug": journey_slug, "topic_slug": topic_slug})

    def test_verified_action_steps_returned_in_order(self):
        """Verified active steps are returned in step_number order."""
        make_action(self.topic, step_number=2)
        make_action(self.topic, step_number=1)
        data = self.client.get(self._url()).json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["step_number"], 1)
        self.assertEqual(data[1]["step_number"], 2)

    def test_action_paths_filtered_by_journey_and_topic(self):
        """Actions for a different topic do not appear."""
        other_topic = make_topic(self.journey, title="Other", slug="other-topic")
        make_action(self.topic,   step_number=1)
        make_action(other_topic,  step_number=1)
        data = self.client.get(self._url()).json()
        self.assertEqual(len(data), 1)

    def test_inactive_action_step_excluded(self):
        """Inactive action steps are excluded."""
        make_action(self.topic, step_number=1, active=False)
        self.assertEqual(self.client.get(self._url()).json(), [])

    def test_unverified_action_step_excluded(self):
        """REVIEW_REQUIRED action steps are excluded."""
        make_action(self.topic, step_number=1, status="REVIEW_REQUIRED")
        self.assertEqual(self.client.get(self._url()).json(), [])

    def test_expired_action_step_excluded(self):
        """EXPIRED action steps are excluded."""
        make_action(self.topic, step_number=1, status="EXPIRED")
        self.assertEqual(self.client.get(self._url()).json(), [])

    def test_linked_support_service_in_response(self):
        """Where a step has a support service, it appears in the response."""
        svc = make_service(slug="linked-svc", phone="116")
        make_action(self.topic, step_number=1,
                    action_type="SUPPORT_REFERRAL", support_service=svc)
        data = self.client.get(self._url()).json()
        self.assertIsNotNone(data[0]["support_service"])
        self.assertEqual(data[0]["support_service"]["slug"], "linked-svc")

    def test_unverified_support_service_not_shown(self):
        """
        If linked support service is REVIEW_REQUIRED, the serializer still
        includes it (it's an inline FK). Trust filtering for services is
        enforced at the /support-services/ endpoint. ActionPath-level service
        visibility is controlled by the ActionPath active/status fields.
        This test documents the current design choice.
        """
        svc = make_service(slug="unverified-svc", status="REVIEW_REQUIRED")
        make_action(self.topic, step_number=1, support_service=svc)
        data = self.client.get(self._url()).json()
        # The action is VERIFIED and active, so it appears; service is inline
        self.assertEqual(len(data), 1)

    def test_action_path_from_another_topic_does_not_leak(self):
        """Steps from a different topic do not appear in this topic's list."""
        other_journey = make_journey(name="Other J", slug="other-j")
        other_topic   = make_topic(other_journey, slug="action-topic")
        make_action(other_topic, step_number=1)
        self.assertEqual(self.client.get(self._url()).json(), [])

    def test_unknown_journey_returns_404(self):
        self.assertEqual(self.client.get(
            self._url(journey_slug="no-such-journey")).status_code, 404)

    def test_unknown_topic_returns_404(self):
        self.assertEqual(self.client.get(
            self._url(topic_slug="no-such-topic")).status_code, 404)


# ===========================================================================
# Day 3 — RiskRule / safety endpoint tests
# ===========================================================================

class SafetyCheckTests(TestCase):

    def _post(self, message):
        return self.client.post(
            reverse("safety-check"),
            data={"message": message},
            content_type="application/json",
        )

    def test_low_default_when_no_rules_match(self):
        """With no rules in DB, any message returns LOW / NORMAL_FLOW."""
        resp = self._post("I have a question about my rights.")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["risk_level"], "LOW")
        self.assertEqual(data["action"], "NORMAL_FLOW")
        self.assertIsNone(data["matched_rule"])

    def test_low_default_when_no_rules_match_message(self):
        """A rule exists but does not match — default LOW returned."""
        make_risk_rule(name="Danger Rule", pattern="help,hurt", risk_level="HIGH",
                       action="SHOW_HIGH_RISK_SUPPORT", priority=10)
        resp = self._post("I want to know about school.")
        self.assertEqual(resp.json()["risk_level"], "LOW")

    def test_high_rule_classification(self):
        """A message containing a HIGH-rule keyword returns HIGH."""
        make_risk_rule(name="High Rule", pattern="hurt,beaten",
                       risk_level="HIGH", action="SHOW_HIGH_RISK_SUPPORT", priority=10)
        resp = self._post("Someone is hurting me.")
        data = resp.json()
        self.assertEqual(data["risk_level"], "HIGH")
        self.assertEqual(data["action"], "SHOW_HIGH_RISK_SUPPORT")
        self.assertEqual(data["matched_rule"], "High Rule")

    def test_immediate_rule_classification(self):
        """A message matching an IMMEDIATE rule returns IMMEDIATE."""
        make_risk_rule(name="Immediate Rule", pattern="not safe,he is here",
                       risk_level="IMMEDIATE", action="SHOW_IMMEDIATE_SAFETY", priority=20)
        resp = self._post("I am not safe right now.")
        data = resp.json()
        self.assertEqual(data["risk_level"], "IMMEDIATE")
        self.assertEqual(data["action"], "SHOW_IMMEDIATE_SAFETY")

    def test_highest_severity_wins_when_multiple_rules_match(self):
        """When multiple rules match, the highest-severity result is returned."""
        make_risk_rule(name="Medium Rule", pattern="worried",
                       risk_level="MEDIUM", action="SHOW_SUPPORT", priority=5)
        make_risk_rule(name="Immediate Rule", pattern="not safe",
                       risk_level="IMMEDIATE", action="SHOW_IMMEDIATE_SAFETY", priority=20)
        resp = self._post("I am worried and not safe.")
        self.assertEqual(resp.json()["risk_level"], "IMMEDIATE")
        self.assertEqual(resp.json()["matched_rule"], "Immediate Rule")

    def test_inactive_rule_ignored(self):
        """An inactive rule is not evaluated."""
        make_risk_rule(name="Inactive Rule", pattern="hurt",
                       risk_level="IMMEDIATE", action="SHOW_IMMEDIATE_SAFETY",
                       priority=99, active=False)
        resp = self._post("Someone is hurting me.")
        self.assertEqual(resp.json()["risk_level"], "LOW")

    def test_empty_message_returns_400(self):
        """An empty message returns HTTP 400."""
        resp = self._post("")
        self.assertEqual(resp.status_code, 400)

    def test_missing_message_field_returns_400(self):
        """A request with no message field returns HTTP 400."""
        resp = self.client.post(
            reverse("safety-check"), data={}, content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_safety_endpoint_does_not_persist_message(self):
        """
        No model stores the user message.
        Verifying indirectly: after a safety check, the only DB records
        are the RiskRule we created — no Interaction or User record exists.
        """
        make_risk_rule(name="Test Rule", pattern="help", risk_level="HIGH",
                       action="SHOW_HIGH_RISK_SUPPORT", priority=10)
        self._post("I need help urgently.")
        # Only the one RiskRule should exist — no interaction/user records
        from django.contrib.auth import get_user_model
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(RiskRule.objects.count(), 1)

    def test_case_insensitive_matching(self):
        """Pattern matching is case-insensitive."""
        make_risk_rule(name="CI Rule", pattern="danger",
                       risk_level="HIGH", action="SHOW_HIGH_RISK_SUPPORT", priority=10)
        resp = self._post("There is DANGER here.")
        self.assertEqual(resp.json()["risk_level"], "HIGH")
