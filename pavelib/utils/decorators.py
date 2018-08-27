""" decorators for paver """

import time
from threading import Thread

def timeout(function, limit=60):
    """
    kill a function if it has not completed within a specified timeframe
    """

    def timed_function():

        function_thread = Thread(target=function)
        function_thread.start()

        function_thread.join(float(limit))

        if function_thread.is_alive():
            raise TimeoutException

    return timed_function()

class TimeoutException(Exception):
    pass
