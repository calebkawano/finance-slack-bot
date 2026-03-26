# Finance Slack Bot

Automatically posts a top finance news story — sourced via the Perplexity API — to a private Slack channel on a configurable daily or weekly schedule.

**Example message:**
> Hi Experts, thought you might find this story interesting 📰
>
> **Fed Holds Rates Steady, Signals Two Cuts in 2025**
> The Federal Reserve kept its benchmark rate unchanged at 5.25–5.50% on Wednesday, while updated projections still point to two quarter-point cuts before year-end.
>
> Here is the link to the article: https://...

---

## Prerequisites

- Python 3.11+
- A Slack workspace with a private channel
- A [Perplexity API key](https://www.perplexity.ai/settings/api)

---

## 1. Create your Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and click **Create New App → From scratch**.
2. Under **OAuth & Permissions → Scopes → Bot Token Scopes**, add:
   - `chat:write`
3. Click **Install to Workspace** and copy the **Bot OAuth Token** (starts with `xoxb-`).
4. In Slack, open your private **#finance** channel, click the channel name → **Integrations → Add an App**, and add your bot.
5. Right-click the channel → **View channel details** → scroll to the bottom to copy the **Channel ID** (starts with `C`).

---

## 2. Configure environment variables

Create a `.env` file in the project root and fill in:

| Variable | Description |
|---|---|
| `SLACK_BOT_TOKEN` | Bot OAuth Token (`xoxb-...`) |
| `SLACK_CHANNEL_ID` | Private channel ID (`C...`) |
| `PERPLEXITY_API_KEY` | Your Perplexity API key |
| `SCHEDULE_TYPE` | `weekly` or `daily` (Mon–Fri) |
| `SCHEDULE_DAY` | Day(s) of week for weekly mode (e.g. `monday` or `monday,friday`) |
| `SCHEDULE_HOUR` | Hour to send in 24h format (default `8`) |
| `SCHEDULE_MINUTE` | Minute to send (default `0`) |
| `TIMEZONE` | Timezone string (default `America/New_York`) |

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Test your setup

Before starting the scheduler, send a test message to verify everything is wired up correctly:

```bash
python bot.py --test
```

You should see the finance update appear in your Slack channel immediately.

---

## 5. Run the bot

```bash
python bot.py
```

The bot will log its schedule and wait for the next trigger. Press `Ctrl+C` to stop.

---

## Deploying to Railway or Render

Both platforms support always-on worker processes.

### Railway
1. Create a new project and connect your repo (or use the Railway CLI).
2. Set all environment variables in the Railway dashboard under **Variables**.
3. Railway will auto-detect the `Procfile` and run `python bot.py` as a worker.

### Render
1. Create a new **Background Worker** service.
2. Set the start command to `python bot.py`.
3. Add all environment variables under **Environment**.

---

## Changing the schedule

Edit `.env` (or the platform's environment variables) — no code changes needed:

| Goal | Settings |
|---|---|
| Every Monday at 8 AM ET | `SCHEDULE_TYPE=weekly`, `SCHEDULE_DAY=monday`, `SCHEDULE_HOUR=8` |
| Every Monday + Friday at 9 AM ET | `SCHEDULE_TYPE=weekly`, `SCHEDULE_DAY=monday,friday`, `SCHEDULE_HOUR=9`, `SCHEDULE_MINUTE=0` |
| Every weekday at 7:30 AM ET | `SCHEDULE_TYPE=daily`, `SCHEDULE_HOUR=7`, `SCHEDULE_MINUTE=30` |
| Every Friday at 4 PM ET | `SCHEDULE_TYPE=weekly`, `SCHEDULE_DAY=friday`, `SCHEDULE_HOUR=16` |

---

## Project structure

```
├── bot.py                # Entry point + scheduler
├── perplexity_client.py  # Fetches news via Perplexity API
├── slack_client.py       # Posts message to Slack
├── config.py             # Loads env vars
├── requirements.txt
├── Procfile              # For Railway / Render
└── .env          
```
