import asyncio
from MeowthLogger import Logger

from fastapi import FastAPI

from MeowthLogger.utilities.fastapi.log_stream import StreamManager
from MeowthLogger.utilities.fastapi.views import get_log_stream_views_router


loop = asyncio.new_event_loop()
managa = StreamManager(loop)
api = FastAPI()


@api.get("/")
async def home():
    return {"ok": True}

logger = Logger(use_files=True, use_uvicorn=True, stream=managa)
logger.info("TEST")


api.include_router(
    get_log_stream_views_router(logger)
)

from uvicorn import Config, Server

config = Config(
    app=api,
    host="0.0.0.0",
    log_config=None
)

server = Server(config)

async def main():
    await server.serve()

if __name__ == "__main__":
    # loop.create_task(server.serve())
    # loop.run_forever()
    asyncio.run(main())