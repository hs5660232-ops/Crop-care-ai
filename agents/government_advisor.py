from agents.base_agent import OfflineAgent
from tools.mcp_client import CropMCPClient

class GovernmentAdvisor(OfflineAgent):
    """
    Retrieves government agricultural schemes via MCP and advises farmers on financial aid options.
    """
    def __init__(self, mcp_client: CropMCPClient, data_dir="data"):
        super().__init__(name="Government Advisor", skill_folder=None, data_dir=data_dir)
        self.mcp_client = mcp_client

    def run(self, context: dict) -> dict:
        """
        Runs scheme lookup.
        Context needs:
          - 'crop': Crop type.
          - 'state': Farmer's state.
        """
        crop = context.get("crop", "").strip()
        state = context.get("state", "").strip()

        if not crop or not state:
            return {
                "eligible_schemes": []
            }

        try:
            # Query MCP Server
            schemes = self.mcp_client.get_government_schemes(crop, state)
            
            # Simple fallback check
            if not isinstance(schemes, list):
                return {
                    "eligible_schemes": []
                }

            # Return list of eligible schemes
            return {
                "eligible_schemes": schemes
            }

        except Exception as e:
            print(f"Error fetching government schemes: {e}")
            return {
                "eligible_schemes": []
            }
