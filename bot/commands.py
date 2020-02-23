import discord
import bot.util as util
from bot.client import CustomClient


def add_commands(client: CustomClient) -> None:

    @client.command()
    async def help(ctx):
        author = ctx.message.author
        embed = discord.Embed(
            color=discord.Color.orange()
        )

        embed.set_author(name='Help')
        embed.add_field(
            name=f'{client.command_prefix}bobby',
            value='Display a random quote from Bobby.',
            inline=False
        )

        await ctx.send(author, embed=embed)

    @client.command()
    async def bobby(ctx):
        await ctx.send(util.random_bobby_quote())
