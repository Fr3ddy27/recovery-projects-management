from .models import ExpenditureUpdateRequest, ProjectStatusIndicators


def notifications_context(request):
    """
    Makes notification counts available in base.html.
    This runs on every page that extends base.html.
    """

    notifications = []
    notification_count = 0

    # If user is not logged in, show no notifications
    if not request.user.is_authenticated:
        return {
            "notification_count": 0,
            "notifications": [],
        }

    # =====================================================
    # SUPERUSER NOTIFICATIONS
    # =====================================================
    if request.user.is_superuser:

        # Pending expenditure approvals
        pending_expenditure_count = (
            ExpenditureUpdateRequest.objects
            .filter(status="pending")
            .count()
        )

        # Pending attachment approvals
        pending_attachment_count = (
            ProjectStatusIndicators.objects
            .filter(attachment__isnull=False)
            .exclude(attachment="")
            .filter(attachment_approved=False)
            .filter(disapproved_comment__isnull=True)
            .count()
        )

        if pending_expenditure_count > 0:
            notifications.append({
                "title": "Pending expenditure approvals",
                "message": f"{pending_expenditure_count} expenditure update(s) waiting for approval.",
                "url_name": "approvals",
                "icon": "✅",
                "count": pending_expenditure_count,
            })

        if pending_attachment_count > 0:
            notifications.append({
                "title": "Pending attachment approvals",
                "message": f"{pending_attachment_count} attachment(s) waiting for approval.",
                "url_name": "status_indicator_attachment_approvals",
                "icon": "📎",
                "count": pending_attachment_count,
            })

        notification_count = pending_expenditure_count + pending_attachment_count

    # =====================================================
    # NORMAL USER NOTIFICATIONS
    # =====================================================
    else:

        # Rejected expenditure updates for this logged-in user
        rejected_expenditure_count = (
            ExpenditureUpdateRequest.objects
            .filter(
                status="rejected",
                requested_by_id=request.user.id,
            )
            .count()
        )

        # Rejected attachments
        rejected_attachment_count = (
            ProjectStatusIndicators.objects
            .filter(attachment__isnull=False)
            .exclude(attachment="")
            .filter(attachment_approved=False)
            .filter(disapproved_comment__isnull=False)
            .exclude(disapproved_comment="")
            .count()
        )

        if rejected_expenditure_count > 0:
            notifications.append({
                "title": "Rejected data updates",
                "message": f"{rejected_expenditure_count} expenditure update(s) were rejected.",
                "url_name": "rejected_expenditure_requests",
                "icon": "❌",
                "count": rejected_expenditure_count,
            })

        if rejected_attachment_count > 0:
            notifications.append({
                "title": "Rejected attachments",
                "message": f"{rejected_attachment_count} attachment(s) were rejected by admin.",
                "url_name": "rejected_status_indicator_attachments",
                "icon": "📎",
                "count": rejected_attachment_count,
            })

        notification_count = rejected_expenditure_count + rejected_attachment_count

    return {
        "notification_count": notification_count,
        "notifications": notifications,
    }