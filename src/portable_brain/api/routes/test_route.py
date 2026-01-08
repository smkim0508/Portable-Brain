# test route for router + dependency injection

import time
from fastapi import APIRouter, Depends
from portable_brain.common.logging.logger import logger
from portable_brain.common.db.session import get_async_session_maker
from portable_brain.core.dependencies import get_main_db_engine, get_droidrun_client
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/test", tags=["Tests"])

@router.get("/first-test")
async def first_test():
    logger.info("first test route")
    return {"message": "this is the first test route"}

@router.get("/second-test")
async def second_test(main_db_engine: AsyncEngine = Depends(get_main_db_engine)):
    logger.info("second test route, trying to inject db session")
    main_session_maker = get_async_session_maker(main_db_engine)

    try:
        async with main_session_maker() as session:
            await session.execute(text("SELECT 1"))
    except Exception as e:
        logger.info(f"error: {e}")
        return {"message": "unable to inject db session"}

    logger.info(f"db session successfully injected, dummy query passed")
    return {"message": "db session successfully injected, dummy query passed"}

@router.get("/get-raw-tree")
async def get_raw_accessibility_tree(
    droidrun_client: DroidRunClient = Depends(get_droidrun_client)
):
    """
    Get the raw accessibility tree from the current screen.
    Returns all available information from the a11y tree including:
    - raw_tree: Complete unfiltered accessibility tree
    - formatted_text: Human-readable indexed UI description
    - focused_element: Currently focused element
    - ui_elements: Parsed list of UI elements
    - phone_state: Current app package, activity, and editable status
    """
    try:
        logger.info("Fetching raw accessibility tree from current screen")
        state = await droidrun_client.get_current_state()
        raw_tree = await droidrun_client.get_raw_tree()

        return {
            "message": "Successfully retrieved raw accessibility tree",
            # "raw_tree": state["raw_tree"],
            "formatted_text": state["formatted_text"],
            "focused_element": state["focused_element"],
            "ui_elements": state["ui_elements"],
            "phone_state": state["phone_state"],
            "timestamp": state["timestamp"]
        }
        # return {
        #     "message": "ok",
        #     "raw_tree": raw_tree["raw_tree"]
        # }
    except Exception as e:
        logger.error(f"Error fetching raw accessibility tree: {e}")
        return {"message": f"Error fetching raw accessibility tree: {e}"}, 500
