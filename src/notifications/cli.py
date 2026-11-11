# SPDX-FileCopyrightText: 2026 Micha Grandel
#
# SPDX-License-Identifier: Apache-2.0

""" Send notifications to slack. """
import os
import sys

from notifications.slack import SlackConnection
from notifications.slack.error import SlackError

# Set the console to use UTF-8 encoding on Windows
if sys.platform == "win32":
    _ = os.system("chcp 65001 >nul")

import builtins

import typer
from rich.console import Console

# Set up the console for rich output
console: Console = Console(force_terminal=True, legacy_windows=False)
builtins.print = console.print

app = typer.Typer()

@app.command()
def slack(
    message: str,
    channel: str = typer.Option(  # pyright: ignore[reportCallInDefaultInitializer]
        "#general",
        "--channel", "-c",
        help="The channel to send the message to."
    ),
    verbose: int = typer.Option(  # pyright: ignore[reportCallInDefaultInitializer]
        0,
        "--verbose", "-v",
        count=True,
        show_default=False,
        help="Enable verbose output"
    )
) -> None:
    """
    Send a notification to slack.

    Send a message to a specified Slack channel. To send a messsage to a private channel, you must invite the bot to the channel first.
    Set the channel-parameter to a user id to send a direct message to a user. The bot must be a member of the channel or
    have permission to send direct messages to the user.

    Args:
        message (str): The message to send.
        channel (str): The channel to send the message to, default is "#general".
        verbose (int): The verbosity level, default is 0. Increase the level by adding more -v flags (e.g., -vv for level 2).
    """
    if not message:
        print("[red]Error: Message is empty.[/red]")
        raise typer.Exit(code=1)
    if verbose > 2:
        print(f"[cyan][ SLACK ] {channel} >> {message}[/cyan]")

    connection = SlackConnection(verbose=verbose)
    try:
        success, response = connection.post_message(channel, message)
    except SlackError as e:
        print(str(e))
        return

    if not success:
        print(f"[red][  200  ] Error: Failed to send message to slack channel '{channel}': {response}[/red]")

    if success and verbose >= 1:
        channel = f"#{channel}" if not channel.startswith("#") else channel
        prefix = "[green][  200  ][/green] " if verbose > 1 else ""
        print(f"{prefix}[bright_black]{channel} >>[/bright_black] {message}")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
