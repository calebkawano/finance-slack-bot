import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# "daily" sends every weekday, "weekly" sends once per week
SCHEDULE_TYPE = os.getenv("SCHEDULE_TYPE", "weekly")

# Day(s) of week for weekly schedule (e.g. monday,friday)
SCHEDULE_DAY = os.getenv("SCHEDULE_DAY", "mon") # mon, tue, wed, thu, fri, sat, sun for weekly schedule

# Time to send (24-hour format)
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8")) # 0-23
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0")) # 0-59

TIMEZONE = os.getenv("TIMEZONE", "America/Los_Angeles")
