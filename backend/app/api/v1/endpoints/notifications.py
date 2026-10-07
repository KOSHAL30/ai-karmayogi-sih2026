# ==============================================================================
# AI KARMAYOGI — NOTIFICATIONS ENDPOINTS
# In-App Administrative Alerts, Assessment Deadlines & Priority Dispatches
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from app.core.deps import get_current_user_payload
from app.schemas.analytics import (
    NotificationListResponse,
    NotificationReadRequest,
)
try:
    from services.notification_service import NotificationService
except ImportError:
    from app.services.notification_service import NotificationService

router = APIRouter()
notif_service = NotificationService()


@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db),
):
    """Fetches user notifications, ordered by priority and recency, with unread badge count."""
    try:
        user_id = payload.get("sub", "00000000-0000-0000-0000-000000000001")
        return await notif_service.list_notifications(db, user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notifications: {str(e)}",
        )


@router.post("/read")
async def mark_notification_read(
    req: NotificationReadRequest,
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db),
):
    """Marks a specific notification as read."""
    try:
        success = await notif_service.mark_read(db, req.notification_id)
        return {"status": "SUCCESS", "notification_id": req.notification_id, "is_read": True}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as read: {str(e)}",
        )


@router.post("/read-all")
async def mark_all_notifications_read(
    payload: dict = Depends(get_current_user_payload),
    db = Depends(get_db),
):
    """Bulk marks all notifications for the active user as read."""
    try:
        user_id = payload.get("sub", "00000000-0000-0000-0000-000000000001")
        await notif_service.mark_all_read(db, user_id)
        return {"status": "SUCCESS", "message": "All notifications marked as read."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark all notifications as read: {str(e)}",
        )
