---
name: Continue Project
description: Loop workflow for autonomous project continuation and repair tasks.
---

# Continue Project

This workflow dictates the exact sequence of actions for autonomously continuing development on the AI Karmayogi project without relying on chat history.

## Workflow Execution Loop

Follow these steps strictly:

1. **Read `docs/SESSION_HANDOFF.md`**: Understand the current context, immediate blocker, and specific next task. Do not perform any broad repository discovery unless the handoff explicitly fails.
2. **Read `docs/00_PROJECT_STATE.md`**: Understand what features are verified working, broken, or unverified. Respect the architecture and constraints detailed here.
3. **Read `docs/REPAIR_QUEUE.md`**: Identify the highest-priority unfinished task.
4. **Select Task**: Choose the topmost unchecked task from the P0 list (or P1 if P0 is empty).
5. **Inspect Files**: Inspect ONLY the files explicitly mentioned in the task or the minimal files necessary to execute the task. DO NOT read every source file.
6. **Implement Fix**: Implement the smallest, most targeted correct fix for the selected task. Do not introduce fake data or fallbacks as a substitute for real functionality.
7. **Run Verification**: Run targeted verification (e.g., executing the specific FastAPI route or a targeted Python script).
8. **Handle Failure**: If verification fails, diagnose the actual failure and fix it. Only retry when technically justified. **NEVER** enter repeated blind retry loops.
9. **Handle Success**: If verification passes:
    * Update `docs/REPAIR_QUEUE.md` to check off the completed task.
    * Update `docs/00_PROJECT_STATE.md` to reflect the new state of the verified feature.
    * Update `docs/SESSION_HANDOFF.md` with the newly unblocked state and the *next* concrete task.
    * Update relevant architecture or demo docs if the system flow has fundamentally changed.
10. **Graphify Sync**: If the runtime architecture (files/imports/functions) changed significantly, follow the existing Graphify rules (run `graphify update .`).
11. **Terminate**: Stop execution after completing the current task. Clearly record the next task in the handoff document.

## Strict Rules
* **DO NOT** repeatedly rediscover the repository.
* **DO NOT** perform full repo audits every iteration.
* **DO NOT** ask the user to repeat project context that exists in the documentation.
* **DO NOT** modify credentials or `.env`.
* **DO NOT** run `seed_analytics.py`.
* **DO NOT** silently replace broken real functionality with fake/mock data.
* **DO NOT** classify unverified features as working without proof.
* **DO NOT** install new infrastructure unless explicitly required by the task.
