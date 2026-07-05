# 🌱 CropCare AI - Intelligent Farming Assistant

CropCare AI is a complete, production-ready offline multi-agent farming assistant built for Kaggle's **AI Agents: Intensive Vibe Coding Capstone** under the **Agents for Good** track. It operates entirely on `localhost` with **zero external AI API keys or internet dependencies**, ensuring reliability and cost-efficiency in remote rural farming regions.

Farmers upload a crop leaf image, select their state/district, and describe observed plant symptoms. The system runs an orchestrated multi-agent reasoning chain to detect diseases, check meteorological infection risks, calculate soil N-P-K balances, design watering schedules, pull local APMC market prices, identify eligible government subsidies, and compile a comprehensive **Farm Action Plan** saved directly to the local filesystem.

---

## 📐 System Architecture

The following diagram illustrates how the frontend, coordinator agent, local specialist agents, dynamic skills, and the local JSON-RPC MCP server communicate.

```mermaid
graph TD
    User([Farmer / User]) -->|Upload Image & Select Region| UI[Streamlit Frontend]
    UI -->|Invoke Runner| Coordinator[Coordinator Agent]
    
    subgraph Offline Specialist Agents
        Coordinator -->|1. Analyze Heuristics| DiseaseAgent[Disease Detection Agent]
        Coordinator -->|2. Get Weather Heuristics| WeatherAgent[Weather Agent]
        Coordinator -->|3. Get Treatment| MedicineAgent[Medicine Recommender Agent]
        Coordinator -->|4. Get Fertilizers| FertilizerAgent[Fertilizer Agent]
        Coordinator -->|5. Get Irrigation| IrrigationAgent[Irrigation Agent]
        Coordinator -->|6. Query Market Prices| MarketAgent[Market Price Agent]
        Coordinator -->|7. Query Schemes| GovtAgent[Government Scheme Agent]
    end

    subgraph Agent Skills (Local Files)
        DiseaseAgent -->|Load Instructions| Skill_Disease[skills/disease_detection/SKILL.md]
        WeatherAgent -->|Load Instructions| Skill_Weather[skills/weather_advice/SKILL.md]
        MedicineAgent -->|Load Instructions| Skill_Med[skills/medicine_recommendation/SKILL.md]
        MarketAgent -->|Load Instructions| Skill_Market[skills/market_analysis/SKILL.md]
    end

    subgraph Local MCP Data Provider
        MarketAgent -->|Call MCP Tool| MCPServer[CropCare MCP Server]
        GovtAgent -->|Call MCP Tool| MCPServer
        WeatherAgent -->|Call MCP Tool| MCPServer
        
        MCPServer -->|Read JSON| DB_Market[(Market Prices DB)]
        MCPServer -->|Read JSON| DB_Govt[(Govt Schemes DB)]
        MCPServer -->|Read JSON| DB_Weather[(Weather DB)]
        MCPServer -->|Save File| FileSys[Filesystem / Action Plans]
    end

    Coordinator -->|Generate Final Plan| UI
```

---

## 🏆 Demonstration of 5 Kaggle Key Concepts

### 1. Multi-Agent System (Google ADK Architecture Style)
Orchestration is handled by a central **Coordinator Agent** mimicking the Google Agent Development Kit (ADK) structure. Rather than packing all rules into a single prompt, the coordinator delegates tasks to **7 specialized agents** (Disease Detection, Weather, Medicine, Fertilizer, Irrigation, Market, and Government). This ensures clear separation of concerns, modularity, and high diagnostic resolution.

### 2. Model Context Protocol (MCP) Server
A local JSON-RPC 2.0 stdio-compliant MCP server (`CropMCPServer` in `mcp/crop_mcp_server.py`) handles data requests. The client (`tools/mcp_client.py`) formats messages in JSON-RPC standard method structures (`tools/list` and `tools/call`) to request resources. The MCP server hosts the database queries and filesystem writer tools, simulating process-level RPC separation.

### 3. Agent Skills
Domain-specific instruction modules are located in the `skills/` directory as markdown files (`SKILL.md`). These skills contain YAML metadata and procedural guidelines for the agents (e.g. how the Weather Agent checks relative humidity thresholds or how the Market Advisor analyzes pricing trends). This solves "context rot" by loading knowledge dynamically when the corresponding agent fires.

### 4. Security
- **No Hardcoded Credentials:** The project structure separates data and configuration.
- **Path Traversal Mitigation:** The MCP filesystem tool uses `os.path.basename` to sanitize save-paths, preventing directory traversal attacks.
- **Input Validation:** User-provided state, district, and crop types are verified against validated internal list mappings.

### 5. Deployability
Running 100% offline removes external AI endpoints. The system requires no API keys, has a low CPU/memory footprint, and can run instantly on any local machine (even on old laptops or offline tablets in field stations) using standard Python packages.

---

## 📁 Folder Structure

```
CropCare-AI/
├── requirements.txt            # Python dependencies (Streamlit, Pillow, Pandas)
├── README.md                   # Installation and operational documentation
├── app.py                      # Premium Streamlit Dashboard frontend
├── test_agents.py              # Automated pipeline integration test script
├── .env.example                # Sample environment file
├── data/                       # Offline databases
│   ├── crop_diseases.json      # Symptoms, diagnosis details, and agronomy catalog
│   ├── market_prices.json      # APMC market rates in INR and price trends
│   ├── government_schemes.json # National and state-specific agricultural schemes
│   └── weather_data.json       # Mock district weather variables (Temp, Humidity)
├── mcp/                        # Model Context Protocol layer
│   ├── __init__.py
│   └── crop_mcp_server.py      # Standard JSON-RPC MCP Server
├── skills/                     # Local Agent Skills (Markdown)
│   ├── disease_detection/
│   │   └── SKILL.md
│   ├── weather_advice/
│   │   └── SKILL.md
│   ├── medicine_recommendation/
│   │   └── SKILL.md
│   └── market_analysis/
│       └── SKILL.md
├── tools/                      # MCP Client and Utility functions
│   ├── __init__.py
│   └── mcp_client.py           # Packagers for RPC messages
└── agents/                     # Agent classes
    ├── __init__.py
    ├── base_agent.py           # Base agent class reading SKILL.md files
    ├── coordinator.py          # Pipeline coordinator and layout compiler
    ├── disease_detector.py     # Fuzzy symptom-matching classifier
    ├── weather_advisor.py      # Climate risk analyzer
    ├── medicine_recommender.py # Bio/chemical remedy recommender
    ├── fertilizer_advisor.py   # N-P-K mineral planner
    ├── irrigation_planner.py   # Watering scheduler
    ├── market_advisor.py       # Local pricing economist
    └── government_advisor.py   # Subsidy and scheme finder
```

---

## 🚀 Setup & Installation Instructions

### Prerequisites
Ensure you have **Python 3.8 to 3.13** installed on your system.

### 1. Clone the Codebase
Move into your target workspace directory:
```bash
cd "c:\Users\lenovo\Downloads\capstone project"
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
Create and activate a python environment:
```bash
python -m venv venv
# On Windows (Command Prompt)
venv\Scripts\activate
# On Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```

---

## 🧪 Verification & Local Testing

You can verify the entire multi-agent coordination, local MCP server calls, and file-writing pipeline with the automated test script:
```bash
python test_agents.py
```
This runs a simulated diagnostic run for a Tomato Leaf Mold infection in Nashik, Maharashtra, asserting that:
- The disease detector correctly identifies "Tomato Leaf Mold" from symptom keywords.
- The MCP server correctly provides weather and APMC price entries.
- The coordinator compiles the Action Plan and saves it to `data/action_plans/` on disk.

---

## 🖥️ Running the Streamlit App

Launch the dashboard locally:
```bash
streamlit run app.py
```
This starts the local web server. Open your browser to the URL displayed in the terminal (usually `http://localhost:8501`).

### User Guide:
1. **Choose Parameters:** Select the target Crop (e.g., Tomato, Potato, Wheat, Rice, Cotton).
2. **Select Region:** Choose the State and District. This pulls localized market price and weather profiles.
3. **Upload Image:** Upload a leaf image (JPG/PNG).
4. **Enter Symptoms (Recommended):** Describe the signs (e.g., *"velvety mold on lower surface"*).
5. **Analyze:** Click **Analyze Crop Health** to watch the execution trace live.
6. **Download Action Plan:** Navigate to the "Complete Farm Action Plan" tab to read the report and download the markdown file.
#   C r o p - c a r e - a i  
 #   C r o p - c a r e - a i  
 #   C r o p - c a r e - a i  
 