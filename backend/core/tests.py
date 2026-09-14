"""
SafeSpace API tests — read-only endpoints.

Tests cover:
  - journey listing (active only)
  - inactive journey exclusion
  - topic filtering by journey (journey-scoped URL)
  - inactive topic exclusion
  - duplicate topic slugs across different journeys
  - VERIFIED rights records returned
  - REVIEW_REQUIRED records excluded
  - EXPIRED records excluded
  - ARCHIVED records excluded
  - inactive rights records excluded
  - rights detail by record_code
  - unknown record_code returns 404
  - unverified record cannot be retrieved from trusted endpoint
  - source provenance in RightsRecord responses
  - cross-journey record leak prevention

No write operations are tested (none exist).
"""

import datetime

from django.test import TestCase
from django.urls import reverse

from .models import Journey, LegalSource, RightsRecord, Topic


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_journey(name="Test Journey", slug="test-journey", active=True, risk="LOW"):
    return Journey.objects.create(
        name=name,
        slug=slug,
        description="Test journey description.",
        risk_default=risk,
        active=active,
    )


def make_topic(journey, title="Test Topic", slug="test-topic", active=True, sort_order=0):
    return Topic.objects.create(
        journey=journey,
        title=title,
        slug=slug,
        description="Test topic description.",
        default_risk_level="LOW",
        sort_order=sort_order,
        active=active,
    )


def make_source(title="Test Act", status="VERIFIED"):
    return LegalSource.objects.create(
        title=title,
        source_type="LEGISLATION",
        publisher="National Assembly of Kenya",
        jurisdiction="Kenya",
        url="https://example.com/test-act",
        last_verified=datetime.date.today(),
        status=status,
    )


def make_record(
    journey,
    topic,
    source,
    record_code="TEST-001",
    status="VERIFIED",
    active=True,
    risk_level="LOW",
    title="Test Right",
):
    return RightsRecord.objects.create(
        record_code=record_code,
        journey=journey,
        topic=topic,
        jurisdiction="Kenya",
        title=title,
        plain_language_summary="You have this right.",
        legal_reference="Test Act, Section 1",
        section_reference="s.1",
        source=source,
        risk_level=risk_level,
        next_step_text="",
        limitations="",
        last_verified=datetime.date.today(),
        status=status,
        active=active,
    )


# ---------------------------------------------------------------------------
# Journey list tests
# ---------------------------------------------------------------------------

class JourneyListTests(TestCase):

    def test_active_journeys_returned(self):
        """Active journeys appear in the list."""
        make_journey(name="Active Journey", slug="active-journey", active=True)
        response = self.client.get(reverse("journey-list"))
        self.assertEqual(response.status_code, 200)
        slugs = [j["slug"] for j in response.json()]
        self.assertIn("active-journey", slugs)

    def test_inactive_journey_excluded(self):
        """Inactive journeys must not appear in the public list."""
        make_journey(name="Hidden Journey", slug="hidden-journey", active=False)
        response = self.client.get(reverse("journey-list"))
        slugs = [j["slug"] for j in response.json()]
        self.assertNotIn("hidden-journey", slugs)

    def test_journey_list_returns_200(self):
        """Journey list always returns HTTP 200."""
        response = self.client.get(reverse("journey-list"))
        self.assertEqual(response.status_code, 200)

    def test_empty_journey_list_returns_empty_array(self):
        """No journeys means an empty array, not an error."""
        response = self.client.get(reverse("journey-list"))
        self.assertEqual(response.json(), [])

    def test_journey_fields_present(self):
        """Journey responses expose the expected public fields."""
        make_journey(name="Field Journey", slug="field-journey")
        response = self.client.get(reverse("journey-list"))
        journey = response.json()[0]
        for field in ("id", "name", "slug", "description", "risk_default"):
            self.assertIn(field, journey)


# ---------------------------------------------------------------------------
# Topic list tests
# ---------------------------------------------------------------------------

class TopicListTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="my-journey")

    def test_topics_returned_for_valid_journey(self):
        """Active topics for an active journey are returned."""
        make_topic(self.journey, slug="topic-one")
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_inactive_topic_excluded(self):
        """Inactive topics are excluded; active ones are included."""
        make_topic(self.journey, slug="active-topic", active=True)
        make_topic(self.journey, slug="inactive-topic", active=False)
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        response = self.client.get(url)
        slugs = [t["slug"] for t in response.json()]
        self.assertIn("active-topic", slugs)
        self.assertNotIn("inactive-topic", slugs)

    def test_unknown_journey_returns_404(self):
        """An unrecognised journey slug returns 404."""
        url = reverse("topic-list", kwargs={"journey_slug": "does-not-exist"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_inactive_journey_returns_404(self):
        """An inactive journey is treated as not found."""
        inactive = make_journey(slug="inactive-journey", active=False)
        make_topic(inactive, slug="some-topic")
        url = reverse("topic-list", kwargs={"journey_slug": "inactive-journey"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_topic_fields_include_journey_slug(self):
        """Topic responses carry journey_slug for navigation context."""
        make_topic(self.journey, slug="my-topic")
        url = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        response = self.client.get(url)
        topic = response.json()[0]
        self.assertEqual(topic["journey_slug"], "my-journey")

    def test_duplicate_slug_in_different_journey_is_scoped(self):
        """
        The same topic slug may exist in two different journeys.
        Each journey's topic list returns only its own topics.
        """
        journey_b = make_journey(name="Journey B", slug="journey-b")
        # Both journeys have a topic with slug "overview"
        make_topic(self.journey, title="Overview A", slug="overview")
        make_topic(journey_b,   title="Overview B", slug="overview")

        url_a = reverse("topic-list", kwargs={"journey_slug": "my-journey"})
        url_b = reverse("topic-list", kwargs={"journey_slug": "journey-b"})

        resp_a = self.client.get(url_a)
        resp_b = self.client.get(url_b)

        titles_a = [t["title"] for t in resp_a.json()]
        titles_b = [t["title"] for t in resp_b.json()]

        self.assertIn("Overview A", titles_a)
        self.assertNotIn("Overview B", titles_a)
        self.assertIn("Overview B", titles_b)
        self.assertNotIn("Overview A", titles_b)


# ---------------------------------------------------------------------------
# Rights list tests
# ---------------------------------------------------------------------------

class RightsListTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="rights-journey")
        self.topic   = make_topic(self.journey, slug="rights-topic")
        self.source  = make_source()

    def _url(self, journey_slug="rights-journey", topic_slug="rights-topic"):
        return reverse(
            "rights-list",
            kwargs={"journey_slug": journey_slug, "topic_slug": topic_slug},
        )

    def test_verified_record_returned(self):
        """A VERIFIED active record appears in the rights list."""
        make_record(self.journey, self.topic, self.source, record_code="V-001", status="VERIFIED")
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, 200)
        codes = [r["record_code"] for r in response.json()]
        self.assertIn("V-001", codes)

    def test_archived_record_excluded(self):
        """ARCHIVED records must not appear in the trusted endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="A-001", status="ARCHIVED")
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("A-001", codes)

    def test_expired_record_excluded(self):
        """EXPIRED records must not appear in the trusted endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="E-001", status="EXPIRED")
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("E-001", codes)

    def test_review_required_record_excluded(self):
        """REVIEW_REQUIRED records must not appear in the trusted endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="R-001", status="REVIEW_REQUIRED")
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("R-001", codes)

    def test_inactive_record_excluded(self):
        """Inactive records are excluded even if status is VERIFIED."""
        make_record(self.journey, self.topic, self.source, record_code="I-001", status="VERIFIED", active=False)
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("I-001", codes)

    def test_unknown_journey_returns_404(self):
        """An unrecognised journey slug returns 404."""
        response = self.client.get(self._url(journey_slug="no-such-journey"))
        self.assertEqual(response.status_code, 404)

    def test_unknown_topic_within_journey_returns_404(self):
        """A topic slug that doesn't belong to the journey returns 404."""
        response = self.client.get(self._url(topic_slug="no-such-topic"))
        self.assertEqual(response.status_code, 404)

    def test_source_provenance_present_in_response(self):
        """Every rights record response carries its source provenance."""
        make_record(self.journey, self.topic, self.source, record_code="P-001", status="VERIFIED")
        response = self.client.get(self._url())
        record = response.json()[0]
        self.assertIn("source", record)
        for field in ("title", "publisher", "url", "last_verified", "status"):
            self.assertIn(field, record["source"])

    def test_records_do_not_leak_across_journeys(self):
        """
        A record belonging to journey B must not appear when querying
        journey A's topic, even if the topic slug is reused.
        """
        journey_b = make_journey(name="Other Journey", slug="other-journey")
        topic_b   = make_topic(journey_b, slug="rights-topic")   # same slug, different journey
        make_record(journey_b, topic_b, self.source, record_code="B-001", status="VERIFIED")

        # Query journey A — should see no records (none belong to journey A)
        codes = [r["record_code"] for r in self.client.get(self._url()).json()]
        self.assertNotIn("B-001", codes)

    def test_topic_slug_resolved_within_correct_journey(self):
        """
        When topic slug 'rights-topic' exists in two journeys, the endpoint
        returns only the records for the requested journey.
        """
        journey_b = make_journey(name="Journey B", slug="journey-b")
        topic_b   = make_topic(journey_b, slug="rights-topic")
        make_record(self.journey, self.topic, self.source, record_code="JA-001", status="VERIFIED")
        make_record(journey_b,    topic_b,    self.source, record_code="JB-001", status="VERIFIED")

        codes_a = [r["record_code"] for r in self.client.get(
            self._url(journey_slug="rights-journey", topic_slug="rights-topic")
        ).json()]
        codes_b = [r["record_code"] for r in self.client.get(
            self._url(journey_slug="journey-b", topic_slug="rights-topic")
        ).json()]

        self.assertIn("JA-001", codes_a)
        self.assertNotIn("JB-001", codes_a)
        self.assertIn("JB-001", codes_b)
        self.assertNotIn("JA-001", codes_b)


# ---------------------------------------------------------------------------
# Rights detail tests
# ---------------------------------------------------------------------------

class RightsDetailTests(TestCase):

    def setUp(self):
        self.journey = make_journey(slug="detail-journey")
        self.topic   = make_topic(self.journey, slug="detail-topic")
        self.source  = make_source()

    def test_verified_record_returned_by_code(self):
        """A known, verified, active record is returned with HTTP 200."""
        make_record(self.journey, self.topic, self.source, record_code="DET-001")
        url = reverse("rights-detail", kwargs={"record_code": "DET-001"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["record_code"], "DET-001")

    def test_unknown_record_code_returns_404(self):
        """An unrecognised record_code returns 404."""
        url = reverse("rights-detail", kwargs={"record_code": "UNKNOWN-999"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_archived_record_returns_404_on_detail(self):
        """ARCHIVED records are not retrievable through the public detail endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="ARC-001", status="ARCHIVED")
        url = reverse("rights-detail", kwargs={"record_code": "ARC-001"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_expired_record_returns_404_on_detail(self):
        """EXPIRED records are not retrievable through the public detail endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="EXP-001", status="EXPIRED")
        url = reverse("rights-detail", kwargs={"record_code": "EXP-001"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_review_required_record_returns_404_on_detail(self):
        """REVIEW_REQUIRED records are not retrievable through the public detail endpoint."""
        make_record(self.journey, self.topic, self.source, record_code="REV-001", status="REVIEW_REQUIRED")
        url = reverse("rights-detail", kwargs={"record_code": "REV-001"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_inactive_record_returns_404_on_detail(self):
        """Inactive records are not retrievable even if VERIFIED."""
        make_record(self.journey, self.topic, self.source, record_code="INA-001", active=False)
        url = reverse("rights-detail", kwargs={"record_code": "INA-001"})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_detail_includes_source_provenance(self):
        """Every detail response carries full source provenance."""
        make_record(self.journey, self.topic, self.source, record_code="SRC-001")
        url = reverse("rights-detail", kwargs={"record_code": "SRC-001"})
        data = self.client.get(url).json()
        self.assertIn("source", data)
        for field in ("title", "publisher", "url", "last_verified", "status"):
            self.assertIn(field, data["source"])

    def test_detail_includes_journey_and_topic_slugs(self):
        """Detail responses include navigation slugs for frontend breadcrumbs."""
        make_record(self.journey, self.topic, self.source, record_code="NAV-001")
        url = reverse("rights-detail", kwargs={"record_code": "NAV-001"})
        data = self.client.get(url).json()
        self.assertEqual(data["journey_slug"], "detail-journey")
        self.assertEqual(data["topic_slug"], "detail-topic")
