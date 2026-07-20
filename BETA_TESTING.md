# Beta Testing Guide — AOS

## What You're Giving Them

A working Python application that:
- Runs a GUI showing real-time physiological metrics
- Has background services (pulse, orchestrator, guardian, senses)
- Exposes MCP tools for autonomous operation
- Has 12/12 passing integration tests

## What You're Asking For

30 minutes of their time to:
1. Install dependencies
2. Run the test suite
3. Launch the GUI
4. Try 3-5 MCP tools
5. Report what breaks, confuses, or frustrates them

## What's NOT Expected

- They don't need to understand the biological metaphor
- They don't need to contribute code
- They don't need to use it long-term
- They don't need to give positive feedback

## Installation Steps (Give This Exactly)

```bash
# 1. Clone
git clone <your-repo-url>
cd aos

# 2. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# OR source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r mcp_server/python/requirements.txt

# 4. Run tests
python tests/test_aos_integration.py

# 5. Launch GUI
python mcp_server/python/nexus_gui.py
```

## Task List for Beta Testers

1. **Run the test suite.** Does it pass? If not, what error do you see?
2. **Launch the GUI.** Does it open? What do you see? Is anything broken or confusing?
3. **Check the physiological sidebar.** Can you see energy, hormones, ECG wave?
4. **Try the Sovereign Terminal.** Type `status` and press Enter. What happens?
5. **Try a tool.** Use the MCP server to call `get_energy_status` or `run_immune_patrol`.
6. **Break something.** Try modifying a file in `archives/` while the GUI is running. What happens?

## Feedback Form (Send This After Their Session)

```markdown
## AOS Beta Feedback

1. **Installation:** Did `pip install -r requirements.txt` work? Any errors?
2. **Tests:** Did all 12 tests pass? If not, which ones failed and what was the error?
3. **GUI:** Did `nexus_gui.py` launch? Rate 1-5:
4. **Confusion:** What was the most confusing part?
5. **Bugs:** Did anything crash or behave unexpectedly?
6. **Missing:** What feature would you expect that wasn't there?
7. **Usefulness:** On a scale of 1-5, how useful would this be for your work?
8. **Willingness to contribute:** Would you consider contributing code/docs? (Yes/No/Maybe)
```

## How to Recruit Beta Testers

### CS Friends (Highest Conversion)
- DM: "Hey, I built an open-source agentic OS. Would you spend 20 minutes running the test suite and telling me what breaks? No obligation, just feedback."

### Developer Discord/Twitter Mutuals
- Post in #showcase or #projects: "Built AOS — agentic OS with biological metaphor. Looking for 3 people to beta test. Takes ~20 min. DM me."

### Reddit (r/Python, r/MachineLearning)
- Comment on your own HN/Reddit posts: "Looking for 3 beta testers. DM if interested. Takes 20 min."

### Cold Outreach (Lower Conversion)
- Find Python devs on LinkedIn/Twitter with open DMs
- Keep message short: "Built AOS, looking for beta feedback. 20 min. Free. DM if curious."

## What to Do With Feedback

| Type | Action |
|------|--------|
| Crash / bug | Fix immediately, commit with `[FIX]` tag |
| UX confusion | Add to README FAQ section |
| Feature request | Add to GitHub Issues as `enhancement` |
| "This is cool" | Screenshot + quote for README/social proof |
| "This is useless" | Ask why. The answer is more valuable than praise. |

## Beta Testing Timeline

| Day | Activity |
|-----|----------|
| Day 3 | Recruit 3 beta testers |
| Day 3-4 | They install and test |
| Day 4 | You fix bugs, document findings |
| Day 5 | Publish case study with results |

## Success Metrics for Beta

- 3+ people complete the full test suite
- <3 critical bugs found (crashes, data loss)
- Average feedback rating >3/5
- At least 1 person says "I'd use this"

## Ethical Reminders

- Be transparent: "This is a prototype. I need your honest feedback."
- Make it optional: They can stop anytime
- No data collection: Don't log their personal info
- Share credit: If they find a bug that becomes a feature, credit them publicly
