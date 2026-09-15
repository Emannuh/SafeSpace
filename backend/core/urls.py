"""
SafeSpace core URL routing — v1.

Knowledge endpoints: GET only.
Safety endpoint: POST only (message not stored).
Included under /api/v1/ in safespace_backend/urls.py.
"""

from django.urls import path

from . import views

urlpatterns = [
    # --- Journeys ---
    path("journeys/",
         views.journey_list, name="journey-list"),

    path("journeys/<slug:journey_slug>/topics/",
         views.topic_list, name="topic-list"),

    path("journeys/<slug:journey_slug>/topics/<slug:topic_slug>/rights/",
         views.rights_list, name="rights-list"),

    path("journeys/<slug:journey_slug>/topics/<slug:topic_slug>/actions/",
         views.action_list, name="action-list"),

    # --- Rights detail ---
    path("rights/<str:record_code>/",
         views.rights_detail, name="rights-detail"),

    # --- Support services ---
    path("support-services/",
         views.support_service_list, name="support-service-list"),

    # --- Safety ---
    path("safety/check/",
         views.safety_check, name="safety-check"),
]
