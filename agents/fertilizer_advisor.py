from agents.base_agent import OfflineAgent

class FertilizerAdvisor(OfflineAgent):
    """
    Formulates soil fertility and fertilizer adjustments during crop diseases.
    """
    def __init__(self, data_dir="data"):
        super().__init__(name="Fertilizer Advisor", skill_folder=None, data_dir=data_dir)

    def run(self, context: dict) -> dict:
        """
        Adjusts fertilization plans.
        Context needs:
          - 'raw_profile': Matched disease profile.
        """
        raw_profile = context.get("raw_profile")
        disease = context.get("detected_disease", "Unknown")

        if not raw_profile:
            return {
                "general_recommendation": "Avoid fertilizing heavily during active plant infection to reduce crop physiological stress.",
                "npk_adjustment": "Maintain baseline potassium (K) levels to support plant moisture retention and cell structure.",
                "micronutrients": "Apply a spray of secondary micronutrients (Zinc, Boron) to assist leaf regeneration."
            }

        specific_advice = raw_profile.get("fertilizer_advice", "Maintain balanced crop fertilization.")

        # Heuristic rules based on disease names
        npk_advice = "Maintain standard NPK ratios."
        micronutrients = "Apply secondary zinc and boron to support plant recovery."

        if "blight" in disease.lower() or "mildew" in disease.lower() or "mold" in disease.lower():
            npk_advice = "REDUCE Nitrogen (N) application immediately. Excess nitrogen promotes soft, succulent leaf tissue which fungal spores easily penetrate. INCREASE Potassium (K) to thicken leaf cell walls."
        elif "rust" in disease.lower():
            npk_advice = "Ensure adequate Potassium (K) and Phosphorus (P) levels to encourage strong root development and cellular healing."
        elif "curl" in disease.lower() or "virus" in disease.lower():
            npk_advice = "Avoid excess nitrogen. Apply organic compost to improve overall plant vigor."
            micronutrients = "Urgent: Apply Foliar Zinc Sulfate (0.5%) and Borax (0.2%) to help crop withstand viral stress."

        return {
            "general_recommendation": specific_advice,
            "npk_adjustment": npk_advice,
            "micronutrients": micronutrients
        }
