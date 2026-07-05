---
name: "Crop Market Analysis"
description: "Analyze market rates and price trends to formulate selling advice for harvested crops."
version: "1.0.0"
---

# Crop Market Analysis Skill

This skill guides the agent in advising farmers when and where to sell their crops to maximize returns.

## Context & Parameters

- `crop`: The crop name.
- `state`: Farmer's state.
- `district`: Farmer's district.
- `apmc_market`: Closest local market name.
- `price_per_quintal`: Price in INR per quintal.
- `trend`: Price direction (Increasing, Stable, Decreasing).

## Instructions

1. Present the current market rate and APMC location retrieved from the MCP server.
2. Evaluate the price trend:
   - **Increasing**: Advise holding a portion of the harvest if storage facilities are available, as prices might rise further.
   - **Decreasing**: Recommend selling soon to avoid further losses, or checking other nearby districts with higher rates.
   - **Stable / MSP**: Advise selling through government purchase centers to guarantee minimum support price (MSP).
3. Include storage and transport recommendations to preserve crop quality during market shifts.
