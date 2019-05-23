import asyncio, os, sys
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

uri = "nats://127.0.0.1:4222"

def make_rpc_call(fn_name, request, timeout=5):
    loop = asyncio.get_event_loop()
    async def get_result():
        nc = NATS()
        await nc.connect(uri, loop=loop)
        try:
            response = await nc.request(fn_name, request, timeout)
            return response.data
        except ErrTimeout:
            print("Request timed out")
            raise
        finally:
            nc.close()
    return loop.run_until_complete(get_result())
