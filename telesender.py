import argparse
import os
import sys
from telethon import TelegramClient

# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Send messages or files to Telegram.")
parser.add_argument("--api-id", required=True, help="Telegram API ID")
parser.add_argument("--api-hash", required=True, help="Telegram API Hash")
parser.add_argument("--phone-number", required=True, help="Your Telegram phone number")
parser.add_argument("--chat-id", required=True, help="Target chat ID or username")
parser.add_argument("--directory", required=True, help="Directory to look for files")
args = parser.parse_args()

# Initialize the Telegram client
client = TelegramClient('session_name', args.api_id, args.api_hash)

async def send_message_or_file(line):
    # If the line is in "filename: caption" format, send file with caption
    if ':' in line:
        filename, caption = line.split(':', 1)
        filename = filename.strip()
        caption = caption.strip()

        file_path = os.path.join(args.directory, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            await client.send_file(args.chat_id, file_path, caption=caption)
        else:
            print(f"File not found: {file_path}")
    else:
        # Plain message, can contain markdown
        await client.send_message(args.chat_id, line)

async def main():
    # Connect to Telegram
    await client.start(phone=args.phone_number)
    
    # Reading from stdin, each line is either a message or file + caption
    for line in sys.stdin:
        line = line.strip()
        if line:
            await send_message_or_file(line)
    
    # Disconnect after sending all messages
    await client.disconnect()

if __name__ == "__main__":
    client.loop.run_until_complete(main())

