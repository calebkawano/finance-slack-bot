import logging
import ssl
import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID

logger = logging.getLogger(__name__)

_client = WebClient(
    token=SLACK_BOT_TOKEN,
    ssl=ssl.create_default_context(cafile=certifi.where()),
)


def send_finance_update(headline: str, summary: str, url: str) -> bool:
    """
    Post a finance news update to the configured Slack channel.
    Returns True on success, False on failure.
    """
    message = (
        f"Hi Experts, thought you might find this story interesting :newspaper:\n\n"
        f"*{headline}*\n"
        f"{summary}\n\n"
        f"Here is the link to the article: {url}"
    )

    try:
        response = _client.chat_postMessage(
            channel=SLACK_CHANNEL_ID,
            text=message,
            mrkdwn=True,
        )
        logger.info("Message posted to %s at ts=%s", SLACK_CHANNEL_ID, response["ts"])
        return True
    except SlackApiError as e:
        logger.error("Slack API error: %s", e.response["error"])
        return False
    except Exception as e:
        raise
