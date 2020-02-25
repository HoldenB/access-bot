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

        # Dictionary containing a command and the given members who have used
        # the command and are on cooldown for that command.
        # This will allow us to restrict access to spamming certain commands.
        # Command timers, eg:
        # _command_timers: {
        #   command_1: {
        #     member_1: CustomTimer(),
        #     member_2: CustomTimer()
        #   },
        #   command_2: {
        #     ...
        #   }
        # }
        self._command_timers = {}

        # Remove the default help command
        self.remove_command('help')

    def _on_timer_timeout(self, command: str, member: str) -> None:
        self._command_timers[command].pop(member)
        if not self._command_timers[command]:
            self._command_timers.pop(command)

    def add_access_member(self, command: str, member: str, cooldown: int) -> None:
        """Adds an access member to a command with an alloted command cooldown timer

        Arguments:
            command {str} -- The command to which to add a user to
            member {str} -- The member (user_id) to add
            cooldown {int} -- Alloted time between command usage
        """
        timer = util.CustomTimer(
            cooldown, lambda: self._on_timer_timeout(command, member))

        if command not in self._command_timers.keys():
            cmd_map = {member: timer}
            self._command_timers[command] = cmd_map
        else:
            self._command_timers[command].update({member: timer})

        # Start the timer
        self._command_timers[command][member].start_timer()

    def member_on_cooldown(self, command: str, member: str) -> bool:
        """Checks the member of a command to see if their alloted
        command cooldown is refreshed

        Arguments:
            command {str} -- The command to check
            member {str} -- The member (user_id) to check

        Returns:
            bool -- True if the member is on command cooldown/unable
            to currently use the command. False otherwise.
        """
        if command not in self._command_timers.keys():
            return False

        return member in self._command_timers[command].keys()

    def member_cooldown_time(self, command: str, member: str) -> int:
        """Remaining duration of the members cooldown timer
        for a given command

        Arguments:
            command {str} -- The command to check
            member {str} -- The member (user_id) to check

        Returns:
            int -- The duration left in seconds
        """
        if not command in self._command_timers.keys():
            return 0
        if not member in self._command_timers[command].keys():
            return 0

        return self._command_timers[command][member].time_remaining()

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
