import asyncio
import threading

loop = None  # this will hold the event loop instance

def start_asyncio_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()