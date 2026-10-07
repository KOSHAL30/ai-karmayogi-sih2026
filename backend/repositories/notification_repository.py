# ==============================================================================
# AI KARMAYOGI — NOTIFICATION REPOSITORY (MongoDB)
# Real-Time Alerts, Assessment Reminders & Certificate Notifications
# ==============================================================================

import copy
import datetime
import logging
from typing import List, Dict, Any, Optional
import uuid

from app.models.entities import new_uuid, utcnow, _to_obj, _to_list

logger = logging.getLogger(__name__)


def _format_notification(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return None
    created_at = doc.get("created_at")
    if isinstance(created_at, datetime.datetime):
        created_at_str = created_at.isoformat()
    elif isinstance(created_at, str):
        created_at_str = created_at
    else:
        created_at_str = utcnow().isoformat()

    notif_id = str(doc.get("_id") or doc.get("id") or "")
    return {
        "id": notif_id,
        "user_id": str(doc.get("user_id", "")),
        "title": doc.get("title", ""),
        "message": doc.get("message", ""),
        "notification_type": doc.get("notification_type", "INFO"),
        "priority": doc.get("priority", "NORMAL"),
        "action_url": doc.get("action_url"),
        "is_read": bool(doc.get("is_read", False)),
        "created_at": created_at_str,
    }


class NotificationRepository:
    """Manages notifications with MongoDB persistence and in-memory demo fallback."""

    def __init__(self, db: Any):
        self.db = db
        self.collection = db["notifications"] if db is not None and hasattr(db, "__getitem__") else None

    async def get_user_notifications(self, user_id: str, limit: int = 20) -> Dict[str, Any]:
        """Fetches notifications for a user, ordered by recency, with unread badge count."""
        user_id_str = str(user_id)
        if self.collection is not None:
            try:
                cursor = self.collection.find({"user_id": user_id_str}).sort("created_at", -1).limit(limit)
                db_notes = await cursor.to_list(length=limit)
                if db_notes:
                    notes = [_format_notification(n) for n in db_notes]
                    unread = sum(1 for n in notes if not n["is_read"])
                    total = await self.collection.count_documents({"user_id": user_id_str})
                    return {
                        "total_notifications": max(total, len(notes)),
                        "unread_count": unread,
                        "notifications": notes,
                    }
            except Exception as e:
                logger.warning("NotificationRepository.get_user_notifications MongoDB query failed: %s", e)

        return {
            "total_notifications": 0,
            "unread_count": 0,
            "notifications": [],
        }

    async def mark_as_read(self, notification_id: str) -> bool:
        """Marks a notification as read."""
        if not notification_id:
            return False
        notif_id_str = str(notification_id)

        if self.collection is not None:
            try:
                await self.collection.update_one(
                    {"$or": [{"_id": notif_id_str}, {"id": notif_id_str}]},
                    {"$set": {"is_read": True}},
                )
            except Exception as e:
                logger.warning("NotificationRepository.mark_as_read MongoDB update failed: %s", e)

        return True

    async def mark_all_as_read(self, user_id: str) -> bool:
        """Bulk marks all notifications for the given user as read."""
        if not user_id:
            return False
        user_id_str = str(user_id)

        if self.collection is not None:
            try:
                await self.collection.update_many(
                    {"user_id": user_id_str},
                    {"$set": {"is_read": True}},
                )
            except Exception as e:
                logger.warning("NotificationRepository.mark_all_as_read MongoDB update failed: %s", e)

        return True

    async def create_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = "INFO",
        priority: str = "NORMAL",
        action_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates and stores a new notification."""
        note_id = new_uuid()
        note_dict = {
            "id": note_id,
            "user_id": str(user_id),
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "priority": priority,
            "action_url": action_url,
            "is_read": False,
            "created_at": utcnow().isoformat(),
        }

        if self.collection is not None:
            try:
                mongo_doc = {**note_dict, "_id": note_id}
                await self.collection.insert_one(mongo_doc)
            except Exception as e:
                logger.warning("NotificationRepository.create_notification MongoDB insert failed: %s", e)

        return note_dict
