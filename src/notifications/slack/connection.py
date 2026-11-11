# SPDX-FileCopyrightText: 2026 Micha Grandel
#
# SPDX-License-Identifier: Apache-2.0
"""Handle the connection to the Slack API."""
import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

import requests

from . import SLACK_BOT_TOKEN  # pyright: ignore[reportPrivateLocalImportUsage]
from .error import (
    SlackError,
    SlackResponseError,
    SlackTokenNotSetError,
    get_error_factory,
)

api_response = tuple[bool, int, str | dict[str, str]]
slack_response = tuple[bool, str | dict[str, str]]

class SlackContentType(StrEnum):
    """Enum for Slack content types."""
    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"

@dataclass
class SlackMessage:
    """A class to represent a Slack message."""
    channel: str
    message: str
    markdown: bool = True
    ts: str | None = None
    _timestamp: datetime | None = None
    icon_url: str | None = None
    icon_emoji: str | None = None
    metadata: dict[str, str] | None = None

    @staticmethod
    def by_ts(ts: str):
        """
        Get a SlackMessage instance from a timestamp.

        Args:
            ts (str): The timestamp of the message.
        """

    @staticmethod
    def by_date(date: datetime):
        """
        Get a SlackMessage instance from a date.

        Args:
            date (datetime): The date of the message.
        """

    @staticmethod
    def by_timestamp(timestamp: int):
        """
        Get a SlackMessage instance from a timestamp.

        Args:
            timestamp (int): The timestamp of the message.
        """



    @property
    def timestamp(self) -> datetime | None:
        """
        Get the timestamp of the message.

        Returns:
            datetime | None: The timestamp of the message, or None if not set.
        """
        if self._timestamp is None and self.ts is not None:
            try:
                self._timestamp = datetime.fromtimestamp(float(self.ts))
            except ValueError:
                raise ValueError(f"Invalid timestamp: {self.ts}")
        return self._timestamp

class SlackConnection:
    """A class to handle the connection to the Slack API."""
    token: str | None = SLACK_BOT_TOKEN
    url: str = "https://slack.com/api/"

    def __init__(self, verbose: int = 0):
        self._verbose: int = verbose

    def post_message(
        self,
        channel: str,
        message: str,
        *args: str,
        content_type: SlackContentType = SlackContentType.JSON,
        **kwargs: str | bool | dict[str, str],
    ) -> slack_response:
        """
        Send a message to Slack.

        Args:
            payload (dict[str, str]): The payload to send to Slack.
            content_type (SlackContentType): The content type of the payload. Defaults to SlackContentType.JSON.
            markdown (bool): Whether to enable markdown formatting. Defaults to True.
        """
        method = "chat.postMessage"

        payloads = self._generate_payloads(channel, message, *args, **kwargs)

        success = False
        response: str | dict[str, str] = "Unknown error"

        for payload in payloads:
            success, _, response = self.send(method, payload, content_type, **kwargs)

        if success:
            return True, "ok"

        error_code: str | None = response.get("error") if isinstance(response, dict) else None

        if error_code is not None:
            exception_factory: Callable[[], Exception] | None = get_error_factory(error_code, method)
            if exception_factory is not None:
                raise exception_factory()

        return False, response.get("error", "Unknown error") if isinstance(response, dict) else response

    def _generate_payloads(self, channel: str, message: str, *args: str, **kwargs: str|bool|dict[str, str]) -> tuple[dict[str, str], ...]:
        """
        Generate the payload for the Slack API request.

        Args:
            channel (str): The channel to send the message to.
            message (str): The message to send.
            kwargs: Additional keyword arguments.
        """
        messages = [message]
        messages.extend(args)

        payload_lines: list[str] = []
        payloads: list[dict[str, str]] = []

        for msg in messages:
            msg = msg.replace("\\n", "\n")
            lines:list[str] = msg.splitlines()
            payload_lines.extend([l.strip() for l in lines if l.strip()])

        for line in payload_lines:
            payload: dict[str, str] = {
                "channel": channel
            }
            text_field = "markdown_text" if kwargs.get("markdown", True) else "text"
            payload[text_field] = line

            if kwargs.get("thread_ts", False):
                payload["thread_ts"] = str(kwargs["thread_ts"])

            if kwargs.get("icon_url", False):
                payload["icon_url"] = str(kwargs["icon_url"])
            elif kwargs.get("icon_emoji", False):
                payload["icon_emoji"] = str(kwargs["icon_emoji"])

            if kwargs.get("metadata", False):
                payload["metadata"] = json.dumps(kwargs["metadata"])

            payloads.append(payload)

        return (*payloads,)
        
    def send(self, method:str, payload: dict[str, str], content_type: SlackContentType = SlackContentType.JSON, **kwargs: str|bool|dict[str, str]) -> api_response:
        """
        Send a message to Slack.

        Args:
            method (str): The Slack API method to call.
            payload (dict[str, str]): The payload to send to Slack.
            content_type (SlackContentType): The content type of the payload. Defaults to SlackContentType.JSON.
        """
        if not self.token:
            raise SlackTokenNotSetError()

        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": f"{content_type.value}; charset=utf-8",
        }

        url = self.url + method

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise SlackResponseError(response.status_code, f"[red][  {response.status_code}  ][/red] {response.text}")

        return self._get_result(response)

    @staticmethod
    def _get_result(response: requests.Response) -> api_response:
        """
        Get the result from the Slack API response.

        Args:
            response (requests.Response): The response from the Slack API.
        """
        try:
            result = response.json()  # pyright: ignore[reportAny]
            s: bool | str = result.get("ok", False)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportUnknownVariableType]
            status: bool = s if isinstance(s, bool) else (s.lower() == "true")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportRedeclaration, reportIndexIssue]

        except ValueError:
            result: str = response.text
            status: bool = False
            if result.startswith("<!doctype html>"):
                result = """\n[red][  200  ][/red] HTML response received. Please check the Slack API endpoint.
                        [red][  200  ][/red] Is your app authorized in your workspace?"""
                result = "\n".join(s.strip() for s in result.splitlines())
            raise SlackResponseError(response.status_code, result)

        return status, response.status_code, result  # pyright: ignore[reportUnknownVariableType]
