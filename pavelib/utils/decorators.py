""" a collection of utililty decorators for paver tasks """

from __future__ import print_function

import multiprocessing
from functools import wraps


def timeout(limit=60):
    """
    kill a function if it has not completed within a specified timeframe
    """

    def _handle_threaded_function(*args, **kwargs):
        queue = kwargs['queue']
        function = kwargs['threaded_function']
        function_args = args
        function_kwargs = kwargs['function_kwargs']
        function_output = function(*function_args, **function_kwargs)
        queue.put(function_output)

    def decorated_function(function):

        def function_wrapper(*args, **kwargs):
            queue = multiprocessing.Queue()
            args_tuple = tuple(a for a in args)
            meta_kwargs = {
                'threaded_function': function, 'queue': queue,
                'function_kwargs': kwargs
            }
            function_proc = multiprocessing.Process(
                target=_handle_threaded_function, args=args_tuple, kwargs=meta_kwargs
            )
            function_proc.start()
            function_proc.join(float(limit))
            if function_proc.is_alive():
                function_proc.terminate()
                print("Function timed out before returning a value")
                raise TimeoutException
            function_output = queue.get()
            return function_output

        return wraps(function)(function_wrapper)

    return decorated_function

class TimeoutException(Exception):
    pass
