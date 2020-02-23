import os
import discord
import bot.util as util
from discord.ext import commands


class CustomClient(commands.Bot):
    def __init__(self, token: str, guild: str, command_prefix: str = '$'):
        super().__init__(command_prefix=command_prefix)
        self._token = token
        self._guild = guild

        # Dictionary containing member: Cooldown timer info
        # This will allow us to restrict access to spamming certain commands
        # TODO We will need timers for each command that wants to call a timer
        # This dict will need to be nested one level futher for the command name
        self._member_timers = {}

        # Remove the default help command
        self.remove_command('help')

    def _on_timer_timeout(self, member: str) -> None:
        self._member_timers.pop(member)

    def add_access_member(self, member: str, cooldown: int) -> None:
        timer = util.CustomTimer(cooldown, lambda: self._on_timer_timeout(member))
        self._member_timers.update({member: timer})
        # Start the timer
        self._member_timers[member].start_timer()

    def member_on_cooldown(self, member: str) -> bool:
        return member in self._member_timers.keys()

    def member_cooldown_time(self, member: str) -> int:
        if not member in self._member_timers.keys():
            return 0

        return self._member_timers[member].time_remaining()

    def run_custom_client(self) -> None:
        super().run(self._token)

    async def on_ready(self):
        print(f'{self.user} Has connected to Discord!')

    async def on_message(self, message: str):
        if message.author == self.user:
            return

        await self.process_commands(message)
