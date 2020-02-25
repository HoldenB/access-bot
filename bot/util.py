import random
import secrets
import threading
import time
import discord


class CustomTimer(threading.Timer):
    """Customer timer object. This extends threading.Timer
    and provides a way of getting the remaining time.
    """
    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__(interval, function, args=None, kwargs=None)
        self._start_time = 0.0

    def start_timer(self) -> None:
        """Forward call to start the timer
        """
        self._start_time = time.time()
        super().start()

    def time_remaining(self) -> int:
        """Get the remaining time left on the timer

        Returns:
            int -- The time remaining in seconds
        """
        elapsed_time = time.time()
        return int(self.interval - (elapsed_time - self._start_time))


class UserData:
    """Object that stores discord user data
    """
    def __init__(self, user_id: str, user_roles: list, secret: str):
        """
        Note:
            Use the generate_user_data() function to create a valid instance
            of this object

        Arguments:
            user_id {str} -- Unique user ID
            user_roles {list} -- List of roles assigned to this Member
            secret {str} -- Generated password secret
        """
        self.user_id = user_id
        self.user_roles = user_roles
        self.secret = secret

    def __repr__(self):
        return f'User ID: {self.user_id}\nRoles: {self.user_roles}\nSecret: {self.secret}'

    @staticmethod
    def generate_user_data(ctx):
        """Generate a valid instance of a UserData object
        from a message context

        Arguments:
            ctx {Context} -- Message context

        Returns:
            UserData -- A valid UserData instance
        """
        #TODO possibly check against channels here to see which
        # channels are available to the user
        # ie: ctx.message.author.permissions_in(channel_name)

        #TODO hash the secret and do not store it, only store the hash
        return UserData(
            ctx.message.author.id,
            [role.name for role in ctx.message.author.roles],
            generate_secret()
        )


def generate_secret(num_bytes: int = 16) -> str:
    """Generate a random URL-safe text string, containing num_bytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately
        1.3 characters. Default returns a 16 byte string.

    Keyword Arguments:
        num_bytes {int} -- Number of bytes (default: {16})

    Returns:
        str -- Returns a random URL-safe text string
    """
    return secrets.token_urlsafe(nbytes=num_bytes)


def random_bobby_quote() -> str:
    """Generate a random Bobby quote and return it to the caller

    Returns:
        str -- A string containing a random Bobby quote
    """
    return random.choice(
        ['Come on baby, why don\'t you come over tonight. I\'ve got a new laser pointer.',
         'He can have a new flavor every day! He\'s dating the ice cream lady!',
         'You had me at "fruit pies."',
         'I\'m going to grow up without anyone to love and die friendless and alone like Weird Al Yancovich.',
         'My dad says butane\'s a bastard gas.',
         'Hey, I didn\'t go looking for trouble. Trouble came-a-knockin\' and Bobby Hill\'s foot answered the door.',
         'My sloppy joe is all sloppy and no joe!',
         'It\'s not a crutch dad, it\'s just something I\'m relying on to get me through life.',
         'Look, dad, I\'m not gonna do drugs. I want to be the first chubby comedian to live past 35.',
         'Can I put a gun rack on my bike?']
    )
