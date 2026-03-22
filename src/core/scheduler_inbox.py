import asyncio
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .tasks import sync_shipment_status


async def main():
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Vladivostok"))

    scheduler.add_job(
        sync_shipment_status,
        IntervalTrigger(seconds=15),
        id="sync_shipment_status",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())