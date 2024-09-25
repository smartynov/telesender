# Telesender

**Telesender** is a command-line tool that allows you to send messages, photos, videos, and files to Telegram chats directly from your terminal. It operates in the Unix philosophy, accepting command-line arguments for account configuration and reading messages from `stdin`.

## Features

- Send plain text and Markdown-formatted messages.
- Send photos, videos, and files with optional captions.
- Support for multiline messages and captions.
- Works with your personal Telegram account via the Telegram API.
- List available chats for easy selection.
- Supports individual and group chats.

## Installation

### Prerequisites

- **Python 3.6** or later.
- **Telethon** library.

### Install Telethon

```bash
pip install telethon
```

### Download Telesender

Clone the repository:

```bash
git clone https://github.com/your_github_username/telesender.git
cd telesender
```

Make the script executable:

```bash
chmod +x telesender
```

## Usage

### First-Time Authentication

1. **Obtain Telegram API Credentials**:

   - Go to [my.telegram.org/apps](https://my.telegram.org/apps).
   - Log in with your Telegram account.
   - Create a new application to get your **API ID** and **API Hash**.

2. **Authenticate with Telesender**:

   - The first time you run Telesender, it will prompt for your **phone number** and send you a code via Telegram to authenticate.

### Command-Line Options

- `--api-id`: Your Telegram **API ID** (required).
- `--api-hash`: Your Telegram **API Hash** (required).
- `--chat-id`: The **ID** of the target chat (required unless using `--list-chats`).
- `--list-chats`: List recent chats and their IDs.

### Listing Available Chats

To list your recent chats and obtain their IDs:

```bash
./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --list-chats
```

### Message Format

- **Single-Line Messages**: Write your message on a single line.
- **Multiline Messages**: Enclose your message or caption within double quotes (`\"`).
- **Message Types**:
  - **text** (default)
  - **markdown**
  - **photo**
  - **video**
  - **file**

**Syntax**:

```
[message_type]:[file_path]:[content]
```

- **message_type**: The type of message (optional for text messages).
- **file_path**: Path to the file (required for `photo`, `video`, `file`).
- **content**: The message text or caption. Use double quotes for multiline content.

**Examples**:

- **Plain Text Message**:

  ```
  Hello, this is a single-line message.
  ```

- **Multiline Text Message**:

  ```
  \"This is
  a multiline
  text message.\"
  ```

- **Markdown Message**:

  ```
  markdown:\"This is **bold** and _italic_ text.\"
  ```

- **Photo with Caption**:

  ```
  photo:/path/to/photo.jpg:\"This is a
  multiline caption
  for the photo.\"
  ```

- **Video with Caption**:

  ```
  video:/path/to/video.mp4:\"Check out this
  awesome video!\"
  ```

### Sending Messages

#### From a File

Create a `messages.txt` file:

```
Hello, this is a single-line message.
\"This is
a multiline message.\"
markdown:\"This is **bold** and _italic_ text.\"
photo:/path/to/photo.jpg:\"This is a
multiline caption
for the photo.\"
```

Send messages using:

```bash
./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id TARGET_CHAT_ID < messages.txt
```

#### Using a Here Document

```bash
cat <<EOF | ./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id TARGET_CHAT_ID
Hello, this is a single-line message.
\"This is
a multiline message.\"
markdown:\"This is **bold** and _italic_ text.\"
photo:/path/to/photo.jpg:\"This is a
multiline caption
for the photo.\"
EOF
```

### Examples

**Sending a Single-Line Text Message**:

```bash
echo \"Hello, World!\" | ./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id CHAT_ID
```

**Sending a Multiline Text Message**:

```bash
echo '\"This is a
multiline message.\"' | ./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id CHAT_ID
```

**Sending a Markdown Message**:

```bash
echo 'markdown:\"This is **bold** and _italic_.\"' | ./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id CHAT_ID
```

**Sending a Photo with Caption**:

```bash
echo 'photo:/path/to/photo.jpg:\"This is a
multiline caption.\"' | ./telesender --api-id YOUR_API_ID --api-hash YOUR_API_HASH --chat-id CHAT_ID
```

### Error Handling

- **Invalid Input**: The script will output error messages to `stderr` if it encounters invalid message formats or missing parameters.
- **File Not Found**: If a specified file does not exist, an error will be printed to `stderr`.
- **Telegram API Errors**: Any errors from the Telegram API will be caught and displayed.

### Security Considerations

- **API Credentials**: Keep your `api_id` and `api_hash` confidential.
- **Session File**: The script creates a `telesender.session` file containing your session data. Protect this file to prevent unauthorized access.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for enhancements and bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Built using the [Telethon](https://github.com/LonamiWebs/Telethon) library.
- Inspired by the need for simple, Unix-style command-line tools for Telegram.

