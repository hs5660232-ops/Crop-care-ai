import os
import json

class CropMCPServer:
    """
    A Model Context Protocol (MCP) server that runs locally.
    Exposes tools to query offline datasets and write action plans to the filesystem.
    """
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.market_prices_path = os.path.join(data_dir, "market_prices.json")
        self.gov_schemes_path = os.path.join(data_dir, "government_schemes.json")
        self.weather_data_path = os.path.join(data_dir, "weather_data.json")

    def get_tools(self):
        """
        Returns the list of available MCP tools in standard MCP format.
        """
        return [
            {
                "name": "get_market_prices",
                "description": "Fetch local market rates (INR per quintal) and trends for a specific crop, state, and district.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "crop": {"type": "string", "description": "Name of the crop (e.g., Tomato, Wheat)."},
                        "state": {"type": "string", "description": "State name (e.g., Maharashtra, Punjab)."},
                        "district": {"type": "string", "description": "District name (e.g., Nashik, Ludhiana)."}
                    },
                    "required": ["crop", "state", "district"]
                }
            },
            {
                "name": "get_government_schemes",
                "description": "Fetch government agricultural schemes, insurance coverages, and subsidies applicable to a crop in a given state.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "crop": {"type": "string", "description": "Name of the crop."},
                        "state": {"type": "string", "description": "State name."}
                    },
                    "required": ["crop", "state"]
                }
            },
            {
                "name": "get_weather_data",
                "description": "Fetch current temperature, humidity, rainfall, and weather forecast for a state and district.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "description": "State name."},
                        "district": {"type": "string", "description": "District name."}
                    },
                    "required": ["state", "district"]
                }
            },
            {
                "name": "save_action_plan",
                "description": "Save the final Farm Action Plan markdown report to the local filesystem.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "The target file name (e.g., plan_tomato.md)."},
                        "content": {"type": "string", "description": "The full Markdown content of the Farm Action Plan."}
                    },
                    "required": ["filename", "content"]
                }
            }
        ]

    def handle_request(self, request_str: str) -> str:
        """
        Processes standard MCP JSON-RPC requests.
        """
        try:
            request = json.loads(request_str)
            method = request.get("method")
            req_id = request.get("id")

            if method == "tools/list":
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": self.get_tools()}
                })

            elif method == "tools/call":
                params = request.get("params", {})
                name = params.get("name")
                arguments = params.get("arguments", {})

                result = self.execute_tool(name, arguments)
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                })
            else:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                })

        except Exception as e:
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)}
            })

    def execute_tool(self, name: str, arguments: dict) -> dict:
        """
        Executes the specified tool with arguments.
        """
        if name == "get_market_prices":
            crop = arguments.get("crop")
            state = arguments.get("state")
            district = arguments.get("district")
            return self._tool_get_market_prices(crop, state, district)

        elif name == "get_government_schemes":
            crop = arguments.get("crop")
            state = arguments.get("state")
            return self._tool_get_government_schemes(crop, state)

        elif name == "get_weather_data":
            state = arguments.get("state")
            district = arguments.get("district")
            return self._tool_get_weather_data(state, district)

        elif name == "save_action_plan":
            filename = arguments.get("filename")
            content = arguments.get("content")
            return self._tool_save_action_plan(filename, content)

        else:
            return {"isError": True, "content": [{"type": "text", "text": f"Tool '{name}' not found."}]}

    def _tool_get_market_prices(self, crop, state, district):
        try:
            if not os.path.exists(self.market_prices_path):
                return {"isError": True, "content": [{"type": "text", "text": "Market price database not found."}]}
            
            with open(self.market_prices_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            crop_data = data.get(crop)
            if not crop_data:
                return {"content": [{"type": "text", "text": f"No market pricing found for crop: {crop}."}]}

            state_data = crop_data.get(state)
            if not state_data:
                return {"content": [{"type": "text", "text": f"No market pricing found for crop {crop} in state {state}."}]}

            district_data = state_data.get(district)
            if not district_data:
                # Fallback to state average or list available districts
                available = list(state_data.keys())
                return {"content": [{"type": "text", "text": f"No pricing details for district {district}. Available districts in {state}: {', '.join(available)}."}]}

            return {"content": [{"type": "text", "text": json.dumps(district_data, indent=2)}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Error: {str(e)}"}]}

    def _tool_get_government_schemes(self, crop, state):
        try:
            if not os.path.exists(self.gov_schemes_path):
                return {"isError": True, "content": [{"type": "text", "text": "Government schemes database not found."}]}

            with open(self.gov_schemes_path, "r", encoding="utf-8") as f:
                schemes = json.load(f)

            matched = []
            for s in schemes:
                crop_ok = s.get("crop_applicability") == "All" or crop in s.get("crop_applicability", [])
                state_ok = s.get("state_applicability") == "All" or state == s.get("state_applicability")
                
                if crop_ok and state_ok:
                    matched.append({
                        "scheme_name": s["scheme_name"],
                        "scope": s["scope"],
                        "benefits": s["benefits"],
                        "eligibility": s["eligibility"]
                    })

            if not matched:
                return {"content": [{"type": "text", "text": f"No government schemes found for crop {crop} in state {state}."}]}

            return {"content": [{"type": "text", "text": json.dumps(matched, indent=2)}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Error: {str(e)}"}]}

    def _tool_get_weather_data(self, state, district):
        try:
            if not os.path.exists(self.weather_data_path):
                return {"isError": True, "content": [{"type": "text", "text": "Weather database not found."}]}

            with open(self.weather_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            state_data = data.get(state)
            if not state_data:
                return {"content": [{"type": "text", "text": f"No weather data found for state {state}."}]}

            district_data = state_data.get(district)
            if not district_data:
                # Return state capital/average or list available
                available = list(state_data.keys())
                return {"content": [{"type": "text", "text": f"Weather data not found for district {district}. Available: {', '.join(available)}."}]}

            return {"content": [{"type": "text", "text": json.dumps(district_data, indent=2)}]}

        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Error: {str(e)}"}]}

    def _tool_save_action_plan(self, filename, content):
        try:
            # Ensure output folder exists. Save to a subfolder "output_plans" under data_dir
            output_dir = os.path.join(self.data_dir, "action_plans")
            os.makedirs(output_dir, exist_ok=True)

            # Sanitize filename
            filename = os.path.basename(filename)
            if not filename.endswith(".md"):
                filename += ".md"

            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "content": [{
                    "type": "text",
                    "text": f"Successfully saved Farm Action Plan to {filepath}."
                }]
            }
        except Exception as e:
            return {"isError": True, "content": [{"type": "text", "text": f"Failed to save action plan: {str(e)}"}]}
