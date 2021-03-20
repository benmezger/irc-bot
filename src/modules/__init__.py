#! /usr/bin/env python
from core.decorators import handle_exceptions

from core.plugins import Plugin, PLUGINS

__ALL__ = ("Command",)


class Command:
    async def run(cmd, con, event, *args, **kwargs):
        if cmd == "help":
            return Command.help(con, event)

        nick = event.source.nick

        words = [_ for _ in event.arguments[0].split(" ")[1:] if len(_) > 1]
        if not words:
            con.notice(nick, "Missing argument(s). Use <command> <args> or run help.")
            return

        if not PLUGINS.get(cmd, None):
            return Command.not_found(con, event)

        async for output in PLUGINS[cmd](tuple(words), *args, **kwargs):
            if isinstance(output, str):
                con.notice(nick, f"{cmd}: {output}")
            else:
                con.notice(nick, f"{cmd}")
                for line in output:
                    con.notice(nick, f"{line}")

    @staticmethod
    def not_found(con=None, event=None):
        con.notice(
           event.source.nick, "Don't know what to do with: " + event.arguments[0]
        )

    @staticmethod
    def help(con=None, event=None):
        msg = ["Available commands:"]
        for cmd in PLUGINS.keys():
            msg.append(f"\t{cmd}")

        nick = event.source.nick

        for line in msg:
            con.notice(nick, f"{line}")
