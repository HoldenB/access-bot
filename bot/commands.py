import discord
import bot.util as util
from bot.client import CustomClient


#######################################################################
# Helper functions

async def command_status_cooldown(cmd: str,
                                  client: CustomClient,
                                  duration: int,
                                  ctx) -> bool:
    """Accepts a command context and extracts the user who sent
    the command. Once the user is extracted, a cooldown is then
    registed with the client for the given issuer of the command.
    This command cooldown is tracked on the client. If this is called
    and the user is not currently on cooldown, we'll return True and
    you should proceed with your command. Otherwise if the user is
    on cooldown with the command, we'll return False and an early
    return is necessary.

    Arguments:
        cmd {str} -- The command name
        client {CustomClient} -- The CustomClient instance
        duration {int} -- duration of the command cooldown
        ctx {Context} -- Command context

    Returns:
        bool -- True if the issuer of the command is not on cooldown,
        and has just been placed on cooldown. False if the user is
        currently on cooldown with the given command.
    """
    user_id = ctx.message.author.id
    if client.member_on_cooldown(cmd, user_id):
        await ctx.message.author.send(
            'Command on cooldown. Please wait'
            f' {client.member_cooldown_time(cmd, user_id)}'
            ' seconds to use this command again.')
        return True

    client.add_access_member(cmd, user_id, duration)
    return False


#######################################################################
# Commands

class Command:
    """Command base class. This class stores a description
    and the command that is associated with it.
    """
    def __init__(self, description: str):
        self.description = description
        self.cmd = None


class BobbyCommand(Command):
    """This command displays a random quote from Bobby
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__('Display a random quote from Bobby.')

        @client.command()
        async def bobby(ctx):
            await ctx.send(util.random_bobby_quote())

        self.cmd = bobby


class AccessCommand(Command):
    """This command provides users with a one time access
    token to view/download files.
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__(
            'Privides the user with a one time access token to view/download files.')

        @client.command()
        async def access(ctx):
            if ctx.message.channel.type == discord.ChannelType.private:
                await ctx.message.author.send(
                    'Command: $access failed. Please do not send this command in a private message.')
                return

            if await command_status_cooldown('access', client, 120, ctx):
                return

            #TODO store this user data in a database
            data = util.UserData.generate_user_data(ctx)

            await ctx.message.author.send(f'Here is your password secret: {data.secret}')

        self.cmd = access


class LatencyCommand(Command):
    """Command to check the Client's latency
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__('Check the client\'s latency.')

        @client.command()
        async def ping(ctx):
            await ctx.send(f'My ping is {round(client.latency * 1000)}ms!')

        self.cmd = ping


# TODO Make sure this is admin only!
class KillCommand(Command):
    """This command forces the client to logout
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__('Force the client to logout.')

        @client.command()
        async def kill(ctx):
            await client.logout()

        self.cmd = kill


#######################################################################

def add_commands(client: CustomClient) -> None:
    """Adds all configured commands to custom client

    Arguments:
        client {CustomClient} -- Custom client object
    """
    custom_commands = [
        BobbyCommand(client),
        AccessCommand(client),
        LatencyCommand(client),
        KillCommand(client)
    ]

    @client.command()
    async def help(ctx):
        author = ctx.message.author
        embed = discord.Embed(
            color=discord.Color.orange()
        )

        embed.set_author(name='Help')

        for command in custom_commands:
            if command is None:
                print(f'commands.py:add_commands: Custom command not found.'
                      ' Did you forget to set a cmd param?')
                continue

            embed.add_field(
                name=f'{client.command_prefix}{command.cmd.name}',
                value=command.description,
                inline=False
            )

        await ctx.send(author, embed=embed)
