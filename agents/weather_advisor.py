from agents.base_agent import OfflineAgent
from tools.mcp_client import CropMCPClient

class WeatherAdvisor(OfflineAgent):
    """
    Retrieves weather data via MCP and advises on meteorological conditions affecting crop diseases.
    """
    def __init__(self, mcp_client: CropMCPClient, data_dir="data"):
        super().__init__(name="Weather Advisor", skill_folder="weather_advice", data_dir=data_dir)
        self.mcp_client = mcp_client

    def run(self, context: dict) -> dict:
        """
        Runs weather evaluation.
        Context needs:
          - 'state': Farmer's state.
          - 'district': Farmer's district.
          - 'detected_disease': Disease name.
        """
        state = context.get("state", "").strip()
        district = context.get("district", "").strip()
        disease = context.get("detected_disease", "Unknown").lower()

        if not state or not district:
            return {
                "weather_summary": "Unavailable (Region not specified)",
                "risk_level": "Unknown",
                "advice": "Please select a State and District to receive localized weather-based advice."
            }

        try:
            # Query MCP Server
            weather = self.mcp_client.get_weather_data(state, district)
            
            if "raw_text" in weather and "not found" in weather["raw_text"].lower():
                return {
                    "weather_summary": f"Unavailable data for {district}, {state}.",
                    "risk_level": "Medium",
                    "advice": "Unable to fetch specific weather logs. Maintain standard field ventilation and monitor humidity."
                }

            temp = weather.get("temp_c", 25.0)
            humidity = weather.get("humidity_pct", 50)
            rainfall = weather.get("rainfall_mm", 0.0)
            forecast = weather.get("forecast", "Fair weather")
            risk_index = weather.get("risk_index", "Medium")

            # Formulate specific advice depending on the disease and weather conditions
            advice_points = []
            is_fungal_disease = any(term in disease for term in ["blight", "rust", "mold", "spot", "mildew"])

            if is_fungal_disease and humidity > 70:
                risk_index = "Critical High (Fungal Propagation Risk)"
                advice_points.append(
                    "WARNING: Current relative humidity is extremely high. Fungal pathogens spread rapidly in humid air. Avoid wetting the leaves."
                )
                advice_points.append(
                    "Prune excess branches immediately to optimize air circulation and allow sunshine into the lower crop canopy."
                )
            elif humidity > 70:
                risk_index = "High"
                advice_points.append("High ambient humidity detected. Keep field boundaries clean and avoid over-irrigation.")
            else:
                advice_points.append("Ambient weather is dry, which limits fungal spore transmission. Standard monitoring is recommended.")

            if rainfall > 10.0:
                advice_points.append(
                    f"Rainfall forecast ({rainfall} mm): Do not apply pesticide or fungicide sprays today as the rain will wash away chemical coats. Delay application until foliage is dry."
                )
                advice_points.append("Ensure drainage channels are clear to prevent water accumulation near crop roots.")
            elif forecast and "shower" in forecast.lower() or "rain" in forecast.lower():
                advice_points.append("Expected rainfall: Delay immediate foliar spray applications by 24 hours.")

            if not advice_points:
                advice_points.append("No active weather warnings. Continue standard cultivation schedules.")

            summary = f"Temperature: {temp}°C, Humidity: {humidity}%, Rainfall: {rainfall} mm, Forecast: {forecast}."

            return {
                "weather_summary": summary,
                "risk_level": risk_index,
                "advice": "\n".join(f"- {pt}" for pt in advice_points)
            }

        except Exception as e:
            return {
                "weather_summary": "Offline API Error",
                "risk_level": "Medium",
                "advice": f"Error running weather query via MCP tool: {str(e)}"
            }
