
"""
Make a couple of event loops and a couple of new threads and assign each
event loop to a thread.  Then just send in work as needed.

"""

import asyncio, threading

def hello(thread_name):
    print('hello from thread {}!'.format(thread_name))

event_loop_a = asyncio.new_event_loop()
event_loop_b = asyncio.new_event_loop()

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=lambda: run_loop(event_loop_a)).start()
threading.Thread(target=lambda: run_loop(event_loop_b)).start()

event_loop_a.call_soon_threadsafe(lambda: hello('a'))
event_loop_b.call_soon_threadsafe(lambda: hello('b'))

event_loop_a.call_soon_threadsafe(event_loop_a.stop)
event_loop_b.call_soon_threadsafe(event_loop_b.stop)

class Parcel(object):
    """Wraps for carrying between threads"""

    def __init__(self, data):
        super(Parcel, self).__init__()
        self.data = data
