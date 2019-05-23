import asyncio
import os
import signal
from nats.aio.client import Client as NATS


def run(loop):
    nc = NATS()

    @asyncio.coroutine
    def closed_cb():
        print("Connection to NATS is closed.")
        yield from asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": ["nats://127.0.0.1:4222"],
        "io_loop": loop,
        "closed_cb": closed_cb
    }

    yield from nc.connect(**options)
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))

    @asyncio.coroutine
    def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a help_request message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        yield from nc.publish(reply, b'I can help')

    # Subscription on queue named 'workers' so that
    # one subscriber handles message a request at a time.
    yield from nc.subscribe("help", "workers", help_request)

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

def start(loop):
    try:
        loop.run_forever()
    finally:
        loop.close()

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
