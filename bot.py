import os
import discord


class CustomClient(discord.Client):
    def __init__(self, token: str, guild: str):
        super().__init__()
        self._token = token
        self._guild = guild

    def run_custom_client(self):
        super().run(self._token)

    async def on_ready(self):
        print(f'{self.user} Has connected to Discord!')


def main(token: str, guild: str):
    client = CustomClient(token, guild)
    client.run_custom_client()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    main(TOKEN, GUILD)
