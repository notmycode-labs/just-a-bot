import os
import requests

def get_message(channel_id, message_id):
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set")

    headers = {'Authorization': f'Bot {token}'}
    response = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get message: {response.status_code} - {response.text}")
        return None
