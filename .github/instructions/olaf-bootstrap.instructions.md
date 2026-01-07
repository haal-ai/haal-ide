---
description: "OLAF framework bootstrap - loads core framework when 'olaf' command is detected"
applyTo: "**"
---

# OLAF-Bootstrap Instructions

Always be very concise.

**CRITICAL: ALWAYS LOAD FIRST**

Before responding to ANY user request, IF and only IF the user request includes the word "olaf" anywhere, you MUST first load the olaf framework condensed from `./.olaf/core/reference/.condensed/olaf-framework-condensed.md` and then `.olaf/data/context/context-current.md`

**ENFORCE COMPLETE LOADING**: You MUST read the ENTIRE files from line 1 to line 1000 (or endLine=-1).

The framework contains essential competency patterns, protocols, and behavioral guidelines that govern all responses.

After loading both files:
1. Say "🔄 OLAF framework loaded"
2. Extract and display the loading announcement from context-current.md (look for content between LOADING_ANNOUNCEMENT_START and LOADING_ANNOUNCEMENT_END comments)
