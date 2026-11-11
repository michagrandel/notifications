# SPDX-FileCopyrightText: 2026 Micha Grandel
#
# SPDX-License-Identifier: Apache-2.0

import os

import dotenv

DOT_ENV_FILE = "./.env"
ENV_SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN"

_ = dotenv.load_dotenv(DOT_ENV_FILE)
SLACK_BOT_TOKEN = os.getenv(ENV_SLACK_BOT_TOKEN)
