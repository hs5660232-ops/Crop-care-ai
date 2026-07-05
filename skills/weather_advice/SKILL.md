---
name: "Weather-based Farming Advice"
description: "Analyze weather conditions and forecast to estimate disease spread risk and give preventative warnings."
version: "1.0.0"
---

# Weather-based Farming Advice Skill

This skill helps the agent translate raw meteorological data into actionable farm management advice.

## Context & Parameters

- `temp_c`: Current temperature in Celsius.
- `humidity_pct`: Relative humidity percentage.
- `rainfall_mm`: Rainfall volume.
- `forecast`: Weather forecast text.
- `detected_disease`: The name of the crop disease detected.

## Instructions

1. Check the relative humidity and forecast:
   - High humidity (>70%) and rainfall/drizzle heavily favor fungal spore germination (like Blights and Rusts).
   - High temperatures and dry conditions may restrict fungal spread but can increase insect vector activity (like whiteflies in Cotton).
2. Rate the warning risk level:
   - **Low**: Conditions are dry and stable.
   - **Medium**: High humidity but no immediate rainfall forecast.
   - **High**: Rain, mist, or high humidity coinciding with active fungal infections.
3. Formulate preventative recommendations, such as pruning for airflow, adjusting spray timing, or sheltering plants.
