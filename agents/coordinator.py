import os
from datetime import datetime
from tools.mcp_client import CropMCPClient
from agents.disease_detector import DiseaseDetector
from agents.weather_advisor import WeatherAdvisor
from agents.medicine_recommender import MedicineRecommender
from agents.fertilizer_advisor import FertilizerAdvisor
from agents.irrigation_planner import IrrigationPlanner
from agents.market_advisor import MarketAdvisor
from agents.government_advisor import GovernmentAdvisor

class CoordinatorAgent:
    """
    Coordinator Agent that orchestrates all specialist agents to generate a complete Farm Action Plan.
    Saves the plan to the local filesystem using the MCP server.
    """
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.mcp_client = CropMCPClient(data_dir=data_dir)
        
        # Instantiate all specialist agents
        self.disease_detector = DiseaseDetector(data_dir=data_dir)
        self.weather_advisor = WeatherAdvisor(mcp_client=self.mcp_client, data_dir=data_dir)
        self.medicine_recommender = MedicineRecommender(data_dir=data_dir)
        self.fertilizer_advisor = FertilizerAdvisor(data_dir=data_dir)
        self.irrigation_planner = IrrigationPlanner(data_dir=data_dir)
        self.market_advisor = MarketAdvisor(mcp_client=self.mcp_client, data_dir=data_dir)
        self.government_advisor = GovernmentAdvisor(mcp_client=self.mcp_client, data_dir=data_dir)

    def run_analysis(self, crop: str, state: str, district: str, symptoms: str, image_provided: bool = False) -> dict:
        """
        Executes the multi-agent analysis pipeline sequentially.
        """
        execution_log = []
        
        # 1. Disease Detection
        execution_log.append("Starting Disease Detection Agent...")
        disease_context = {"crop": crop, "symptoms": symptoms, "image_provided": image_provided}
        disease_res = self.disease_detector.run(disease_context)
        detected_disease = disease_res.get("detected_disease", "Unknown")
        confidence = disease_res.get("confidence", 0.0)
        explanation = disease_res.get("explanation", "")
        raw_profile = disease_res.get("raw_profile")
        execution_log.append(f"Disease Detection Agent completed: Detected '{detected_disease}' with {confidence*100}% confidence.")

        # 2. Weather Advice
        execution_log.append("Starting Weather Agent...")
        weather_context = {
            "state": state,
            "district": district,
            "detected_disease": detected_disease
        }
        weather_res = self.weather_advisor.run(weather_context)
        execution_log.append("Weather Agent completed analysis.")

        # 3. Treatment & Medicine Recommendation
        execution_log.append("Starting Medicine Recommendation Agent...")
        medicine_context = {
            "detected_disease": detected_disease,
            "raw_profile": raw_profile
        }
        medicine_res = self.medicine_recommender.run(medicine_context)
        execution_log.append("Medicine Recommendation Agent completed.")

        # 4. Fertilizer Recommendation
        execution_log.append("Starting Fertilizer Agent...")
        fertilizer_context = {
            "detected_disease": detected_disease,
            "raw_profile": raw_profile
        }
        fertilizer_res = self.fertilizer_advisor.run(fertilizer_context)
        execution_log.append("Fertilizer Agent completed.")

        # 5. Irrigation Recommendation
        execution_log.append("Starting Irrigation Planner Agent...")
        irrigation_context = {
            "raw_profile": raw_profile,
            "weather_data": weather_res
        }
        irrigation_res = self.irrigation_planner.run(irrigation_context)
        execution_log.append("Irrigation Planner Agent completed.")

        # 6. Market Prices
        execution_log.append("Starting Market Price Agent...")
        market_context = {
            "crop": crop,
            "state": state,
            "district": district
        }
        market_res = self.market_advisor.run(market_context)
        execution_log.append("Market Price Agent completed.")

        # 7. Government Schemes
        execution_log.append("Starting Government Scheme Agent...")
        govt_context = {
            "crop": crop,
            "state": state
        }
        govt_res = self.government_advisor.run(govt_context)
        execution_log.append("Government Scheme Agent completed.")

        # Compile final plan content
        execution_log.append("Compiling Farm Action Plan...")
        action_plan_md = self._generate_markdown_plan(
            crop, state, district, disease_res, weather_res, medicine_res, 
            fertilizer_res, irrigation_res, market_res, govt_res
        )

        # Save the plan to the filesystem via the MCP client
        execution_log.append("Saving Farm Action Plan to filesystem via MCP tool...")
        filename = f"action_plan_{crop.lower()}_{district.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        save_status = "Not Saved"
        try:
            save_msg = self.mcp_client.save_action_plan(filename, action_plan_md)
            save_status = "Saved Successfully"
            execution_log.append(f"MCP server response: {save_msg}")
        except Exception as e:
            save_status = f"Failed to Save: {e}"
            execution_log.append(f"MCP server save error: {e}")

        return {
            "crop": crop,
            "state": state,
            "district": district,
            "disease_result": disease_res,
            "weather_result": weather_res,
            "medicine_result": medicine_res,
            "fertilizer_result": fertilizer_res,
            "irrigation_result": irrigation_res,
            "market_result": market_res,
            "government_result": govt_res,
            "action_plan_markdown": action_plan_md,
            "execution_log": "\n".join(f"[{datetime.now().strftime('%H:%M:%S')}] {line}" for line in execution_log),
            "save_status": save_status,
            "filename": filename
        }

    def _generate_markdown_plan(self, crop, state, district, disease_res, weather_res, medicine_res, fertilizer_res, irrigation_res, market_res, govt_res) -> str:
        """
        Assembles all agent outputs into a premium Markdown action plan.
        """
        disease_name = disease_res.get("detected_disease", "Unknown")
        confidence = disease_res.get("confidence", 0.0) * 100
        explanation = disease_res.get("explanation", "")

        weather_summary = weather_res.get("weather_summary", "N/A")
        weather_risk = weather_res.get("risk_level", "Medium")
        weather_advice = weather_res.get("advice", "")

        organic_ctrl = medicine_res.get("organic_control", "")
        chemical_ctrl = medicine_res.get("chemical_control", "")
        med_guidelines = medicine_res.get("application_guidelines", "")

        fert_general = fertilizer_res.get("general_recommendation", "")
        fert_npk = fertilizer_res.get("npk_adjustment", "")
        fert_micro = fertilizer_res.get("micronutrients", "")

        irrig_disease = irrigation_res.get("disease_specific_watering", "")
        irrig_sched = irrigation_res.get("watering_schedule", "")
        irrig_method = irrigation_res.get("watering_method", "")

        market_details = market_res.get("market_details", "")
        market_advice = market_res.get("selling_advice", "")

        schemes = govt_res.get("eligible_schemes", [])
        schemes_md = ""
        if schemes:
            for s in schemes:
                schemes_md += f"#### **{s['scheme_name']}** ({s['scope']})\n"
                schemes_md += f"- **Benefits:** {s['benefits']}\n"
                schemes_md += f"- **Eligibility:** {s['eligibility']}\n\n"
        else:
            schemes_md = "_No specific government subsidies or schemes matched for this selection._\n"

        plan = f"""# CROPCARE AI - FARM ACTION PLAN
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Location:** {district}, {state} | **Target Crop:** {crop}

---

## 🔬 Section 1: Disease Diagnosis & Pathology
*   **Detected Disease:** `{disease_name}`
*   **Confidence Score:** `{confidence:.1f}%`
*   **Pathology Explanation:**  
    {explanation}

---

## 🌤️ Section 2: Meteorological Conditions & Spore Transmission Risk
*   **Weather Conditions:** {weather_summary}
*   **Disease Transmission Risk Level:** `{weather_risk}`
*   **Weather-Based Warnings & Airflow Controls:**  
{weather_advice}

---

## 💊 Section 3: Integrated Pest & Disease Treatment Guidelines
### 🌿 Organic & Biological Control (Recommended)
{organic_ctrl}

### 🧪 Chemical Control (For Severe Infection)
{chemical_ctrl}

### ⚠️ Application & Safety Guidelines
{med_guidelines}

---

## 🧪 Section 4: Soil Health & Fertilizer Adjustments
*   **Primary Adjustment:** {fert_general}
*   **N-P-K Ratio Adjustments:** {fert_npk}
*   **Micronutrients & Vigor Boosters:** {fert_micro}

---

## 💧 Section 5: Water Management & Irrigation Schedule
*   **Disease Prevention Advice:** {irrig_disease}
*   **Irrigation Cycle:** {irrig_sched}
*   **Watering Method:** {irrig_method}

---

## 📈 Section 6: Market Economics & Financial Aids
### 🏢 Local Wholesale Market Pricing (APMC)
{market_details}
*   **Selling Advice:** {market_advice}

### 🏛️ Eligible Government Schemes & Subsidies
{schemes_md}
---
**Disclaimer:** *CropCare AI is a local decision-support tool. Farmers are advised to verify safety guidelines and local pesticide regulations prior to chemical application.*
"""
        return plan
