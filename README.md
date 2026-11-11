# Slack Notifications

A Python package and command-line tool for sending notifications to Slack.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Slack bot token with permission to post messages

## Setup

Clone the repository, then install the project and its dependencies:

```shell
uv sync
```

Set the bot token in a `.env` file in the project directory:

```dotenv
SLACK_BOT_TOKEN=xoxb-your-token
```

Keep the token secret and do not commit the `.env` file.

## Usage

Send a message to the default `#general` channel:

```shell
uv run notify "Build completed successfully."
```

Choose another channel with `--channel` (or `-c`):

```shell
uv run notify "Deployment finished." --channel "#releases"
```

The bot must be a member of the channel. To send a direct message, use the
recipient's Slack user ID as the channel value.

Increase verbosity with `-v` (up to `-vvv`):

```shell
uv run notify "Build completed successfully." -v
```

## For developers

Import `SlackConnection` in another Python project and call `post_message`.
Set `SLACK_BOT_TOKEN` in the environment before importing the library:

```python
from notifications.slack import SlackConnection

connection = SlackConnection()
success, response = connection.post_message(
    "#general",
    "A notification from my Python app.",
)

if not success:
    raise RuntimeError(f"Slack rejected the message: {response}")
```
