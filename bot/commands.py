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


async def is_private_channel(cmd: str, ctx) -> bool:
    """Checks to see if the incoming message has been
    sent from a private channel

    Arguments:
        cmd {str} -- The command name
        ctx {Context} -- Command context

    Returns:
        bool -- True if the message has been sent from a
        private channel. False otherwise.
    """
    if ctx.message.channel.type == discord.ChannelType.private:
        await ctx.message.author.send(
            f'Command: ${cmd} failed: Please do not send this command in a private message.')
        return True

    return False


def gen_command_help_embed(commands: list,
                           cmd_type: str,
                           client: CustomClient,
                           ctx) -> discord.Embed:
    """Generate a "help" embed for a list of
    commands. A command type should be passed to
    populate the title of the embed.

    Arguments:
        commands {list} -- List of commands
        cmd_type {str} -- Command type, ie. Custom, Admin, etc.
        client {CustomClient} -- Custom client
        ctx {Context} -- Command context

    Returns:
        discord.Embed -- The "help" embed for the list
        of commands
    """
    embed = discord.Embed(
        title=f'{cmd_type} Command Help',
        description=f'A list of {cmd_type} commands that you are able to use',
        color=discord.Color.orange()
    )

    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

    for command in commands:
        if command is None:
            print(f'commands.py:add_commands: Custom command not found.'
                ' Did you forget to set a cmd param?')
            continue

        embed.add_field(
            name=f'{client.command_prefix}{command.cmd.name}',
            value=command.description,
            inline=False
        )

    return embed


#######################################################################
# Commands

class Command:
    """Command base class. This class stores a description
    and the command that is associated with it.
    """
    def __init__(self, description: str, is_admin: bool = False):
        self.description = description
        self.is_admin = is_admin
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
            cmd = 'access'

            if await is_private_channel(cmd, ctx):
                return
            if await command_status_cooldown(cmd, client, 120, ctx):
                return

            #TODO store this user data in a database
            data = util.UserData.generate_user_data(ctx)

            await ctx.message.author.send(f'Here is your password secret:')
            # Send on a new line so that it's easily copyable on mobile
            await ctx.message.author.send(data.secret)

        self.cmd = access


class LatencyCommand(Command):
    """Command to check the Client's latency
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__('Check the client\'s latency.', True)

        @client.command()
        @discord.ext.commands.has_permissions(administrator=True)
        async def ping(ctx):
            await ctx.send(f'My ping is {round(client.latency * 1000)}ms!')

        self.cmd = ping


class KillCommand(Command):
    """This command forces the client to logout
    """
    def __init__(self, client: CustomClient):
        """
        Arguments:
            client {CustomClient} -- Discord client object
        """
        super().__init__('Force the client to logout.', True)

        @client.command()
        #TODO possibly just remove this and manually implement so that
        # feedback can be provided to the issuer
        @discord.ext.commands.has_permissions(administrator=True)
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

    # Separate admin commands and filter out the original ones
    admin_commands = [c for c in custom_commands if c.is_admin]
    custom_commands = [c for c in custom_commands if not c.is_admin]

    @client.command()
    async def help(ctx):
        # User must call this in a non-private channel, however the response
        # is sent via private. This is to ensure non-admin users cannot see
        # admin commands
        if await is_private_channel('help', ctx):
            return

        author = ctx.message.author
        author_is_admin = author.top_role.permissions.administrator

        await author.send(
            author, embed=gen_command_help_embed(
                custom_commands, 'Custom', client, ctx))

        if not author_is_admin:
            return

        # If the author is an admin, also send them the
        # list of admin commands
        await author.send(
            author, embed=gen_command_help_embed(
                admin_commands, 'Admin', client, ctx))
