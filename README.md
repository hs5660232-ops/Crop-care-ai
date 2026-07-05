🌾 CropCare AI
Intelligent Offline Multi-Agent Farming Assistant

🚜 AI-powered crop disease diagnosis, weather analysis, fertilizer planning, irrigation scheduling, market intelligence, and government scheme recommendations — running completely offline.












📖 Overview

CropCare AI is a production-ready offline intelligent farming assistant built for the Kaggle AI Agents Intensive Vibe Coding Capstone (Agents for Good Track).

Unlike cloud-based AI solutions, CropCare AI requires:

❌ No Internet
❌ No OpenAI API
❌ No Gemini API
❌ No HuggingFace API
❌ No External Services

Everything runs locally using lightweight rule-based AI agents and an offline MCP server.

✨ Key Features
Feature	Description
🌿 Disease Detection	Detect plant diseases using symptom matching and image heuristics
🌦 Weather Advisor	Estimates infection risk using local weather profiles
💊 Medicine Recommendation	Suggests organic and chemical treatments
🌱 Fertilizer Planner	Calculates NPK recommendations
💧 Irrigation Planner	Generates crop watering schedule
💰 Market Intelligence	Shows local APMC market prices
🏛 Government Schemes	Finds eligible agriculture schemes
📄 Farm Action Plan	Generates downloadable reports
🏗 Architecture

Complete Offline Multi-Agent Pipeline

Farmer
   │
   ▼
Streamlit UI
   │
   ▼
Coordinator Agent
   │
 ┌─┴─────────────────────────┐
 │ Disease Agent             │
 │ Weather Agent             │
 │ Medicine Agent            │
 │ Fertilizer Agent          │
 │ Irrigation Agent          │
 │ Market Agent              │
 │ Government Agent          │
 └──────────────┬────────────┘
                │
                ▼
      Local MCP Server
                │
        JSON Databases
                │
                ▼
      Farm Action Plan
📸 Screenshots

Add screenshots here

assets/
│
├── home.png
├── diagnosis.png
├── action_plan.png
├── architecture.png

Then

## Home Screen

![Home](assets/home.png)

## Diagnosis

![Diagnosis](assets/diagnosis.png)

## Final Report

![Report](assets/action_plan.png)
🛠 Technology Stack
Layer	Technology
Frontend	Streamlit
Backend	Python
Agents	Offline Rule-Based Agents
RPC	JSON-RPC MCP
Database	JSON
Image Processing	Pillow
Data Analysis	Pandas
Report Generation	Markdown
🚀 Quick Start
git clone https://github.com/username/CropCare-AI.git

cd CropCare-AI

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
📂 Project Structure

(keep your existing tree)

🧪 Testing
python test_agents.py

Expected Output

✔ Disease detected

✔ Weather analyzed

✔ Fertilizer generated

✔ Market price fetched

✔ Govt schemes found

✔ Action Plan saved
🏆 Kaggle Requirements Covered
Requirement	Status
✅ Multi-Agent System	✔
✅ MCP Server	✔
✅ Agent Skills	✔
✅ Security	✔
✅ Offline Deployment	✔
📜 License

MIT License

⭐ Future Improvements
Voice Assistant
Hindi & Regional Language Support
Offline CNN Disease Detection
Satellite Weather Integration
Yield Prediction
Pest Forecasting
Soil Health Analytics
