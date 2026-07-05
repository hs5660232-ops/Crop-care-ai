import os
import glob
from agents.coordinator import CoordinatorAgent

def test_cropcare_pipeline():
    print("==================================================")
    print("[START] STARTING CROPCARE AI INTEGRATION TEST")
    print("==================================================")
    
    # 1. Initialize Coordinator
    coordinator = CoordinatorAgent(data_dir="data")
    print("[OK] Coordinator Agent initialized.")
    
    # 2. Define inputs
    crop = "Tomato"
    state = "Maharashtra"
    district = "Nashik"
    symptoms = "velvety mold on lower surface of leaves with olive-green spots"
    
    print(f"\nParameters:\n- Crop: {crop}\n- Location: {district}, {state}\n- Symptoms: '{symptoms}'")
    
    # 3. Run Analysis Pipeline
    print("\nRunning multi-agent analysis...")
    result = coordinator.run_analysis(
        crop=crop,
        state=state,
        district=district,
        symptoms=symptoms,
        image_provided=True
    )
    
    print("\n[OK] Analysis execution trace completed.")
    print("--------------------------------------------------")
    print("COORDINATOR AGENT LOG:")
    print(result["execution_log"])
    print("--------------------------------------------------")
    
    # 4. Assert and verify outputs
    detected_disease = result["disease_result"]["detected_disease"]
    confidence = result["disease_result"]["confidence"]
    save_status = result["save_status"]
    filename = result["filename"]
    
    print(f"\nResults Verification:")
    print(f"- Detected Disease: {detected_disease} (Expected: Tomato Leaf Mold)")
    print(f"- Confidence Score: {confidence * 100:.1f}%")
    print(f"- Save Status: {save_status}")
    print(f"- Action Plan Filename: {filename}")
    
    assert "leaf mold" in detected_disease.lower(), f"Unexpected disease detected: {detected_disease}"
    assert confidence > 0.8, f"Confidence score too low: {confidence}"
    assert "saved successfully" in save_status.lower(), f"File save failed: {save_status}"
    
    # 5. Check if file exists in data/action_plans/
    saved_file_path = os.path.join("data", "action_plans", filename)
    file_exists = os.path.exists(saved_file_path)
    print(f"- File written to disk: {file_exists} ({saved_file_path})")
    
    assert file_exists, f"Saved plan file not found at {saved_file_path}"
    
    # Read the file to ensure it has content
    with open(saved_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"- Saved plan size: {len(content)} characters.")
    assert len(content) > 500, "Saved action plan is too short or empty."
    
    print("\n==================================================")
    print("[SUCCESS] ALL PIPELINE TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_cropcare_pipeline()
