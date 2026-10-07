import asyncio
import os
import sys
import dns.resolver

sys.path.insert(0, os.path.abspath('.'))
from app.core.config import settings

async def test_dns():
    print("Testing DNS resolution for Atlas...")
    uri = settings.MONGODB_URI
    if "@" in uri:
        host = uri.split("@")[1].split("/")[0].split("?")[0]
    else:
        host = uri.replace("mongodb://", "").replace("mongodb+srv://", "").split("/")[0]
    print(f"Target Host: {host}")
    
    try:
        if uri.startswith("mongodb+srv://"):
            srv_record = f"_mongodb._tcp.{host}"
            answers = dns.resolver.resolve(srv_record, 'SRV')
            print("SRV Records found:")
            for rdata in answers:
                print(f" - {rdata.target}:{rdata.port}")
        else:
            answers = dns.resolver.resolve(host, 'A')
            print("A Records found:")
            for rdata in answers:
                print(f" - {rdata.address}")
    except Exception as e:
        print(f"DNS Resolution Failed: {e}")

asyncio.run(test_dns())
