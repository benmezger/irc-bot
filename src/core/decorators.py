from loguru import logger


def handle_exceptions(f):
    async def wrapper(*args, **kw):
        try:
            logger.info(f"Running {f} with {args} {kw}")
            return await f(*args, **kw)
        except Exception as e:
            logger.exception(f"Got exception from {f} {e}")

            con = kw.get("con")
            event = kw.get("event")
            nick = event.source.nick

            con.notice(nick, f"Something went terribly wrong: {e}")

    return wrapper
