from agents.base_agent import OfflineAgent

class IrrigationPlanner(OfflineAgent):
    """
    Develops irrigation schedules to prevent disease spread and manage crop water stress.
    """
    def __init__(self, data_dir="data"):
        super().__init__(name="Irrigation Planner", skill_folder=None, data_dir=data_dir)

    def run(self, context: dict) -> dict:
        """
        Plans watering regimes.
        Context needs:
          - 'raw_profile': Matched disease profile.
          - 'weather_data': Output dictionary from WeatherAdvisor.
        """
        raw_profile = context.get("raw_profile")
        weather = context.get("weather_data", {})
        risk_level = weather.get("risk_level", "Medium").lower()

        specific_advice = "Irrigate the soil at the base of the plant early in the morning."
        if raw_profile:
            specific_advice = raw_profile.get("irrigation_advice", specific_advice)

        # Standard heuristics based on weather risk
        if "critical" in risk_level or "high" in risk_level:
            watering_schedule = "Suspend manual irrigation temporarily or reduce watering frequency by 50%. The current wet weather and high humidity provide excess moisture, and waterlogging will speed up root rot and spore replication."
            watering_method = "Switch to ground-level drip irrigation. STRICTLY avoid overhead sprinkler or manual hose irrigation on foliage."
        elif "low" in risk_level:
            watering_schedule = "Maintain normal watering schedule (e.g., once every 3-4 days depending on crop type)."
            watering_method = "Water early in the morning (before 8:00 AM) to ensure any splash water on foliage evaporates quickly during the day."
        else:
            watering_schedule = "Maintain moderate watering schedule. Keep the top soil damp but not soggy."
            watering_method = "Implement drip irrigation or furrow watering."

        return {
            "disease_specific_watering": specific_advice,
            "watering_schedule": watering_schedule,
            "watering_method": watering_method
        }
