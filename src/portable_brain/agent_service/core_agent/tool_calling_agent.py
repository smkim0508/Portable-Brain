# main tool calling agent, connects to droidrun

# import clients
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient
from portable_brain.common.services.llm_service.llm_client.google_genai_client import AsyncGenAITypedClient

# import tool calling declarations
from portable_brain.common.services.llm_service.tool_calling.gemini.droidrun_tool_declaration import droidrun_execution_declaration

class ToolCallingAgent():
    """
    Main agent to handle tool calling and execution.
    Receives memory context and executes commands on device via tool calls to droidrun.

    NOTE: no repository intialized yet.
    """
    def __init__(self, droidrun_client: DroidRunClient, gemini_llm_client: AsyncGenAITypedClient):
        self.droidrun_client = droidrun_client
        self.llm_client = gemini_llm_client # NOTE: for now, this llm client must be the gemini client (not dispatcher) to allow atool_call() method
    
    # test helper to connect with droidrun
    def test_tool_call(self):
        # come up with dummy system prompt
        test_system_prompt = "You are a helpful assistant."
        test_user_prompt = "Tell me my device name."
        
        # execute a baseline command to verify that LLM is able to call droidrun
        return self.llm_client.atool_call(
            system_prompt=test_system_prompt,
            user_prompt=test_user_prompt,
            function_declarations=[droidrun_execution_declaration],
            tool_executors={"execute_command": self.droidrun_client.execute_command},
            max_turns=5
        )
