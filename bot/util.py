import random
import threading
import time


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
