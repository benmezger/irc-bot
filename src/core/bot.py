#! /usr/bin/env python

import sys
import asyncio

from loguru import logger
from irc.client_aio import AioSimpleIRCClient
from irc.bot import SingleServerIRCBot
from irc.client_aio import AioReactor

from modules import Command


class SedsBot(SingleServerIRCBot):
    reactor_class = AioReactor

    def __init__(self, nickname, server, port=6667, allowed_nicks=[], command=Command):
        self.allowed_nicks = allowed_nicks
        self.command = command

        logger.info(f"Connecting to {server}:{port} with nickname {nickname}")
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)

    def connect(self, *args, **kwargs):
        self.c = self.reactor.loop.run_until_complete(
            self.connection.connect(*args, **kwargs)
        )
        print("Listening now. Please send an IRC message to verify operation")

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        logger.info(f"Got privmsg from {e.source.nick}")
        self.do_command(e)

    def do_command(self, e):
        cmd = e.arguments[0].split(" ")[0]

        nick = e.source.nick
        if nick not in self.allowed_nicks:
            logger.info(f"Nick '{nick}' not in ALLOWED_NICKS")
            return

        asyncio.get_running_loop().create_task(
            self.command.run(cmd, self.connection, e)
        )
