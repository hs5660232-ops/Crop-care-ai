from agents.base_agent import OfflineAgent

class MedicineRecommender(OfflineAgent):
    """
    Formulates treatment recommendations (chemical and biological) for crop diseases.
    """
    def __init__(self, data_dir="data"):
        super().__init__(name="Medicine Recommender", skill_folder="medicine_recommendation", data_dir=data_dir)

    def run(self, context: dict) -> dict:
        """
        Runs treatment lookup.
        Context needs:
          - 'raw_profile': The dictionary containing the matched disease profile from DiseaseDetector.
          - 'detected_disease': The name of the detected disease.
        """
        raw_profile = context.get("raw_profile")
        disease = context.get("detected_disease", "Unknown")

        if not raw_profile or disease == "Unknown":
            return {
                "organic_control": "Apply neem oil (1-2%) to limit insect vector and general fungal activity.",
                "chemical_control": "Consult local extension officer for crop-safe protective fungicides.",
                "application_guidelines": "Prune infected parts and destroy them. Do not compost diseased leaves."
            }

        medicine = raw_profile.get("medicine", {})
        chemical = medicine.get("chemical", "No chemical control documented.")
        biological = medicine.get("biological", "No biological control documented.")

        # Construct specific application instructions
        guidelines = [
            "Always spray early in the morning or late in the evening to prevent crop scorching.",
            "Wear appropriate protective clothing, gloves, and face masks during chemical spray operations.",
            "Maintain a pre-harvest interval (PHI) of at least 7-14 days after applying chemical treatments."
        ]

        if "blight" in disease.lower() or "rust" in disease.lower():
            guidelines.append("Thoroughly spray the undersides of leaves as fungal spores reside there.")
        
        if "curl" in disease.lower() or "virus" in disease.lower():
            guidelines.append("Remove the infected crop immediately if infection is severe, to prevent spread by insect vectors.")

        return {
            "organic_control": biological,
            "chemical_control": chemical,
            "application_guidelines": "\n".join(f"- {pt}" for pt in guidelines)
        }
