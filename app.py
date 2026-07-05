import streamlit as st
import os
import time
import pandas as pd
from PIL import Image
from agents.coordinator import CoordinatorAgent

# Set page configuration with a modern look
st.set_page_config(
    page_title="CropCare AI - Intelligent Farming Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Layout Styling */
    .main {
        background-color: #f7f9fb;
    }
    
    /* Header Card */
    .header-container {
        background: linear-gradient(135deg, #1e5631 0%, #4c9a2a 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
        top: -100px;
        right: -100px;
    }
    
    /* Card Styles */
    .metric-card {
        background-color: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        border: 1px solid #eef2f6;
        margin-bottom: 1.5rem;
    }
    
    .status-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        text-align: center;
    }
    
    .status-high {
        background-color: #ffeef0;
        color: #ff3b30;
        border: 1px solid #ffd1d6;
    }
    
    .status-medium {
        background-color: #fff9e6;
        color: #ff9500;
        border: 1px solid #ffe8b3;
    }
    
    .status-low {
        background-color: #e6f6ec;
        color: #34c759;
        border: 1px solid #b3e6c3;
    }
    
    /* Button Customization */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #1e5631 0%, #4c9a2a 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border-radius: 10px;
        border: none;
        width: 100%;
        box-shadow: 0 5px 15px rgba(30,86,49,0.2);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(30,86,49,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Coordinator Agent
coordinator = CoordinatorAgent(data_dir="data")

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/color/96/sprout.png", width=70)
st.sidebar.title("CropCare AI Panel")
st.sidebar.markdown("---")

st.sidebar.subheader("📍 Crop & Location Selectors")
crop_list = ["Tomato", "Potato", "Wheat", "Rice", "Cotton"]
selected_crop = st.sidebar.selectbox("Select Crop Type", crop_list, index=0)

state_districts = {
    "Maharashtra": ["Pune", "Nashik", "Nagpur"],
    "Uttar Pradesh": ["Lucknow", "Agra", "Varanasi"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
    "Karnataka": ["Bengaluru", "Mysore", "Belagavi"],
    "Tamil Nadu": ["Coimbatore", "Madurai", "Trichy"]
}
selected_state = st.sidebar.selectbox("Select State", list(state_districts.keys()), index=0)
selected_district = st.sidebar.selectbox("Select District", state_districts[selected_state], index=0)

st.sidebar.subheader("📸 Crop Image Upload")
uploaded_file = st.sidebar.file_uploader("Upload leaf or plant image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Uploaded Crop Image", use_container_width=True)

st.sidebar.subheader("📝 Leaf Symptoms (Optional)")
symptoms_input = st.sidebar.text_area(
    "Describe symptoms (e.g. brown rings, white powder, curling)",
    placeholder="Describe what you see on leaves or stems..."
)

st.sidebar.markdown("---")
analyze_button = st.sidebar.button("🔍 Analyze Crop Health")

# Main Page Header
st.markdown("""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700; color: white;">🌱 CropCare AI Dashboard</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Multi-Agent Intelligent Farming Decision-Support System (100% Offline)</p>
</div>
""", unsafe_allow_html=True)

# Main App Logic
if analyze_button:
    st.markdown("### 🛠️ Agent Execution Sequence & Live Handshakes")
    
    # Simulate agent live log loading
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = [
        ("Disease Detection Agent: scanning image and symptom patterns...", 20),
        ("Weather Agent: retrieving microclimate logs from MCP server...", 40),
        ("Medicine Recommender Agent: retrieving biological and chemical remedies...", 60),
        ("Fertilizer Agent: calculating N-P-K adjustments...", 75),
        ("Irrigation Planner Agent: generating watering cycles...", 90),
        ("Market Price & Government Scheme Agents: loading wholesale pricing and subsidies...", 100)
    ]
    
    for i, (msg, percentage) in enumerate(stages):
        status_text.info(f"🤖 {msg}")
        progress_bar.progress(percentage)
        time.sleep(0.4)
        
    status_text.success("🎉 Multi-agent analysis complete! Farm Action Plan compiled.")
    
    # Run the pipeline
    image_provided = uploaded_file is not None
    result = coordinator.run_analysis(
        crop=selected_crop,
        state=selected_state,
        district=selected_district,
        symptoms=symptoms_input,
        image_provided=image_provided
    )
    
    # Destructure results
    disease = result["disease_result"]
    weather = result["weather_result"]
    medicine = result["medicine_result"]
    fertilizer = result["fertilizer_result"]
    irrigation = result["irrigation_result"]
    market = result["market_result"]
    govt = result["government_result"]
    
    st.markdown("---")
    
    # Layout Grid: Visual Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0; color:#1e5631;">🔬 Diagnosis</h3>
            <p style="margin-bottom:0.2rem; font-weight:600;">Detected Disease:</p>
            <p style="font-size:1.4rem; font-weight:700; color:#c0392b; margin-top:0;">{disease['detected_disease']}</p>
            <p style="margin-bottom:0.2rem; font-weight:600;">Confidence Score:</p>
            <p style="font-size:1.2rem; font-weight:600; color:#555; margin-top:0;">{disease['confidence']*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        risk_class = "status-low"
        risk_level = weather["risk_level"]
        if "high" in risk_level.lower() or "critical" in risk_level.lower():
            risk_class = "status-high"
        elif "medium" in risk_level.lower():
            risk_class = "status-medium"
            
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0; color:#1e5631;">🌤️ Weather & Risk</h3>
            <p style="margin-bottom:0.2rem; font-weight:600;">Condition Summary:</p>
            <p style="font-size:0.95rem; color:#444; margin-top:0;">{weather['weather_summary']}</p>
            <p style="margin-bottom:0.4rem; font-weight:600;">Outbreak Risk:</p>
            <span class="status-pill {risk_class}">{risk_level}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin-top:0; color:#1e5631;">📈 Market Price</h3>
            <p style="margin-bottom:0.2rem; font-weight:600;">APMC Wholesale Price:</p>
            <p style="font-size:0.95rem; color:#444; margin-top:0;">{market['market_details']}</p>
            <p style="margin-bottom:0.2rem; font-weight:600;">Price Trend:</p>
            <p style="font-size:1.1rem; font-weight:700; color:#2e7d32; margin-top:0;">{market['price_trend']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Analysis Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💊 Treatment & Remedies", 
        "🌾 Agronomic Advice", 
        "🏢 Market & Economics", 
        "📋 Complete Farm Action Plan",
        "⚙️ System Logs"
    ])
    
    with tab1:
        col_med1, col_med2 = st.columns(2)
        with col_med1:
            st.subheader("🌿 Organic & Biological Control")
            st.success(medicine["organic_control"])
        with col_med2:
            st.subheader("🧪 Chemical Control")
            st.warning(medicine["chemical_control"])
            
        st.subheader("⚠️ Application & Safety Guidelines")
        st.info(medicine["application_guidelines"])
        
    with tab2:
        col_agr1, col_agr2 = st.columns(2)
        with col_agr1:
            st.subheader("🧪 Soil Health & Fertilization Adjustments")
            st.write(f"**Adjustments:** {fertilizer['general_recommendation']}")
            st.write(f"**NPK Balancing:** {fertilizer['npk_adjustment']}")
            st.write(f"**Vigor Boosters:** {fertilizer['micronutrients']}")
        with col_agr2:
            st.subheader("💧 Irrigation Planning")
            st.write(f"**Disease Advice:** {irrigation['disease_specific_watering']}")
            st.write(f"**Watering Cycle:** {irrigation['watering_schedule']}")
            st.write(f"**Method:** {irrigation['watering_method']}")
            
    with tab3:
        st.subheader("🏢 Selling Recommendations")
        st.info(market["selling_advice"])
        
        st.subheader("🏛️ Eligible Government Schemes & Subsidies")
        eligible_schemes = govt.get("eligible_schemes", [])
        if eligible_schemes:
            for s in eligible_schemes:
                with st.expander(f"📌 {s['scheme_name']} ({s['scope']})"):
                    st.write(f"**Benefits:** {s['benefits']}")
                    st.write(f"**Eligibility:** {s['eligibility']}")
        else:
            st.write("_No schemes found for this selection._")
            
    with tab4:
        st.markdown(f"**Save Status:** `📁 {result['save_status']} (Saved as data/action_plans/{result['filename']})`")
        st.markdown("---")
        st.markdown(result["action_plan_markdown"])
        
        # Download button
        st.download_button(
            label="💾 Download Farm Action Plan (Markdown)",
            data=result["action_plan_markdown"],
            file_name=result["filename"],
            mime="text/markdown"
        )
        
    with tab5:
        st.subheader("🤖 Coordinator Execution Trace")
        st.code(result["execution_log"], language="text")

else:
    # Empty State Display
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background-color: white; border-radius: 16px; border: 1px dashed #c2cfd6; margin-bottom: 2rem;">
        <img src="https://img.icons8.com/color/144/sprout.png" width="100" style="margin-bottom: 1.5rem;" />
        <h2 style="color: #2c3e50; font-weight: 600; margin-bottom: 0.5rem;">Begin Crop Analysis</h2>
        <p style="color: #7f8c8d; font-size: 1.1rem; max-width: 600px; margin: 0 auto 1.5rem auto;">
            Please select the target crop, your state, and district in the left panel. Upload an image of the plant leaf and click "Analyze Crop Health" to invoke the coordinator and start the specialist agents.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature explanation grid
    st.markdown("### How CropCare AI Works (Multi-Agent Coordination)")
    col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)
    
    with col_feat1:
        st.markdown("""
        <div style="background-color: white; padding: 1.5rem; border-radius: 12px; height: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); border: 1px solid #eef2f6;">
            <h4 style="color:#1e5631; margin-top:0;">🔍 1. Image Diagnosis</h4>
            <p style="font-size:0.9rem; color:#666;">The Disease Detection Agent scans visual symptoms and isolates pathogens using a local offline catalog.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_feat2:
        st.markdown("""
        <div style="background-color: white; padding: 1.5rem; border-radius: 12px; height: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); border: 1px solid #eef2f6;">
            <h4 style="color:#1e5631; margin-top:0;">🌦️ 2. Weather Assessment</h4>
            <p style="font-size:0.9rem; color:#666;">The Weather Agent queries the MCP tool for district climate conditions, warning of humidity spikes that favor disease spread.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_feat3:
        st.markdown("""
        <div style="background-color: white; padding: 1.5rem; border-radius: 12px; height: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); border: 1px solid #eef2f6;">
            <h4 style="color:#1e5631; margin-top:0;">🧪 3. Treatment Planning</h4>
            <p style="font-size:0.9rem; color:#666;">The Medicine, Fertilizer, and Irrigation agents design a customized botanical and chemical recovery plan.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_feat4:
        st.markdown("""
        <div style="background-color: white; padding: 1.5rem; border-radius: 12px; height: 180px; box-shadow: 0 4px 10px rgba(0,0,0,0.01); border: 1px solid #eef2f6;">
            <h4 style="color:#1e5631; margin-top:0;">📈 4. Economics & Aids</h4>
            <p style="font-size:0.9rem; color:#666;">Market and Government agents find pricing and subsidies from local datasets using MCP tools, saving plans to the filesystem.</p>
        </div>
        """, unsafe_allow_html=True)
