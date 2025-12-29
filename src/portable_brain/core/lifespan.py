from contextlib import asynccontextmanager, AsyncExitStack
from fastapi import FastAPI
from portable_brain.config.app_config import get_service_settings
from portable_brain.common.logging.logger import logger
from portable_brain.common.db.session import create_db_engine_context, parse_db_settings_from_service, DBSettings, DBType

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the service's startup and shutdown events.
    """
    # default start up message
    logger.info(f"Starting Portable-Brain service!")

    # initialize resources during start up
    logger.info("Initializing service resources...")
    settings = get_service_settings()

    async with AsyncExitStack() as stack:
        
        # TODO: add any initialization code here
        # use stack.enter_async_context when the resource has __aenter__ and __aexit__ support
        # use stack.push_async_context to register the clean up method only

        # Main db engine

        # parse main db settings, and create engine
        main_db_settings = parse_db_settings_from_service(settings, DBType.MainDB)
        app.state.main_db_engine = await stack.enter_async_context(
            create_db_engine_context(
                db_settings=main_db_settings
            )
        )
        logger.info("Main database engine initialized.")

        try:
            # lets FastAPI process requests during yield
            yield
        finally:
            # explicit resource clean up, otherwise automatically cleaned via exit stack
            logger.info("Shutting down service resources...")
            # TODO: add any explicit cleanup / shutdown code here

        # The AsyncExitStack will automatically call the __aexit__ or registered cleanup
        # methods for all resources entered or pushed to it, in reverse order.
        logger.info("All global resources have been gracefully closed.")
