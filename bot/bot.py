import os
import discord
import util
from discord.ext import commands


class CustomClient(commands.Bot):
    def __init__(self, token: str, guild: str, command_prefix: str = '$'):
        super().__init__(command_prefix=command_prefix)
        self._token = token
        self._guild = guild

        # Remove the default help command
        self.remove_command('help')

        self.add_command(commands.Command(self.help))
        self.add_command(commands.Command(self.bobby))

    def run_custom_client(self):
        super().run(self._token)

    async def on_ready(self):
        print(f'{self.user} Has connected to Discord!')

    async def on_message(self, message: str):
        if message.author == self.user:
            return
        await self.process_commands(message)

    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(
            color=discord.Color.orange()
        )

        embed.set_author(name='Help')
        embed.add_field(
            name=f'{self.command_prefix}bobby',
            value='Display a random quote from Bobby.',
            inline=False
        )

        await ctx.send(author, embed=embed)

    async def bobby(self, ctx):
        await ctx.send(util.random_bobby_quote())


def main(token: str, guild: str):
    client = CustomClient(token, guild)
    client.run_custom_client()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    main(TOKEN, GUILD)
