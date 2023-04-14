from environs import Env


def load_env():
    global settings

    env = Env()
    env.read_env()

    settings = {"token_api": env.str("TOKEN_API")}
