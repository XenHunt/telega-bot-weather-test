import os


def getEnv(key):
    envval = os.getenv(key)
    if envval is None:
        return "None"
    return envval


config = {
    "BOT_TOKEN": getEnv("BOT_TOKEN"),
    "WEATHER_TOKEN": getEnv("WEATHER_TOKEN"),
    "DATA_BASE": {
        "USER": getEnv("DATABASE_USER"),
        "PORT": getEnv("DATABASE_PORT"),
        "PASSWORD": getEnv("DATABASE_PASSWORD"),
    },
}
