# src/monitoring/observation_tracker.py
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient
from portable_brain.common.types.android_apps import AndroidApp
from portable_brain.common.logging.logger import logger

# Canonical DTOs for UI state, inferred action, observations
from portable_brain.monitoring.background_tasks.types.ui_states.ui_state import UIState, UIActivity
from portable_brain.monitoring.background_tasks.types.ui_states.state_changes import UIStateChange, StateChangeSource
from portable_brain.monitoring.background_tasks.types.ui_states.state_change_types import StateChangeType
from portable_brain.monitoring.background_tasks.types.action.action_types import ActionType
from portable_brain.monitoring.background_tasks.types.action.actions import (
    Action,
    AppSwitchAction,
    UnknownAction,
    InstagramMessageSentAction,
    InstagramPostLikedAction,
    WhatsAppMessageSentAction,
    SlackMessageSentAction,
    # TBD
)

class ObservationTracker:
    """
    Track ALL device state changes, including manual user actions.
    - Client refers to the main DroidRunClient instance.
    - The client's helper are used to detect state changes.

    This complements DroidRunClient.action_history which only tracks
    execute_command() actions.

    TODO: finish implementing this tracker.
    - Also create canonical DTO for observations and enums for actions
    """

    def __init__(self, client: DroidRunClient):
        self.client = client
        self.inferred_actions: List[Action] = []
        # TODO: add observations that feed to memory handler
        self.running = False
        self._tracking_task: Optional[asyncio.Task] = None

    async def start_tracking(self, poll_interval: float = 1.0):
        """
        Start continuous observation tracking.

        Args:
            poll_interval: How often to poll for changes (seconds)
        """
        self.running = True

        while self.running:
            try:
                # Detect any state change
                change: UIStateChange | None = await self.client.detect_state_change()

                if change:
                    # Infer what action might have caused this change
                    inferred_action = self._infer_action(change)

                    # Store inferred actions
                    self.inferred_actions.append(inferred_action)

                    # TODO: should be handled by memory handler in future
                    # await self.memory_handler.process_observation(observation)
                    # shorter cooldown if state change HAS been found -> likely another action might pursue
                    await asyncio.sleep(0.2)
                else:
                    await asyncio.sleep(poll_interval) # cooldown after each iteration

            except Exception as e:
                print(f"Observation tracking error: {e}")
                await asyncio.sleep(5)  # Back off on error

    def _infer_action(self, change: UIStateChange) -> Action:
        """
        Infer a user action from recorded UI state change.
        Returns an Action object, based on change type and state metadata.
        Returns UnknownAction if action can't be inferred.
        """

        # parse change
        change_type: StateChangeType = change.change_type
        before: UIState = change.before # states
        after: UIState = change.after # states
        curr_package: str = before.package

        # TODO: infer all actions based on each change type and state metadata
        if change.change_type == StateChangeType.APP_SWITCH:
            return AppSwitchAction(
                timestamp=change.timestamp,
                source_change_type=change.change_type,
                package=change.after.package,
                source=change.source,
                description=change.description,
                src_package=change.before.package,
                src_activity=change.before.activity,
                dst_package=change.after.package,
                dst_activity=change.after.activity,
            )

        # else, see if current app is supported
        elif curr_package == AndroidApp.INSTAGRAM:
            if change_type == StateChangeType.TEXT_INPUT:
                return InstagramMessageSentAction(
                    timestamp=change.timestamp,
                    source_change_type=change.change_type,
                    actor_username=change.after.raw_tree.get("username", "unknown user") if change.after.raw_tree else "unknown user", # actor username
                    target_username=change.after.raw_tree.get("target_username", "unknown user") if change.after.raw_tree else "unknown user", # target username
                    source=change.source,
                    # importance is set to default 1.0 for now
                    description=change.description,
                    message_summary=None, # should use UI states diff to infer message summary w/ LLM
                )
            # otherwise no other actions are supported for Instagram, so return unknown

        elif curr_package == AndroidApp.WHATSAPP:
            if change_type == StateChangeType.TEXT_INPUT:
                return WhatsAppMessageSentAction(
                    timestamp=change.timestamp,
                    source_change_type=change.change_type,
                    recipient_name=change.after.raw_tree.get("recipient_name", "unknown user") if change.after.raw_tree else "unknown user",
                    is_dm=change.after.raw_tree.get("is_dm", False) if change.after.raw_tree else False,
                    target_name=change.after.raw_tree.get("target_name", "unknown user") if change.after.raw_tree else "unknown user",
                    source=change.source,
                    # importance is set to default 1.0 for now
                    description=change.description,
                    message_summary=None,
                )
            # otherwise no other actions are supported for WhatsApp, so return unknown
        
        elif curr_package == AndroidApp.SLACK:
            if change_type == StateChangeType.TEXT_INPUT:
                return SlackMessageSentAction(
                    timestamp=change.timestamp,
                    source_change_type=change.change_type,
                    workspace_name=change.after.raw_tree.get("workspace_name", "unknown workspace") if change.after.raw_tree else "unknown workspace",
                    channel_name=change.after.raw_tree.get("channel_name", "unknown channel") if change.after.raw_tree else "unknown channel",
                    thread_name=change.after.raw_tree.get("thread_name", None) if change.after.raw_tree else None,
                    target_name=change.after.raw_tree.get("target_name", "unknown user") if change.after.raw_tree else "unknown user",
                    source=change.source,
                    # importance is set to default 1.0 for now
                    description=change.description,
                    message_summary=None,
                )
            # otherwise no other actions are supported for Slack, so return unknown

        # if action can't be inferred, return UnknownAction 
        return UnknownAction(
            timestamp=change.timestamp,
            source_change_type=change.change_type,
            package=change.after.package,
            source=change.source,
            importance=0.0, # TEMP: for unknown actions, we override importance to 0.0
            description=change.description,
        )

    def _create_observation(self, change: Dict[str, Any]) -> Optional[Action]:
        """
        Creates the final observation object based on the action dictionary.
        This is a high-level abstraction derived from a union of low-level actions.
        NOTE: observation is what's ultimately stored in the memory.
        """
        change_type: StateChangeType = change["change_type"] # TODO: add change DTO
        before = change["before"] # states
        after = change["after"] # states
        curr_package = before["package"]

        if change_type == StateChangeType.APP_SWITCH:
            return AppSwitchAction(
                timestamp=change["timestamp"],
                source_change_type=change_type,
                package=after["package"],
                source=change["source"],
                importance=change["importance"],
                description=change["description"],
                src_package=before["package"],
                src_activity=before["activity"],
                dst_package=after["package"],
                dst_activity=after["activity"],
            )

        # else, see if current app supports special tracking
        elif curr_package == AndroidApp.INSTAGRAM:
            if change_type == StateChangeType.TEXT_INPUT:
               return InstagramMessageSentAction(
                   timestamp=change["timestamp"],
                   source_change_type=change["change_type"],
                   actor_username=change["username"], # actor username
                   target_username=change["target_username"],
                   source=change["source"],
                   importance=change["importance"],
                   description=change["description"],
                   message_summary=change["message_summary"], # should use UI states diff to infer message summary w/ LLM
               )
            else:
                return None

        elif curr_package == AndroidApp.WHATSAPP:
            if change_type == StateChangeType.TEXT_INPUT:
               return WhatsAppMessageSentAction(
                   timestamp=change["timestamp"],
                   source_change_type=change["change_type"],
                   recipient_name=change["name"],
                   is_dm=change["is_dm"],
                   target_name=change["target_name"],
                   source=change["source"],
                   importance=change["importance"],
                   description=change["description"],
                   message_summary=change["message_summary"],
               )
            else:
                return None
        
        elif curr_package == AndroidApp.SLACK:
            if change_type == StateChangeType.TEXT_INPUT:
               return SlackMessageSentAction(
                   timestamp=change["timestamp"],
                   source_change_type=change["change_type"],
                   workspace_name=change["workspace_name"],
                   channel_name=change["channel_name"],
                   thread_name=change["thread_name"],
                   target_name=change["target_name"],
                   source=change["source"],
                   importance=change["importance"],
                   description=change["description"],
                   message_summary=change["message_summary"],
               )
            else:
                return None
        else:
            logger.info(f"Unknown action, change type: {change_type}")
            return None

    def get_observations(
        self,
        limit: Optional[int] = None,
        change_types: Optional[List[str]] = None,
    ) -> List[Action]:
        """
        Get observation history.

        Args:
            limit: Max observations to return
            change_types: Filter by change types (e.g., ['app_switch', 'screen_change'])

        Returns:
            List of observations
            NOTE: the bottom index in returned list is the most recent. Possibly reverse indices to fetch most recent on top.
        """
        observations = self.inferred_actions

        if change_types:
            observations = [
                o for o in observations
                if o.source_change_type in change_types
            ]

        if limit:
            observations = observations[-limit:]
        
        observations.reverse() # make the first observation the most recent

        return observations

    def clear_observations(self):
        """Clear observation history after persisting to DB."""
        self.inferred_actions = []

    def start_background_tracking(self, poll_interval: float = 1.0):
        """
        Start tracking as a background task.
        Currently called by the background tracking endpoint.

        Args:
            poll_interval: How often to poll for changes (seconds)
        """
        if self._tracking_task is not None and not self._tracking_task.done():
            raise RuntimeError("Observation tracking already running")

        self._tracking_task = asyncio.create_task(self.start_tracking(poll_interval))
        return self._tracking_task

    async def stop_tracking(self):
        """
        Stop observation tracking and wait for cleanup.
        Call this in lifespan shutdown.
        """
        self.running = False

        # Wait for the tracking loop to exit gracefully
        if self._tracking_task is not None and not self._tracking_task.done():
            try:
                # Give it a moment to finish current iteration
                await asyncio.wait_for(self._tracking_task, timeout=5.0)
            except asyncio.TimeoutError:
                # Force cancel if it doesn't stop gracefully
                self._tracking_task.cancel()
                try:
                    await self._tracking_task
                except asyncio.CancelledError:
                    pass  # Expected
    