"""爬虫定时调度入口。"""

import asyncio
import os
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

sys.path.insert(0, os.path.dirname(__file__))

from adapters.tencent import TencentAdapter
from pipeline.dedup import run_adapter

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://jobradar:jobradar_dev@db:5432/jobradar"
)
SCHEDULE_HOUR = int(os.getenv("CRAWLER_SCHEDULE_HOUR", "2"))

ADAPTERS = [TencentAdapter]


async def crawl_all():
    for adapter_cls in ADAPTERS:
        await run_adapter(adapter_cls, DATABASE_URL)


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(crawl_all, "cron", hour=SCHEDULE_HOUR, minute=0, id="daily_crawl")
    scheduler.start()
    print(f"Crawler scheduler started. Daily run at {SCHEDULE_HOUR}:00 UTC")
    print(f"Registered adapters: {[a.__name__ for a in ADAPTERS]}")

    if os.getenv("CRAWLER_RUN_ON_START", "1") == "1":
        await crawl_all()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
