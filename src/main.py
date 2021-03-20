import os, sys

from loguru import logger

from core.plugins import import_modules, get_plugins

import_modules("modules")

from modules import Command
from core.bot import SedsBot
from core.env import SERVER, SERVER_PORT, ALLOWED_NICKS, BOT_NICKNAME, LOGFILE

if __name__ == "__main__":
    logger.add(
        sys.stdout, format="{time} {level} {message}", filter="ircbot", level="INFO"
    )
    logger.add(LOGFILE, rotation="500 MB")

    logger.info(f"Loaded plugins: {', '.join(tuple(get_plugins().keys()))}")

    bot = SedsBot(BOT_NICKNAME, SERVER, SERVER_PORT, ALLOWED_NICKS)
    bot.start()
