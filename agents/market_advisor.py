from agents.base_agent import OfflineAgent
from tools.mcp_client import CropMCPClient

class MarketAdvisor(OfflineAgent):
    """
    Retrieves market prices via MCP and advises farmers on crop sales and pricing.
    """
    def __init__(self, mcp_client: CropMCPClient, data_dir="data"):
        super().__init__(name="Market Advisor", skill_folder="market_analysis", data_dir=data_dir)
        self.mcp_client = mcp_client

    def run(self, context: dict) -> dict:
        """
        Runs market analysis.
        Context needs:
          - 'crop': Crop type.
          - 'state': Farmer's state.
          - 'district': Farmer's district.
        """
        crop = context.get("crop", "").strip()
        state = context.get("state", "").strip()
        district = context.get("district", "").strip()

        if not crop or not state or not district:
            return {
                "market_details": "No crop/location details selected.",
                "price_trend": "Unknown",
                "selling_advice": "Please select crop and district to fetch local market prices."
            }

        try:
            # Query MCP Server
            prices = self.mcp_client.get_market_prices(crop, state, district)
            
            if "raw_text" in prices and "no market" in prices["raw_text"].lower():
                return {
                    "market_details": f"Market data unavailable for {crop} in {district}, {state}.",
                    "price_trend": "Inconclusive",
                    "selling_advice": "No active APMC pricing registered. Check nearest alternative wholesale market or sell through local cooperatives."
                }

            apmc = prices.get("apmc_market", "Local Market")
            price = prices.get("price_per_quintal", 0)
            trend = prices.get("trend", "Stable")
            last_updated = prices.get("last_updated", "N/A")

            # Formulate selling advice based on trends
            if trend.lower() == "increasing":
                advice = (
                    f"Market prices at {apmc} are currently INCREASING. If you have dry storage structures available, "
                    f"consider holding back 40-50% of your harvest for 2-3 weeks to fetch premium rates."
                )
            elif trend.lower() == "decreasing":
                advice = (
                    f"Market prices at {apmc} are DECREASING. It is recommended to sell your mature crop immediately "
                    f"to minimize losses, or explore transport to adjacent districts."
                )
            elif "msp" in trend.lower():
                advice = (
                    f"The price at {apmc} is pegged to the Government Minimum Support Price (MSP). "
                    f"Register at your local government purchase center to ensure you receive the full MSP rate of INR {price}/quintal."
                )
            else:
                advice = (
                    f"Prices at {apmc} are STABLE. Proceed with harvesting as per your operational schedule "
                    f"and sell at the current rate of INR {price}/quintal."
                )

            return {
                "market_details": f"APMC Market: {apmc} | Current Rate: INR {price}/quintal (Last updated: {last_updated})",
                "price_trend": trend,
                "selling_advice": advice
            }

        except Exception as e:
            return {
                "market_details": "Offline Query Failure",
                "price_trend": "Unknown",
                "selling_advice": f"Could not fetch market details via MCP tool: {str(e)}"
            }
