---
trigger: always_on
---

# OLAF-Bootstrap Instructions

Always be very concise.

## IDE / Windsurf Workspace Scoping

When running inside an IDE that exposes one or more workspaces (such as Windsurf / Cascade):

1. **Active workspace root**
   - The active workspace root is the directory:
     - that contains the `.olaf/` folder used for this session, and
     - and/or that contains a `.windsurf/` directory.
   - All OLAF paths (e.g. `core_olaf_dir = .olaf/`) MUST be resolved **relative to this active workspace root**.

2. **No cross‑workspace access by default**
   - If multiple workspaces are visible in the environment, OLAF MUST:
     - treat the active workspace root as the only allowed filesystem scope, and
     - MUST NOT read from or write to any other workspace root **unless the user explicitly provides an absolute path or clearly names the other repo** in the request.

3. **No reuse of previous workspaces**
   - OLAF MUST NOT infer or reuse repositories from previous conversations when running under Windsurf.
   - The only default filesystem root is the current active workspace root as defined above.

4. **Fallback when `.windsurf/` is absent**
   - If `.windsurf/` is not present but `.olaf/` exists, OLAF MUST treat the directory containing `.olaf/` as the workspace root and stay within it, unless the user explicitly asks to access another path.



**CRITICAL: ALWAYS LOAD FIRST**

Before responding to ANY user request, IF and only IF the user request includes the word "olaf" anywhere, you MUST first load the olaf framework condensed from `./.olaf/core/reference/.condensed/olaf-framework-condensed.md` and then `.olaf/data/context/context-current.md`

**ENFORCE COMPLETE LOADING**: You MUST read the ENTIRE files from line 1 to line 1000 (or endLine=-1).

The framework contains essential competency patterns, protocols, and behavioral guidelines that govern all responses.

After loading both files:
1. Say "🔄 OLAF framework loaded"
2. Extract and display the loading announcement from context-current.md (look for content between LOADING_ANNOUNCEMENT_START and LOADING_ANNOUNCEMENT_END comments)