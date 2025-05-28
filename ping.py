
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "C08V10AVABS"  # Replace with your actual Slack channel ID
MEMBERS = ["<@U0557BXF1B8>", "<@U06M0AMJF39>", "<@U027F58ADEV>"]  # Use Slack user IDs in this format

STATE_FILE = "state.json"

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"index": 0}

def save_state(index):
    with open(STATE_FILE, "w") as f:
        json.dump({"index": index}, f)

def post_message(client, user):
    message = f"🔔 It's your turn today, {user}!"
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=message)
        print(f"Message sent: {message}")
    except SlackApiError as e:
        print(f"Failed to send message: {e.response['error']}")

def main():
    if not SLACK_TOKEN:
        raise ValueError("Missing SLACK_BOT_TOKEN environment variable")

    client = WebClient(token=SLACK_TOKEN)
    state = load_state()
    index = state["index"]
    user = MEMBERS[index]

    post_message(client, user)

    next_index = (index + 1) % len(MEMBERS)
    save_state(next_index)

if __name__ == "__main__":
    main()
