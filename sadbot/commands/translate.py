"""Translate bot command"""

import re

from typing import Optional

import requests
from sadbot.commands.interface import CommandsInterface
from sadbot.message import Message
from sadbot.message_repository import MessageRepository


class TranslateBotCommand(CommandsInterface):
    """This is the translate bot command class"""

    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    @property
    def command_regex(self) -> str:
        """Returns the regex for matching translate commands"""
        return r"([.]|[!])[Tt]([Rr]|[Ll])(.*)"

    @property
    def parsemode(self) -> Optional[str]:
        """Returns the command parsemode"""
        return None

    def get_reply(self, message: Optional[Message] = None) -> Optional[str]:
        """Get the translation"""
        try:
            untranslated = self.message_repository.get_reply_message(message)
            print(untranslated)
            lang = message.text[4:]
            url = f"https://translate.google.com/m?q={untranslated.text}&tl={lang}"
            print(url)
            req = requests.get(url)
            ans = "Translation: " + re.findall(r"result-container\">(.*?)</", req.text)
            return ans[0]
        except (re.error, requests.ConnectionError):
            return None