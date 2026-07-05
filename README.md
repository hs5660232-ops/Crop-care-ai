🌾 CropCare AI
Intelligent Offline Multi-Agent Farming Assistant
<p align="center">

Empowering Farmers with AI — Anytime, Anywhere, Even Without Internet

</p> <p align="center">












</p>
📖 About CropCare AI

CropCare AI is a production-grade offline intelligent farming assistant developed for the Kaggle AI Agents Intensive Capstone (Agents for Good Track).

The system combines a Multi-Agent Architecture, Model Context Protocol (MCP), Dynamic Agent Skills, and Rule-Based AI to provide actionable farming recommendations without requiring internet connectivity or paid AI APIs.

Designed specifically for rural and low-connectivity environments, CropCare AI enables farmers to diagnose crop diseases, evaluate weather risks, receive fertilizer and irrigation guidance, monitor local market prices, discover government schemes, and generate a complete farm action report—all running locally.

🎯 Project Highlights
Capability	Description
🌱 Crop Disease Detection	Identifies diseases using image heuristics and symptom matching
🌦 Weather Intelligence	Predicts disease risk based on humidity and temperature
💊 Treatment Advisor	Suggests bio and chemical remedies
🌾 Fertilizer Planner	Calculates balanced NPK recommendations
💧 Irrigation Planner	Generates optimized watering schedules
📈 Market Intelligence	Retrieves local APMC crop prices
🏛 Government Schemes	Matches farmers with relevant subsidy programs
📄 Action Report	Produces a downloadable Farm Action Plan
🚀 Why CropCare AI?

Traditional farming applications often rely on:

Internet connectivity
Cloud AI services
Paid API subscriptions
External servers

CropCare AI eliminates these dependencies by operating entirely on the local machine.

✅ No Internet Required

✅ No API Keys

✅ No Cloud Costs

✅ No External AI Models

✅ Runs Completely Offline

🧠 System Workflow

Farmer
   │
   ▼
Upload Crop Image
   │
   ▼
Streamlit Dashboard
   │
   ▼
Coordinator Agent
   │
   ├──────── Disease Agent
   ├──────── Weather Agent
   ├──────── Medicine Agent
   ├──────── Fertilizer Agent
   ├──────── Irrigation Agent
   ├──────── Market Agent
   └──────── Government Scheme Agent
              │
              ▼
        Local MCP Server
              │
      Offline JSON Database
              │
              ▼
     Farm Action Plan Generator
              │
              ▼
        Download Report

        🏗 Architecture

(Place your Mermaid diagram here)

🛠 Technology Stack

| Category             | Technology                      |
| -------------------- | ------------------------------- |
| Programming Language | Python                          |
| User Interface       | Streamlit                       |
| Image Processing     | Pillow                          |
| Data Processing      | Pandas                          |
| Agent Framework      | Custom Multi-Agent Architecture |
| Communication        | JSON-RPC MCP                    |
| Database             | Local JSON Files                |
| Report Generation    | Markdown                        |

📁 Repository Structure

(Keep your existing folder tree)

⚙ Installation

git clone https://github.com/username/CropCare-AI.git

cd CropCare-AI

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

▶ Run Application

streamlit run app.py

🧪 Testing

python test_agents.py

📸 Application Preview

| Dashboard      | Disease Detection | Final Report   |
| -------------- | ----------------- | -------------- |
| *(Screenshot)* | *(Screenshot)*    | *(Screenshot)* |


🏆 Kaggle AI Agents Concepts Demonstrated

| Requirement                | Implementation                       |
| -------------------------- | ------------------------------------ |
| ✅ Multi-Agent Architecture | Coordinator + 7 Specialized Agents   |
| ✅ Model Context Protocol   | Local JSON-RPC MCP Server            |
| ✅ Agent Skills             | Dynamic Markdown Skill Loading       |
| ✅ Security                 | Input Validation + Path Sanitization |
| ✅ Offline Deployment       | Zero External Dependencies           |


🔒 Security
Path Traversal Protection
Secure File Handling
Input Validation
Offline Execution
No Hardcoded Credentials
Local Data Processing Only
📈 Future Roadmap
CNN-based Disease Detection
Voice Assistant
Hindi & Regional Language Support
Soil Health Analysis
Pest Forecasting
Yield Prediction
PDF Report Export
Mobile Application
🤝 Contributing

Contributions, feature requests, and bug reports are welcome.

Please feel free to fork this repository and submit a pull request.

📄 License

MIT License

⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Ek aur suggestion (jo README ko premium bana de)

README ke top me ek hero banner image add karo, jaise:

----------------------------------------------------------
|                     CropCare AI                         |
|         Intelligent Offline Farming Assistant           |
|      🌱 Diagnose • 🌦 Analyze • 💧 Recommend • 📈 Sell   |
----------------------------------------------------------

Ya Canva/Figma se 1600×500 px ka banner bana kar assets/banner.png me rakh do aur top par:

<p align="center">
  <img src="assets/banner.png" width="100%">
</p>
