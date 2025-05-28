
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DAILY_CHANNEL_ID = "C08V10AVABS"
WEEKLY_CHANNEL_ID = "C08UE9DCM8U"

DAILY_MEMBERS = ["<@U0557BXF1B8>", "<@U06M0AMJF39>", "<@U027F58ADEV>"]  # Use Slack user IDs in this format
WEEKLY_MEMBERS_MEMBERS = ["<@U0557BXF1B8>", "<@U06M0AMJF39>", "<@U027F58ADEV>", "<@U08B8PM8PJS>"]  # Use Slack user IDs in this format

# State Files
DAILY_STATE_FILE = "state.json"
WEEKLY_STATE_FILE = "weekly_state.json"

def handle_rotation(client, members, state_file, channel_id, prefix):
    # Load current index
    try:
        with open(state_file) as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {"index": 0}

    index = state["index"]
    user = members[index]
    message = f"{prefix} {user}!"

    # Post message
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        print(f"Message sent to {channel_id}: {message}")
    except SlackApiError as e:
        print(f"Error sending message to {channel_id}: {e.response['error']}")

    # Save new index
    next_index = (index + 1) % len(members)
    with open(state_file, "w") as f:
        json.dump({"index": next_index}, f)

def main():
    if not SLACK_TOKEN:
        raise ValueError("Missing SLACK_BOT_TOKEN environment variable")

    client = WebClient(token=SLACK_TOKEN)

    # Daily rotation - always run
    handle_rotation(
        client,
        DAILY_MEMBERS,
        DAILY_STATE_FILE,
        DAILY_CHANNEL_ID,
        "🔔 It's your turn today,"
    )

    # Weekly rotation - only on Mondays
    if datetime.utcnow().weekday() == 0:  # Monday is 0
        handle_rotation(
            client,
            WEEKLY_MEMBERS,
            WEEKLY_STATE_FILE,
            WEEKLY_CHANNEL_ID,
            "📣 Weekly duty goes to"
        )

if __name__ == "__main__":
    main()
