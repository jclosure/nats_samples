import asyncio

def _fwrap(f, gf):
    try:
        f.set_result(gf.result())
    except Exception as e:
        f.set_exception(e)

def fwrap(gf, loop=None):
    '''
        Wraps a GRPC result in a future that can be yielded by asyncio

        Usage::

            async def my_fn(param):
                result = await fwrap(stub.function_name.future(param, timeout))

        TODO(JOEL):
            to get a future for this:
            see: use loop.create_task()
            http://masnun.com/2015/11/20/python-asyncio-future-task-and-the-event-loop.html

    '''
    f = asyncio.Future()

    if loop is None:
        loop = asyncio.get_event_loop()

    gf.add_done_callback(lambda _: loop.call_soon_threadsafe(_fwrap, f, gf))
    return f
