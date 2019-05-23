import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

async def run(loop):
    nc = NATS()
    sc = STAN()

    # First connect to NATS, then start session with NATS Streaming.
    await nc.connect(io_loop=loop)
    await sc.connect("test-cluster", "client-456", nats=nc)

    # Periodically send a message
    while True:
        await sc.publish("greetings", b'Hello World!')
        await asyncio.sleep(1, loop=loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()
