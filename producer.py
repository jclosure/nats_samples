import asyncio
from datetime import datetime
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout


class Client:
    def __init__(self, nc, loop=asyncio.get_event_loop()):
        self.nc = nc
        self.loop = loop

    @asyncio.coroutine
    def send(self, topic, msg):
        try:
            yield from self.nc.connect(io_loop=self.loop)
        except:
            pass

        nc = self.nc
        try:
            yield from nc.publish(topic, "please: {}".format(msg).encode())


        except ErrConnectionClosed:
            print("Connection closed prematurely")

        if nc.is_connected:

            # Wait a bit for messages to be dispatched...
            # yield from asyncio.sleep(2, loop=self.loop)

            # Detach from the server.
            yield from nc.close()

        if nc.last_error is not None:
            print("Last Error: {}".format(nc.last_error))

        if nc.is_closed:
            print("Disconnected.")


def publish(topic, msg):
    c = Client(NATS())
    c.loop.run_until_complete(c.send(msg))
    c.loop.close()
