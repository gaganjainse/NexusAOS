# Reading Log: I built 10 multiagent systems at enterprise scale
**Source**: https://www.reddit.com/r/AI_Agents/comments/1npg0a9/i_built_10_multiagent_systems_at_enterprise_scale/
**Date**: 2026-07-25

## Summary
Focuses on architectural patterns for large-scale MAS, emphasizing data pipelines and cross-device visibility.

## New Points
1. **Pipeline Offloading**: Moving string manipulation and data cleansing to the database layer (Firestore Enterprise) using pre-GA pipeline functions to save on agent compute/tokens.
2. **Glanceable Agency**: Leveraging Wear OS Tiles and "Ongoing Activities" to provide persistent, non-intrusive visibility for long-running agent tasks.
