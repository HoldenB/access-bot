import os
from bot.client import CustomClient
from bot.commands import add_commands


def main(token: str, guild: str):
    client = CustomClient(token, guild)
    add_commands(client)
    client.run_custom_client()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    main(TOKEN, GUILD)
