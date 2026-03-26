"""
Finance Slack Bot
-----------------
Fetches the top finance news story from Perplexity and posts it to a
private Slack channel on a configurable schedule (daily or weekly).

Usage:
  python bot.py            # start the scheduler
  python bot.py --test     # send one message immediately and exit
"""

import argparse
import logging
import sys

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    PERPLEXITY_API_KEY,
    SCHEDULE_DAY,
    SCHEDULE_HOUR,
    SCHEDULE_MINUTE,
    SCHEDULE_TYPE,
    SLACK_BOT_TOKEN,
    SLACK_CHANNEL_ID,
    TIMEZONE,
)
from perplexity_client import fetch_finance_news
from slack_client import send_finance_update

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

_DAY_ALIASES: dict[str, str] = {
    "mon": "mon",
    "monday": "mon",
    "tue": "tue",
    "tues": "tue",
    "tuesday": "tue",
    "wed": "wed",
    "wednesday": "wed",
    "thu": "thu",
    "thur": "thu",
    "thurs": "thu",
    "thursday": "thu",
    "fri": "fri",
    "friday": "fri",
    "sat": "sat",
    "saturday": "sat",
    "sun": "sun",
    "sunday": "sun",
}


def validate_config() -> None:
    missing = [
        name
        for name, value in [
            ("SLACK_BOT_TOKEN", SLACK_BOT_TOKEN),
            ("SLACK_CHANNEL_ID", SLACK_CHANNEL_ID),
            ("PERPLEXITY_API_KEY", PERPLEXITY_API_KEY),
        ]
        if not value
    ]
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        logger.error("Copy .env.example to .env and fill in the values.")
        sys.exit(1)


def run_update() -> None:
    logger.info("Running finance news update...")
    try:
        headline, summary, url = fetch_finance_news()
        logger.info("Fetched story: %s", headline)
        success = send_finance_update(headline, summary, url)
        if success:
            logger.info("Update delivered successfully.")
        else:
            logger.error("Failed to deliver update to Slack.")
    except Exception as exc:
        logger.exception("Unexpected error during update: %s", exc)


def _normalize_day_of_week(day: str) -> str:
    day_clean = day.strip().lower()
    return _DAY_ALIASES.get(day_clean, day_clean)


def build_triggers() -> list[CronTrigger]:
    tz = pytz.timezone(TIMEZONE)
    if SCHEDULE_TYPE == "daily":
        logger.info(
            "Schedule: daily (Mon–Fri) at %02d:%02d %s",
            SCHEDULE_HOUR,
            SCHEDULE_MINUTE,
            TIMEZONE,
        )
        return [
            CronTrigger(
                day_of_week="mon-fri",
                hour=SCHEDULE_HOUR,
                minute=SCHEDULE_MINUTE,
                timezone=tz,
            )
        ]

    # Weekly schedule can be a single day ("monday") or a comma-separated list
    # ("monday,friday").
    days = [
        _normalize_day_of_week(d)
        for d in SCHEDULE_DAY.split(",")
        if d.strip()
    ]
    if not days:
        logger.error("Invalid SCHEDULE_DAY=%r (expected at least one day)", SCHEDULE_DAY)
        sys.exit(1)

    logger.info(
        "Schedule: weekly on %s at %02d:%02d %s",
        ", ".join(days),
        SCHEDULE_HOUR,
        SCHEDULE_MINUTE,
        TIMEZONE,
    )
    return [
        CronTrigger(
            day_of_week=day,
            hour=SCHEDULE_HOUR,
            minute=SCHEDULE_MINUTE,
            timezone=tz,
        )
        for day in days
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Finance Slack Bot")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send one update immediately and exit (useful for verifying setup).",
    )
    args = parser.parse_args()

    validate_config()

    if args.test:
        logger.info("Test mode: sending one update now.")
        run_update()
        return

    scheduler = BlockingScheduler()
    for trigger in build_triggers():
        scheduler.add_job(run_update, trigger)

    logger.info("Bot started. Press Ctrl+C to stop.")
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped.")


if __name__ == "__main__":
    main()
