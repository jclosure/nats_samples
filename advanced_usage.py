import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout, ErrNoServers

nc = NATS()

async def run(loop):


    try:
        if not nc.is_connected:
            # Setting explicit list of servers in a cluster.
            await nc.connect(servers=["nats://127.0.0.1:4222", "nats://127.0.0.1:4223", "nats://127.0.0.1:4224"], loop=loop)
    except ErrNoServers as e:
        print(e)
        return

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        for i in range(0, 20):
            await nc.publish(reply, "i={i}".format(i=i).encode())

    await nc.subscribe("help.>", cb=message_handler)

    async def request_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    import math
    # Signal the server to stop sending messages after we got 10 already.
    await nc.request(
        "help.please", b'help', expected=int("inf"), cb=request_handler)

    try:
        # Flush connection to server, returns when all messages have been processed.
        # It raises a timeout if roundtrip takes longer than 1 second.
        await nc.flush(1)
    except ErrTimeout:
        print("Flush timeout")

    await asyncio.sleep(1, loop=loop)

    # Drain gracefully closes the connection, allowing all subscribers to
    # handle any pending messages inflight that the server may have sent.
    # await nc.drain()

def main():
    loop = asyncio.get_event_loop()
    # (run(loop))
    # loop.close()
    loop.create_task(run(loop))
    loop.run_forever()
    return loop

if __name__ == '__main__':
    main()
