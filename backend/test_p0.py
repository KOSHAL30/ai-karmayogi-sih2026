
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.core.config import settings
from repositories.analytics_repository import AnalyticsRepository
from repositories.certificate_repository import CertificateRepository
from repositories.notification_repository import NotificationRepository

async def test():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    
    analytics_repo = AnalyticsRepository(db)
    kpis = await analytics_repo.get_macro_kpis()
    print('KPIs:', {k: v['value'] for k, v in kpis.items()})

    cert_repo = CertificateRepository(db)
    certs = await cert_repo.get_all('00000000-0000-0000-0000-000000000001')
    print('Certs count:', len(certs))

    notif_repo = NotificationRepository(db)
    notifs = await notif_repo.get_user_notifications('00000000-0000-0000-0000-000000000001')
    print('Notifications count:', notifs['total_notifications'])

if __name__ == '__main__':
    asyncio.run(test())

