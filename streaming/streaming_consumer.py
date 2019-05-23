import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

# randomizing client ids for broadcast
import uuid
client_id=str(uuid.uuid1())

async def run(loop):
    nc = NATS()
    sc = STAN()

    # Start session with NATS Streaming cluster using
    # the established NATS connection.
    await nc.connect(io_loop=loop)
    await sc.connect("test-cluster", client_id, nats=nc)

    # Example async subscriber
    async def cb(msg):
        print("Received a message (seq={}): {}".format(msg.seq, msg.data))

    # Subscribe to get all messages from the beginning.
    await sc.subscribe("greetings", start_at='first', cb=cb)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()
