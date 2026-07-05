import json
import os
from mcp.crop_mcp_server import CropMCPServer

class CropMCPClient:
    """
    Simulates an MCP Client connection to the local CropMCPServer.
    Constructs JSON-RPC 2.0 messages, executes them, and parses the response.
    """
    def __init__(self, data_dir="data"):
        # Instantiate server directly in-memory to preserve 100% offline, zero-dependency behavior
        # while keeping the JSON-RPC interface intact.
        self.server = CropMCPServer(data_dir=data_dir)
        self.request_counter = 1

    def _call_rpc_method(self, tool_name: str, arguments: dict) -> str:
        """
        Wraps arguments in a JSON-RPC request, sends to server, and returns the text response content.
        """
        req_id = self.request_counter
        self.request_counter += 1

        request_body = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }

        # Serialize to simulate RPC transmission
        request_str = json.dumps(request_body)
        
        # Server processes request and returns serialized response
        response_str = self.server.handle_request(request_str)
        
        # Deserialize response
        response = json.loads(response_str)
        
        if "error" in response:
            raise Exception(f"MCP RPC Error: {response['error'].get('message', 'Unknown Error')}")
            
        result = response.get("result", {})
        if result.get("isError"):
            error_content = result.get("content", [{}])[0].get("text", "Unknown tool error")
            raise Exception(f"MCP Tool Execution Error: {error_content}")

        # Extract text content
        contents = result.get("content", [])
        if contents and contents[0].get("type") == "text":
            return contents[0].get("text", "")
            
        return ""

    def get_market_prices(self, crop: str, state: str, district: str) -> dict:
        """
        Fetches market prices via MCP Tool call.
        """
        result_str = self._call_rpc_method("get_market_prices", {
            "crop": crop,
            "state": state,
            "district": district
        })
        try:
            return json.loads(result_str)
        except json.JSONDecodeError:
            return {"raw_text": result_str}

    def get_government_schemes(self, crop: str, state: str) -> list:
        """
        Fetches schemes via MCP Tool call.
        """
        result_str = self._call_rpc_method("get_government_schemes", {
            "crop": crop,
            "state": state
        })
        try:
            return json.loads(result_str)
        except json.JSONDecodeError:
            return [{"raw_text": result_str}]

    def get_weather_data(self, state: str, district: str) -> dict:
        """
        Fetches weather data via MCP Tool call.
        """
        result_str = self._call_rpc_method("get_weather_data", {
            "state": state,
            "district": district
        })
        try:
            return json.loads(result_str)
        except json.JSONDecodeError:
            return {"raw_text": result_str}

    def save_action_plan(self, filename: str, content: str) -> str:
        """
        Saves the action plan to the filesystem via MCP Tool call.
        """
        return self._call_rpc_method("save_action_plan", {
            "filename": filename,
            "content": content
        })
