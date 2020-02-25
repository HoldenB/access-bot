from discord.ext import commands
import bot.util as util


class CustomClient(commands.Bot):
    """Custom bot command client. This custom client introduces
    an API that allows timed lockouts on commands.
    """
    def __init__(self, token: str, guild: str, command_prefix: str = '$'):
        """
        Arguments:
            token {str} -- Bot client secret key (Token)
            guild {str} -- Discord Guild/Server that the client will run on
        Keyword Arguments:
            command_prefix {str} -- Prefix string for bot commands (default: {'$'})
        """
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
        """Adds an access member with an alloted command cooldown timer

        Arguments:
            member {str} -- The member (user_id) to add
            cooldown {int} -- Alloted time between command usage
        """
        timer = util.CustomTimer(cooldown, lambda: self._on_timer_timeout(member))
        self._member_timers.update({member: timer})
        # Start the timer
        self._member_timers[member].start_timer()

    def member_on_cooldown(self, member: str) -> bool:
        """Checks the member to see if they are able to use a command

        Arguments:
            member {str} -- The member (user_id) to check
        Returns:
            bool -- True if the member is on command cooldown/unable
            to currently use the command. False otherwise.
        """
        return member in self._member_timers.keys()

    def member_cooldown_time(self, member: str) -> int:
        """Remaining duration of the members cooldown timer

        Arguments:
            member {str} -- The member (user_id) to check
        Returns:
            int -- The duration left in seconds
        """
        if not member in self._member_timers.keys():
            return 0

        return self._member_timers[member].time_remaining()

    def run_custom_client(self) -> None:
        """Run the client and connect to the given guild
        """
        super().run(self._token)

    async def on_ready(self):
        """Handle when the bot has connected to the given guild

        Note:
            This function is async
        """
        print(f'{self.user} Has connected to Discord!')

    async def on_message(self, message: str):
        """Handle when the client receives a message

        Arguments:
            message {str} -- The received message

        Note:
            This function is async
        """
        if message.author == self.user:
            return

        await self.process_commands(message)
