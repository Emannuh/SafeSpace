"""
SafeSpace core URL routing.

All routes are read-only (GET only).
Included under /api/v1/ in safespace_backend/urls.py.

URL design:
  Topic slugs are only unique within a Journey (see the
  unique_topic_slug_per_journey constraint on the Topic model).
  The rights-list endpoint therefore uses the full
  journeys/<journey_slug>/topics/<topic_slug>/rights/ path so the
  backend can resolve the topic unambiguously without relying on
  a globally unique slug.
"""

from django.urls import path

from . import views

urlpatterns = [
    # List all active journeys
    path(
        "journeys/",
        views.journey_list,
        name="journey-list",
    ),
    # List active topics within a specific journey
    path(
        "journeys/<slug:journey_slug>/topics/",
        views.topic_list,
        name="topic-list",
    ),
    # List verified rights records for a topic within a journey
    path(
        "journeys/<slug:journey_slug>/topics/<slug:topic_slug>/rights/",
        views.rights_list,
        name="rights-list",
    ),
    # Single rights record by stable record_code
    path(
        "rights/<str:record_code>/",
        views.rights_detail,
        name="rights-detail",
    ),
]
