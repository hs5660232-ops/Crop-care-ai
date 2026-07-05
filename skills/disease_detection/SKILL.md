---
name: "Crop Disease Detection"
description: "Diagnose crop diseases based on crop type and observed visual symptoms."
version: "1.0.0"
---

# Crop Disease Detection Skill

This skill allows the agent to analyze a crop and its symptoms to detect any agricultural disease.

## Context & Parameters

- `crop_type`: The type of crop (e.g. Tomato, Potato, Wheat, Rice, Cotton).
- `symptoms`: Textual description of visual symptoms on leaves, stem, or fruit.
- `image_provided`: Boolean indicating if a crop image was uploaded.

## Instructions

1. Retrieve the crop profile from the local disease database.
2. If an image is provided, simulate a visual scan of the leaves, stems, and fruits.
3. Compare the observed symptoms with the database entries for the selected crop:
   - Identify the best matching disease (e.g., if "concentric rings" are mentioned for Potato, match "Potato Early Blight").
   - If no symptoms are specified, choose the primary prevalent disease for that crop as a default visual match from the upload.
4. Calculate a diagnostic confidence score based on symptom matching (typically 80% to 98%).
5. Formulate a clear botanical explanation of the disease, how it spreads, and its common names.
6. Format the output as a clean JSON object containing:
   - `detected_disease`: The name of the matched disease.
   - `confidence`: Float between 0.0 and 1.0.
   - `explanation`: Summary of the disease pathology.
