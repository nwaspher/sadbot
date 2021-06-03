# sadbot
A simple telegram bot.  
Which main feature is its sed command, the famous UNIX command.

## Dependencies
The bot has the following dependencies:
- `requests`

Which can be installed with:
```
pip3 install -r requirements.txt \
             -r dev-requirements.txt # Add this when developing the bot
```

## Installation
You have to place your bot token either in the environment variables or in the
config files, by manually editing them:
```
nano sadbot/config.py
nano Dockerfile # If you are using Docker/Podman
```
In the `sadbot/config.py` file you can also find the settings for configurable
bot commands (like `cringe`, `roulette` etc.)


## Usage
### Manual
Here's how you run the bot manually:  
```
nohup PYTHONPATH=. python3 -m sadbot & disown
```
### Systemd Service
Alternatively, you can create a new systemd service, which handles the bot
restart in a way more neat way, with these commands:
```
sed -i 's/userplaceholder/BOTUSER' sadbot.service
sed -i 's/pathplaceholder/BOTPATH' sadbot.service
sudo cp sadbot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo service sadbot start
```
And to check the bot status you can simply type:
```
sudo service sadbot status
```
or, for reading the full log:
```
sudo journalctl -u sadbot.service
```
### Docker/Podman
If you like docker or podman, you can easily build the container using the
Dockerfile:
```
sudo docker build -m sadbot .
```
Then you can easily start the bot with:
```
sudo docker run -it sadbot
```

## Todo list
- [ ] Add media support for outgoing messages
- [X] Fix the roulette code
- [ ] Eval command
- [ ] Weather command
- [ ] Status command
- [ ] Seen command
- [ ] Tay command
- [ ] User ratelimit
- [ ] Group ratelimit
- [ ] Antiflood, samewords count and newlines count
- [X] FBI watchlist
- [ ] Captcha command
- [X] Translate command
- [ ] Outgoing messages queue
- [ ] Asynchronous processing
- [ ] Welcome messages
- [ ] Big chan url pictures
- [ ] Beaver command
- [ ] Reminder tag/bookmark command

## Contributing
Pull requests are welcome.  
It's recommended to use `pylint` and `black` to cleanup and review the
code before submitting.

### Writing a new bot command
If you want to add a new command you just have to write a new module file.  
Here is a sample bot command, `sample_command.py`, it's pretty self explanatory:
```
"""Sample bot command"""
# these imports are required in every module
from typing import Optional

from sadbot.commands import CommandsInterface
from sadbot.message import Message


class SampleCommandBotCommand(CommandsInterface): # the class name must be the
pascal case of the module filename + "BotCommand"
    """This is the sample command bot command class"""

    @property
    def command_regex(self) -> str:
        regex = r"" # here is the regex that triggers this bot command
        return regex

    @property
    def parsemode(self) -> Optional[str]:
        parsemode = None # here is the bot reply parsemode: it can be None,
HTML, Markdown (deprecated) or MarkdownV2
        return parsemode

    def get_reply(self, message: Optional[Message] = None) -> Optional[str]:
        reply = "" # here is the reply that will be sent by the bot
        return reply
```
Here is the same example with some dependencies and more code manipulation:
```
"""Sample bot command"""
# here are some unrequired imports
import re
import sqlite3

# these imports are required in every module
from typing import Optional

from sadbot.commands import CommandsInterface
from sadbot.message import Message


class SampleCommandBotCommand(CommandsInterface): # the class name must be the
pascal case of the module filename + "BotCommand"
    """This is the sample command bot command class"""

    # the constructor is not required, but if the bot command need some
dependencies, they will be automatically injected through it
    def __init__(self, message_repository: MessageRepository, con: sqlite3.Connection):
        self.message_repository = message_repository
        self.con = con

    @property
    def command_regex(self) -> str:
        regex = r"" # here is the regex that triggers this bot command
        return regex

    @property
    def parsemode(self) -> Optional[str]:
        parsemode = None # here is the bot reply parsemode: it can be None,
HTML, Markdown (deprecated) or MarkdownV2
        return parsemode

    def get_reply(self, message: Optional[Message] = None) -> Optional[str]:
        reply = "" # here is the reply that will be sent by the bot
        re.sub(r"(\w{3})", r"\1w", message.text) # this is an example on how you
can process the message that triggered the command to get a custom reply
        return reply
```
