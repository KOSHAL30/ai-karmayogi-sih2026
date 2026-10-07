# ==============================================================================
# AI KARMAYOGI — NOTIFICATION SERVICE
# Priority Filtering, Real-Time Alerts & Lifecycle Event Triggers
# ==============================================================================

from typing import Dict, Any, List, Optional
from repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(
        self,
        db: Any = None,
        notif_repo: Optional[NotificationRepository] = None,
    ):
        self.db = db
        self.notif_repo = notif_repo or (NotificationRepository(db) if db is not None else None)

    def _resolve_repo(self, db: Any = None) -> NotificationRepository:
        if self.notif_repo is not None and (db is None or db == self.db):
            return self.notif_repo
        target_db = db if db is not None else self.db
        return NotificationRepository(target_db)

    async def list_notifications(
        self, db: Any = None, user_id: Optional[str] = None, limit: int = 20
    ) -> Dict[str, Any]:
        """Gets notifications and unread badge count."""
        if isinstance(db, str) and user_id is None:
            user_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.get_user_notifications(user_id=user_id, limit=limit)

    async def mark_read(
        self, db: Any = None, notification_id: Optional[str] = None
    ) -> bool:
        """Marks a notification as read."""
        if isinstance(db, str) and notification_id is None:
            notification_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.mark_as_read(notification_id=notification_id)

    async def mark_all_read(
        self, db: Any = None, user_id: Optional[str] = None
    ) -> bool:
        """Marks all notifications as read for a user."""
        if isinstance(db, str) and user_id is None:
            user_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.mark_all_as_read(user_id=user_id)

    async def dispatch_event(
        self,
        db: Any = None,
        user_id: Optional[str] = None,
        event_type: str = "INFO",
        title: str = "",
        message: str = "",
        priority: str = "NORMAL",
        action_url: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Dispatches an administrative or learning alert."""
        if isinstance(db, str) and user_id is None:
            user_id = db
            db = None
        repo = self._resolve_repo(db)
        return await repo.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=event_type,
            priority=priority,
            action_url=action_url,
        )
