---

name: create-decision-record

description: Create a new decision record following the standard template and update related indexes.

tags: [documentation, decision-making, governance]

---

CRITICAL: Ensure the OLAF condensed framework is loaded and applied: <olaf-work-instructions>, <olaf-framework-validation>. If not loaded, read the full [id:condensed_framework].

CRITICAL: Skill-local resource resolution: if this prompt references `templates/...`, `kb/...`, `docs/...`, `tools/...`, or `scripts/...`, you MUST search for and resolve those paths within THIS SAME SKILL directory. Concretely, resolve them relative to this skill root directory (the parent folder of `prompts/`).

## Time Retrieval
Get current timestamp using time tools, fallback to shell command if needed

## Input Parameters

**IMPORTANT**: When you don't have entries provided, ask the USER to provide them.
- **title**: string - Concise description of the decision
- **type**: enum[Architecture,Project,Business,Functional,People,Technical,Security,Other] - Type of decision
- **status**: enum[Proposed,Accepted,Replaced,Superseded] - (Optional) Decision status (default: Proposed)
- **context**: string - Background and problem statement
- **drivers**: string - Key factors influencing the decision
- **options**: string - Options considered with pros and cons
- **decision**: string - (Optional) Selected option if already determined
- **decision_makers**: string - Individuals responsible for the decision
- **stakeholders**: string - Affected parties and stakeholders

## Process
1. **Record Creation**:
   - Generate unique ID (DR-YYYYMMDD-NN)
   - Create file in `[id:decision_records_dir]`
   - Populate using `templates/project-manager/decision-record-template.md`
2. **Documentation Updates**:
   - Add entry to `[id:decision_records_dir]decision-records-register.md`
   - Update relevant indexes
   - Create changelog entry
3. **Validation**:
   - Verify all required fields
   - Check for similar decisions
   - Ensure proper formatting

## Output/Result Format

Use `templates/project-manager/decision-record-template.md` to structure the decision record:
- Follow the template's sections for consistency
- Create file: `[id:decision_records_dir]YYYYMMDD-title-as-kebab-case.md`
- Register entry in `[id:decision_records_dir]decision-records-register.md`
- Changelog entry in `[id:changelog_register]`

## Output to USER
1. **Confirmation**:
   - Record creation status
   - File location
   - Assigned decision ID
2. **Next Steps**:
   - Review instructions
   - Stakeholder notification
   - Follow-up actions

## Domain-Specific Rules
- Rule 0: NEVER create, modify, or delete any file under `[id:global_olaf_dir]` (e.g., `~/.olaf/`). All writes MUST be within the current repo workspace (i.e., paths rooted at `[id:core_olaf_dir]`).
- Rule 1: Follow existing naming conventions
- Rule 2: Maintain cross-references
- Rule 3: Preserve decision history
- Rule 4: Ensure traceability
- Rule 5: Keep records up-to-date

## Required Actions
1. Generate decision ID
2. Create record file
3. Update register
4. Document in changelog
5. Confirm completion

⚠️ **Critical Notes**
- Never modify existing decisions
- Maintain audit trail
- Include all stakeholders
- Document assumptions
- Keep records concise
