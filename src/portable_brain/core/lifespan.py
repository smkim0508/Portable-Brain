from contextlib import asynccontextmanager, AsyncExitStack
from fastapi import FastAPI
from portable_brain.config.app_config import get_main_settings
from portable_brain.common.logging.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's startup and shutdown events.
    """
    # default start up message
    logger.info(f"Starting Portable-Brain app!")

    # initialize resources during start up
    logger.info("Initializing app resources...")
    settings = get_main_settings()

    async with AsyncExitStack() as stack:
        
        # TODO: add any initialization code here
        # use stack.enter_async_context when the resource has __aenter__ and __aexit__ support
        # use stack.push_async_context to register the clean up method only

        try:
            # lets FastAPI process requests during yield
            yield
        finally:
            # explicit resource clean up, otherwise automatically cleaned via exit stack
            logger.info("Shutting down app resources...")
            # TODO: add any explicit cleanup / shutdown code here

        # The AsyncExitStack will automatically call the __aexit__ or registered cleanup
        # methods for all resources entered or pushed to it, in reverse order.
        logger.info("All global resources have been gracefully closed.")
