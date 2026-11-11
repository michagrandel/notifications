# SPDX-FileCopyrightText: 2026 Micha Grandel
#
# SPDX-License-Identifier: Apache-2.0
from collections.abc import Callable


class SlackError(Exception):
    """Raised when there is a connection error with the Slack API."""

    def __init__(self, message: str = "Error: Unknown error."):
        """Initialize the SlackConnectionError with a message."""
        self.message: str = message
        super().__init__(message)

class SlackTokenNotSetError(SlackError):
    """Raised when the Slack bot token is not set."""

    def __init__(self):
        """Initialize the SlackTokenNotSetError with a message."""
        super().__init__("[red]Error: Slack bot token is not set. Please set the SLACK_BOT_TOKEN environment variable.[/red]")


class SlackResponseError(SlackError):
    """Raised when the Slack API returns an error response."""

    def __init__(self, status_code: int, message: str):
        """Initialize the SlackResponseError with the status code and message."""
        self.status_code = status_code
        self.message = message
        super().__init__(message)

# -----------------------------------------

class SlackChannelError(SlackResponseError):
    """Raised when there is an error with the Slack channel."""

    def __init__(self, message: str):
        """Initialize the SlackChannelError with the status code and message."""
        super().__init__(200, message)

class SlackNotInChannelError(SlackChannelError):
    """Raised when the bot is not in the channel."""

    def __init__(self):
        """Initialize the NotInChannelError with a message."""
        super().__init__("[red][  200  ] Error: The bot is not in the channel. Please invite the bot to the channel.[/red]")

class SlackChannelNotFoundError(SlackChannelError):
    """Raised when the specified channel is not found."""

    def __init__(self):
        """Initialize the ChannelNotFoundError with a message."""
        super().__init__("[red][  200  ] Error: The specified channel was not found. Please check the channel name.[/red]")

class SlackChannelIsArchivedError(SlackChannelError):
    """Raised when the specified channel is archived."""

    def __init__(self):
        """Initialize the ChannelIsArchivedError with a message."""
        super().__init__("[red][  200  ] Error: The specified channel is archived. Please unarchive the channel or use a different channel.[/red]")

# -----------------------------------------

class SlackDeprecatedError(SlackResponseError):
    """Raised when the Slack API endpoint or method is deprecated."""

    def __init__(self, message: str):
        """Initialize the SlackDeprecatedError with a message."""
        super().__init__(200, f"[red][  200  ] Error: {message}[/red]")

class SlackEnpointIsDeprecatedError(SlackDeprecatedError):
    """Raised when the Slack API endpoint is deprecated."""

    def __init__(self):
        """Initialize the DeprecatedEndpointError with a message."""
        super().__init__("[red][  200  ] Error: The Slack API endpoint is deprecated. Please check the Slack API documentation for the correct endpoint.[/red]")

class SlackMethodIsDeprecatedError(SlackDeprecatedError):
    """Raised when the Slack API endpoint is deprecated."""

    def __init__(self):
        """Initialize the DeprecatedMethodError with a message."""
        super().__init__("[red][  200  ] Error: The Slack API method is deprecated. Please check the Slack API documentation for the correct method.[/red]")

# -----------------------------------------

class SlackServerError(SlackResponseError):
    """Raised when the Slack API returns a server error."""

    def __init__(self):
        """Initialize the ServerError with a message."""
        super().__init__(200, "[red][  200  ] Error: The Slack API returned a server error. Please try again later.[/red]")

# -----------------------------------------

class SlackRequestIsInvalidError(SlackResponseError):
    """Raised when the Slack API returns an invalid request error."""

    def __init__(self, message: str):
        """Initialize the InvalidRequestError with a message."""
        self.message = message
        super().__init__(200, f"[red][  200  ] Error: Invalid request: {message}[/red]")

class SlackArgumentIsInvalidError(SlackRequestIsInvalidError):
    """Raised when an invalid argument is passed to the Slack API."""

    def __init__(self, method: str):
        """Initialize the InvalidArgumentError with a message."""
        super().__init__(f"[red][  200  ] Error: Method was called with invalid arguments: {method}[/red]")

class SlackAuthIsInvalidError(SlackRequestIsInvalidError):
    """Raised when the Slack API returns an invalid authentication error."""

    def __init__(self):
        """Initialize the InvalidAuthError with a message."""
        super().__init__("[red][  200  ] Error: Invalid authentication token. Please check your Slack bot token.[/red]")

class SlackBlocksIsInvalidError(SlackRequestIsInvalidError):
    """Raised when the Slack API returns an invalid blocks error."""

    def __init__(self):
        """Initialize the InvalidBlocksError with a message."""
        super().__init__("[red][  200  ] Error: Invalid blocks format or message blocks are too long. Please check your message blocks.[/red]")

class SlackContentTypeIsMissingError(SlackRequestIsInvalidError):
    """Raised when the Slack API request is missing a content type."""

    def __init__(self):
        """Initialize the RequestMissingContentTypeError with a message."""
        super().__init__("[red][  200  ] Error: The request is missing a content type. Please set the content type to application/json or application/x-www-form-urlencoded.[/red]")

class SlackScopeIsMissingPermissionError(SlackRequestIsInvalidError):
    """Raised when the Slack API request is missing a permission scope."""

    def __init__(self):
        """Initialize the ScopeMissingPermissionError with a message."""
        super().__init__("[red][  200  ] Error: The request is missing a permission scope. Please check your Slack app's OAuth scopes.[/red]")

# -----------------------------------------

class SlackRateLimitError(SlackResponseError):
    """Raised when the Slack API returns a rate limit error."""

    def __init__(self, message: str = ""):
        """Initialize the RateLimitError with a message."""
        super().__init__(200, "[red][  200  ] Error: The request is violating a rate limit. Please wait before sending more messages.[/red]")

class SlackTooManyMessagesError(SlackRateLimitError):
    """Raised when too many messages are sent to the Slack API."""

    def __init__(self):
        """Initialize the TooManyMessagesError with a message."""
        super().__init__("[red][  200  ] Error: The app or members on this team are sending too many messages. Please wait before sending more messages.[/red]")


# -----------------------------------------

class SlackPermissionError(SlackResponseError):
    """Raised when the Slack API request is missing a permission scope."""

    def __init__(self, message: str):
        """Initialize the SlackPermissionError with a message."""
        super().__init__(200, f"[red][  200  ] Error: Missing permissions: {message}[/red]")

class SlackAdminsDisabledSendingMessagesError(SlackPermissionError):
    """Raised when admins have disabled sending messages."""

    def __init__(self):
        """Initialize the AdminsDisabledSendingMessagesError with a message."""
        super().__init__("[red][  200  ] Error: Admins have disabled sending messages to the specified channel. Please contact your Slack workspace admin.[/red]")

class SlackTokenMissingPermissionError(SlackPermissionError):
    """Raised when the Slack API request is missing a permission scope."""

    def __init__(self):
        """Initialize the TokenMissingPermissionError with a message."""
        super().__init__("[red][  200  ] Error: The token is missing permissions to complete your request. Make sure the app is a member of the conversation it's attempting to post a message to.[/red]")

class SlackTokenExpiredError(SlackPermissionError):
    """Raised when the Slack API request is missing a permission scope."""

    def __init__(self):
        """Initialize the SlackTokenExpiredError with a message."""
        super().__init__("[red][  200  ] Error: The token has expired. Please refresh your Slack bot token.[/red]")

class SlackTokenRevokedError(SlackPermissionError):
    """Raised when the Slack API request is missing a permission scope."""

    def __init__(self):
        """Initialize the SlackTokenRevokedError with a message."""
        super().__init__("[red][  200  ] Error: The token has been revoked. Please check your Slack bot token.[/red]")

def get_error_factory(error_code: str, method: str = "") -> Callable[[], Exception] | None:
    """Get the error factory for the given error code.

    Args:
        error_code (str): The error code returned by the Slack API.
        method (str): The Slack API method that was called.

    Returns:
        Callable[[], Exception] | None: The error factory for the given error code, or None if the error code is not recognized.
    """
    error_factories: dict[str, Callable[[], Exception]] = {
        "not_in_channel": SlackNotInChannelError,
        "channel_not_found": SlackChannelNotFoundError,
        "deprecated_endpoint": SlackEnpointIsDeprecatedError,
        "method_deprecated": SlackMethodIsDeprecatedError,
        "ekm_access_denied": SlackAdminsDisabledSendingMessagesError,
        "fatal_error": SlackServerError,
        "internal_error": SlackServerError,
        "service_unavailable": SlackServerError,
        "invalid_arguments": lambda: SlackArgumentIsInvalidError(method),
        "invalid_array_arg": lambda: SlackArgumentIsInvalidError(method),
        "invalid_auth": SlackAuthIsInvalidError,
        "invalid_blocks": SlackBlocksIsInvalidError,
        "invalid_block_format": SlackBlocksIsInvalidError,
        "msg_blocks_too_long": SlackBlocksIsInvalidError,
        "is_archived": SlackChannelIsArchivedError,
        "message_limit_exceeded": SlackTooManyMessagesError,
        "rate_limited": SlackTooManyMessagesError,
        "ratelimited": SlackTooManyMessagesError,
        "missing_post_type": SlackContentTypeIsMissingError,
        "missing_scope": SlackScopeIsMissingPermissionError,
        "no_permission": SlackTokenMissingPermissionError,
        "token_expired": SlackTokenExpiredError,
        "token_revoked": SlackTokenRevokedError,
    }
    if error_code in error_factories:
        return error_factories[error_code]
    return None
