from environs import Env

env = Env()

DEBUG = env.bool("DEBUG", default=False)

if DEBUG:
    # read .env file
    env.read_env()

SERVER = env.str("SERVER", default="irc.freenode.net")
SERVER_PORT = env.int("SERVER_PORT", default=6667)

BOT_NICKNAME = env.str("BOT_NICKNAME", default="mebot")
ALLOWED_NICKS = env.list("ALLOWED_NICKS")

LOGFILE = env.str("LOGFILE", default=f"{BOT_NICKNAME}.log")
