# Reading Log: MetaGPT: Meta Programming for Multi-Agent
**Source**: https://arxiv.org/abs/2308.00352
**Date**: 2026-07-25

## Summary
Introduces SOPs (Standard Operating Procedures) to LLM multi-agent systems to mimic professional "assembly line" workflows.

## New Points
1. **SOP Prompt Encoding**: Encoding professional SOPs directly into prompt sequences to ensure agents follow structured verification steps for intermediate results.
2. **Cascading Hallucination Mitigation**: By requiring specialized agents to verify the output of previous agents before proceeding, it prevents the propagation of errors common in free-form "chained" LLM conversations.