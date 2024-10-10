import os


def getEnv(key):
    envval = os.getenv(key)
    if envval is None:
        return "None"
    return envval


config = {"TOKEN": (getEnv("BOT_TOKEN"))}
