import discord
import bot.util as util
from bot.client import CustomClient


class Command:
    def __init__(self, description: str):
        self.description = description
        self.cmd = None


class BobbyCommand(Command):
    def __init__(self, client: CustomClient):
        super().__init__('Display a random quote from Bobby.')

        @client.command()
        async def bobby(ctx):
            await ctx.send(util.random_bobby_quote())

        self.cmd = bobby


class AccessCommand(Command):
    def __init__(self, client: CustomClient):
        super().__init__(
            'Privides the user with a one time access token to view/download files.')

        @client.command()
        async def access(ctx):
            token = "someRandomTokenString"
            await ctx.message.author.send(f'Here is your access token: {token}')

        self.cmd = access


def add_commands(client: CustomClient) -> None:

    custom_commands = [
        BobbyCommand(client),
        AccessCommand(client)
    ]

    @client.command()
    async def help(ctx):
        author = ctx.message.author
        embed = discord.Embed(
            color=discord.Color.orange()
        )

        embed.set_author(name='Help')

        for command in custom_commands:
            assert(command.cmd.name)
            embed.add_field(
                name=f'{client.command_prefix}{command.cmd.name}',
                value=command.description,
                inline=False
            )

        await ctx.send(author, embed=embed)
