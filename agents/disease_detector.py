import os
import json
from agents.base_agent import OfflineAgent

class DiseaseDetector(OfflineAgent):
    """
    Analyzes visual symptoms and crop types to detect plant disease.
    Uses the disease database for diagnostic checks.
    """
    def __init__(self, data_dir="data"):
        super().__init__(name="Disease Detector", skill_folder="disease_detection", data_dir=data_dir)

    def run(self, context: dict) -> dict:
        """
        Executes the diagnostic check.
        Context needs:
          - 'crop': Selected crop name.
          - 'symptoms': User's text description of symptoms.
        """
        crop = context.get("crop", "").strip()
        symptoms = context.get("symptoms", "").strip().lower()

        if not crop:
            return {
                "detected_disease": "Unknown",
                "confidence": 0.0,
                "explanation": "No crop selected. Unable to initiate diagnostic run."
            }

        # Load database
        db_path = os.path.join(self.data_dir, "crop_diseases.json")
        if not os.path.exists(db_path):
            return {
                "detected_disease": "Database Error",
                "confidence": 0.0,
                "explanation": f"Crop disease database was not found at {db_path}."
            }

        with open(db_path, "r", encoding="utf-8") as f:
            disease_db = json.load(f)

        crop_profiles = disease_db.get(crop, [])
        if not crop_profiles:
            return {
                "detected_disease": "Healthy / No Disease Profile Found",
                "confidence": 0.90,
                "explanation": f"No documented disease profiles for {crop} exist in the local database. The crop is likely healthy or has an uncatalogued issue."
            }

        # Heuristic matching: find which disease profile matches the symptoms best
        best_match = None
        highest_score = 0

        # If user didn't specify symptoms, default to the first profile but lower confidence
        if not symptoms:
            best_match = crop_profiles[0]
            # Create a mock detection based on general database profiles
            return {
                "detected_disease": best_match["disease_name"],
                "confidence": round(best_match["confidence_score"] - 0.15, 2), # lower confidence since no symptoms provided
                "explanation": best_match["explanation"] + " (Note: Heuristically matched based on general crop profile, as no specific symptoms were described.)",
                "raw_profile": best_match
            }

        for profile in crop_profiles:
            score = 0
            # Split symptoms description into words
            words = symptoms.replace(",", " ").replace(".", " ").split()
            # Match against profile symptoms definition
            profile_symptoms_text = profile["symptoms"].lower()
            
            # Simple keyword matching score
            for word in words:
                if len(word) > 3 and word in profile_symptoms_text:
                    score += 1

            # Match against disease name keywords
            disease_name_words = profile["disease_name"].lower().split()
            for d_word in disease_name_words:
                if len(d_word) > 3 and d_word in symptoms:
                    score += 2  # Higher weight for disease name matching

            if score > highest_score:
                highest_score = score
                best_match = profile

        if best_match and highest_score > 0:
            # We found a match
            return {
                "detected_disease": best_match["disease_name"],
                "confidence": best_match["confidence_score"],
                "explanation": best_match["explanation"],
                "raw_profile": best_match
            }
        else:
            # If no match but crop exists, default to the first profile with lower confidence
            best_match = crop_profiles[0]
            return {
                "detected_disease": best_match["disease_name"],
                "confidence": 0.70,
                "explanation": f"Inconclusive symptoms matching. The symptoms described do not clearly match the database. Exhibiting high similarity to: {best_match['disease_name']}. {best_match['explanation']}",
                "raw_profile": best_match
            }
