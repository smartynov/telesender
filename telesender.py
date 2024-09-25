#!/usr/bin/env python3

import sys
import argparse
import asyncio
import shlex
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

    lines = sys.stdin.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue  # Skip empty lines

        msg_type = 'text'
        content = ''
        file_path = None

        # Check for message type and parameters
        if ':' in line:
            parts = line.split(':', 2)
            if len(parts) == 2:
                msg_type, remaining = parts
                msg_type = msg_type.strip().lower()
                remaining = remaining.strip()
                if msg_type in ['photo', 'video', 'file']:
                    file_path = remaining
                else:
                    # The remaining is part of the content
                    content = remaining
            elif len(parts) == 3:
                msg_type, file_path, remaining = parts
                msg_type = msg_type.strip().lower()
                file_path = file_path.strip()
                remaining = remaining.strip()
                content = remaining
            else:
                content = line
        else:
            content = line

        # Handle multiline content enclosed in double quotes
        if content.startswith('"'):
            content = content[1:]  # Remove the opening quote
            multiline_content = [content]
            i += 1
            while i < len(lines):
                next_line = lines[i].rstrip('\n')
                if next_line.endswith('"'):
                    multiline_content.append(next_line[:-1])  # Remove the closing quote
                    break
                else:
                    multiline_content.append(next_line)
                i += 1
            content = '\n'.join(multiline_content)
        else:
            # Single-line content, proceed to next line
            i += 1

        # Process the message
        try:
            if msg_type == 'text':
                await client.send_message(entity, content)
            elif msg_type == 'markdown':
                await client.send_message(entity, content, parse_mode='markdown')
            elif msg_type == 'photo':
                caption = content if content else None
                await client.send_file(entity, file_path, caption=caption)
            elif msg_type == 'video':
                caption = content if content else None
                await client.send_file(entity, file_path, caption=caption, supports_streaming=True)
            elif msg_type == 'file':
                caption = content if content else None
                await client.send_file(entity, file_path, caption=caption)
            else:
                print(f"Unknown message type: {msg_type}", file=sys.stderr)
        except Exception as e:
            print(f"Failed to send message: {e}", file=sys.stderr)

    await client.disconnect()

def main():
    parser = argparse.ArgumentParser(description='Send messages to Telegram chats.')
    parser.add_argument('--api-id', required=True, help='Telegram API ID')
    parser.add_argument('--api-hash', required=True, help='Telegram API Hash')
    parser.add_argument('--chat-id', help='Target chat ID')
    parser.add_argument('--list-chats', action='store_true', help='List recent chats')
    args = parser.parse_args()

    async def run():
        # Use the client as an asynchronous context manager
        async with TelegramClient('telesender', int(args.api_id), args.api_hash) as client:
            if args.list_chats:
                await list_chats(client)
            else:
                await send_messages(client, args)

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

