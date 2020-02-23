import os
import discord
import bot.util as util
from discord.ext import commands


class CustomClient(commands.Bot):
    def __init__(self, token: str, guild: str, command_prefix: str = '$'):
        super().__init__(command_prefix=command_prefix)
        self._token = token
        self._guild = guild

        # Remove the default help command
        self.remove_command('help')

    def run_custom_client(self):
        super().run(self._token)

    async def on_ready(self):
        print(f'{self.user} Has connected to Discord!')

    async def on_message(self, message: str):
        if message.author == self.user:
            return
        await self.process_commands(message)
