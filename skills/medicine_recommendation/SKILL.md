---
name: "Agricultural Medicine Recommendation"
description: "Recommend chemical and biological treatment plans for specific crop diseases."
version: "1.0.0"
---

# Agricultural Medicine Recommendation Skill

This skill guides the agent in choosing safe and effective remedies to treat plant pathogens.

## Context & Parameters

- `detected_disease`: The name of the crop disease detected.
- `severity`: Estimate of disease severity (e.g. Mild, Moderate, Severe).

## Instructions

1. Retrieve treatment profiles from the disease catalog.
2. Structure the recommendation into two main treatment paths:
   - **Biological/Organic Control**: Using bio-agents (like Bacillus subtilis, Pseudomonas, Neem oil, or Trichoderma) to manage the pathogen naturally, which is preferred for early or mild infections.
   - **Chemical Control**: Recommending specific active ingredients (e.g., Mancozeb, Metalaxyl, Chlorothalonil) for moderate to severe cases, along with application safety rules.
3. Include dosage guidance or application best practices (e.g., spray in the morning, wear protective gear, do not spray before rain).
