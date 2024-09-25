#!/usr/bin/env python3

import sys
import argparse
import asyncio
from telethon import TelegramClient, errors
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

async def list_chats(client):
    chats = []
    last_date = None
    chunk_size = 200

    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    print("Available Chats:")
    for chat in chats:
        try:
            print(f"{chat.id}: {chat.title}")
        except AttributeError:
            pass  # Skip if chat has no title

async def send_messages(client, args):
    try:
        if args.chat_id:
            entity = await client.get_entity(int(args.chat_id))
        else:
            print("Error: --chat-id is required unless using --list-chats.", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        print("Invalid chat ID. Please provide a valid integer.", file=sys.stderr)
        sys.exit(1)
    except errors.RPCError as e:
        print(f"Error fetching chat entity: {e}", file=sys.stderr)
        sys.exit(1)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        if ':' not in line:
            print(f"Invalid message format: {line}", file=sys.stderr)
            continue

        msg_type, content = line.split(':', 1)
        msg_type = msg_type.lower()

        try:
            if msg_type == 'text':
                await client.send_message(entity, content)
            elif msg_type == 'markdown':
                await client.send_message(entity, content, parse_mode='markdown')
            elif msg_type == 'photo':
                parts = content.split(':', 1)
                file_path = parts[0]
                caption = parts[1] if len(parts) > 1 else ''
                await client.send_file(entity, file_path, caption=caption)
            elif msg_type == 'video':
                parts = content.split(':', 1)
                file_path = parts[0]
                caption = parts[1] if len(parts) > 1 else ''
                await client.send_file(entity, file_path, caption=caption, video_note=False)
            elif msg_type == 'file':
                parts = content.split(':', 1)
                file_path = parts[0]
                caption = parts[1] if len(parts) > 1 else ''
                await client.send_file(entity, file_path, caption=caption)
            else:
                print(f"Unknown message type: {msg_type}", file=sys.stderr)
        except Exception as e:
            print(f"Failed to send message: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Send messages to Telegram chats.')
    parser.add_argument('--api-id', required=True, help='Telegram API ID')
    parser.add_argument('--api-hash', required=True, help='Telegram API Hash')
    parser.add_argument('--chat-id', help='Target chat ID')
    parser.add_argument('--list-chats', action='store_true', help='List recent chats')
    args = parser.parse_args()

    client = TelegramClient('telegram_cli_session', int(args.api_id), args.api_hash)

    async def run():
        await client.start()
        if args.list_chats:
            await list_chats(client)
        else:
            await send_messages(client, args)
        await client.disconnect()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except errors.RPCError as e:
        print(f"Telegram API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()


