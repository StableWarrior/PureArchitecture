import asyncio
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .tasks import sync_order_paid


async def main():
    scheduler = AsyncIOScheduler(timezone=ZoneInfo("Asia/Vladivostok"))

    scheduler.add_job(
        sync_order_paid,
        IntervalTrigger(seconds=10),
        id="sync_order_paid",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
