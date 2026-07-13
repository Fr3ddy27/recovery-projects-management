from django.urls import path
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import create_project, DashboardLoginView


urlpatterns = [
    # MAIN
    path("", views.overview, name="overview"),
    path("projects/", views.projects, name="projects"),
    path("location/", views.location, name="location"),
    path("timeline/", views.timeline, name="timeline"),
    path("reports/", views.reports, name="reports"),

    # AUTHENTICATION
    path("login/", DashboardLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="overview"), name="logout"),

    # DATA ENTRY
    path("data-entry/", create_project, name="data-entry"),

    # APPROVALS
    path("approvals/", views.approvals, name="approvals"),
    path(
        "approvals/expenditure/<int:request_id>/approve/",
        views.approve_expenditure_request,
        name="approve_expenditure_request"
    ),

    path(
        "approvals/expenditure/<int:request_id>/reject/",
        views.reject_expenditure_request,
        name="reject_expenditure_request"
    ),

    #DISAPPROVALS
    path(
    "approvals/expenditure/rejected/",
    views.rejected_expenditure_requests,
    name="rejected_expenditure_requests"
    ),

    # ATTACHMENT DOWNLOAD
    path("gip/<int:pk>/download/", views.download_gip, name="download_gip"),

    # AREA COUNCIL
    path("api/area-councils/", views.area_councils_json, name="area_councils_json"),

    # DATA UPDATE
    path("data-update/", views.recovery_projects_table, name="data-update"),
    path("api/recovery-projects/", views.recovery_projects_api_list, name="recovery_projects_api_list"),
    path("api/recovery-projects/<int:pk>/", views.recovery_projects_api_detail, name="recovery_projects_api_detail"),

    # CHILD TABLES API - LOCATIONS
    path("api/project-locations/list/<int:project_id>/", views.project_locations_api_list, name="project_locations_api_list"),
    path("api/project-locations/<int:pk>/", views.project_locations_api_detail, name="project_locations_api_detail"),
    path("api/project-locations/create/<int:project_id>/", views.project_locations_api_create, name="project_locations_api_create"),

    # CHILD TABLES API - STATUS INDICATORS
    path("api/project-status-indicators/list/<int:project_id>/", views.project_status_indicators_api_list, name="project_status_indicators_api_list"),
    path("api/project-status-indicators/<int:pk>/", views.project_status_indicators_api_detail, name="project_status_indicators_api_detail"),
    path("api/project-status-indicators/create/<int:project_id>/", views.project_status_indicators_api_create, name="project_status_indicators_api_create"),

    path("approvals/expenditure/<int:request_id>/approve/", views.approve_expenditure_request, name="approve_expenditure_request"),
    path("approvals/expenditure/<int:request_id>/reject/", views.reject_expenditure_request, name="reject_expenditure_request"),

    #REGISTRAION
    path("register/", views.register_view, name="register"),

    #REPORT APPROVAL
    path(
        "approvals/status-indicator-attachments/",
        views.status_indicator_attachment_approvals,
        name="status_indicator_attachment_approvals"
    ),

    path(
        "approvals/status-indicator-attachments/<int:pk>/approve/",
        views.approve_status_indicator_attachment,
        name="approve_status_indicator_attachment"
    ),

    path(
        "approvals/status-indicator-attachments/<int:pk>/disapprove/",
        views.disapprove_status_indicator_attachment,
        name="disapprove_status_indicator_attachment"
    ),

    #REJECTED ATTACHMENTS
    path(
        "approvals/attachments/rejected/",
        views.rejected_status_indicator_attachments,
        name="rejected_status_indicator_attachments"
    ),
    #USERS LIST
    path("users/", views.users_list, name="users_list"),
    path("users/<int:user_id>/edit/", views.edit_user, name="edit_user"),
    path("users/<int:user_id>/password/", views.change_user_password, name="change_user_password"),

    #DELETE USER
    path("users/<int:user_id>/delete/", views.delete_user, name="delete_user"),
]


# MEDIA UPLOAD
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)