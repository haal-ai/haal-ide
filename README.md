# HAAL IDE

> **⚠️ DEPRECATED**: haal-ide is now deprecated in favor of **[haal-skills](https://github.com/haal-ai/haal-skills)**. The new standard for skills is [Overview - Agent Skills](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/prompt_caching/agent_skills).

**HAAL** (Human AI Assistant Layer) IDE provides seamless integration between humans and AI assistants (for both IDE and some CLI-based agents), enabling better communication and collaboration through intelligent skills, tools, templates and guidance.

## 🏛️ Origin and evolutions

HAAL is a fork and evolution of **AMADEUS™ IT Group's OLAF** (Open Lightweight AI Assistant Framework). 

🔗 **Original Project:** https://github.com/AmadeusITGroup/olaf

It was decided to make this incarnation and evolution of OLAF public, but most of the skills, code, and documentation are from July 2025 and have been used, curated, and augmented since then. 

> **⚠️ Note 08-jan-2026:** This repository may not evolve further if we can standardize on Anthropic's™ Agent Skills format and keep our competencies, collections, and multiple other features.

## 📋 Features

Like OLAF, it works directly with multiple IDE agents agents (e.g., Windsurf™, GitHub™ Copilot Agent, AWS Kiro™ as of January 2026) and is easy to evolve and use without requiring any extensions. It is also easy to adapt to Other IDE of CLI based agentic solutions.


As compared to OLAF v1, it retains and augments:
- OLAF formatted skills concept (and their tools, templates, guidance, and directives)
- OLAF competencies concept - sets of skills 
- Skill discovery and execution using agent chat/conversation 
- A convention for storing all produced outcomes (temporary or for review) 
- A conversation protocol (ASK, PROPOSE-ASK, PROPOSE-CONFIRM-ASK) per skill
- Ability for users to create OLAF formatted skills using an OLAF skill 

**It changes:**
- OLAF skills are self-sufficient and are not defined in competencies manifest 
- OLAF competencies are lighter manifests that just link related skills per user profile (e.g., architect, coder, business analyst, technical writer) or per intent (e.g., redocumenting, migrating)

**It adds:**
- OLAF collections - sets of competencies for easy distribution
- Auto injection of specific context based on skills or user intent
- OLAF agentic skills - specific skills interfacing with local agentic solutions (currently demonstrated with AWS Strands SDK based agents)
- Auto compute of /slash command for those IDE agents that support it (e.g., Windsurf, GitHub Copilot Agent in this repository)

**Advantages:** As this is based solely on using LLMs to select the best skill based on user intent, it does not require using a specific IDE or CLI-based agent.

**Limitation:** It uses its own conventions, prompt format, and skills organization, and cannot be used as-is by CLI or IDE-based agents that commoditize on Agent Skill format (see https://github.com/haal-ai/haal-skills).

## 🚀 Quick Start
 WIP
 
## 🔧 Configuration
 WIP

## 🔗 HAAL AI Ecosystem

See **[haal-skills](https://github.com/haal-ai/haal-skills)** for the active project using Anthropic's™ Agent Skills format.


## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
