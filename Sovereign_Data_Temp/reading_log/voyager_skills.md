# Reading Log: Voyager: An Open-Ended Embodied Agent
**Source**: https://arxiv.org/abs/2305.16291
**Date**: 2026-07-25

## Summary
An open-ended agent in Minecraft that uses a skill library and automatic curriculum for lifelong learning.

## New Points
1. **Executable Skill Library**: Storing skills as **JavaScript code** instead of model weights. This ensures persistence, interpretability, and prevents "catastrophic forgetting."
2. **Automatic Curriculum**: A self-directed goal-setting mechanism that maximizes "Exploration Novelty" by identifying and pursuing new tech-tree milestones autonomously.
3. **Iterative Self-Verification**: Using execution errors (environment feedback) to refine code skills until they work, before committing them to the library.