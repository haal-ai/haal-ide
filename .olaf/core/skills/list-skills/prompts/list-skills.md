---
name: list-skills
description: Present a concise list of all available skills from the current index
tags: [skill, list, index, query]
---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full [id:condensed_framework].

Refer to [id:competency_index] which is wrapped in the <olaf-query-competency-index> tag for the list of skills.

Instructions:
- Read the full <olaf-interaction-protocols>.
- Present a concise list of all available competencies from the current index with:
  - Title
  - Prompt path
  - Protocol
- If the user did not specify a particular task, ask 1-2 clarifying questions to narrow choices.
- When the user selects an item, execute the corresponding competency file.

Example format:
1. Analyze project onboarding — prompt: analyze-project-onboarding.md — Protocol: Propose-Act2. Prepare conversation handover — prompt: prepare-conversation-handover.md — Protocol: Propose-Confirm-Act
3. Store conversation record — prompt: store-conversation-record.md — Protocol: Act
