---
name: researcher
description: Agent-driven research with quick (search-and-learn) or deep (research-and-report) modes
tags: [research, learning, search, web-fetch, agents, parallelization]
protocol: Act
---

# Researcher Skill

Real agent-driven research workflows with two distinct modes for different research needs.

## Two Research Modes

### QUICK MODE (--quick)
Fast research for immediate insights. Workflow:
1. **Understand demand** - Clarify research requirements
2. **Search URLs** - Find relevant web sources
3. **Fetch content** - Retrieve web pages
4. **Summarize** - Generate quick findings report

**Best for**: Quick learning, rapid prototyping, time-sensitive research

### DEEP MODE (--deep, default)
Comprehensive research with structured analysis. Workflow:
1. **Understand demand** - Detailed requirement analysis
2. **Create research plan** - Structure with logical chapters
3. **Parallelize research** - Concurrent chapter research and writing
4. **Polish chapters** - Deduplication and consistency review
5. **Publish report** - Finalize consolidated report

**Best for**: Market analysis, comprehensive documentation, executive reports

## Input Parameters

- **topic** (required): The research topic or question
- **--quick**: Execute quick research mode (search-and-learn)
- **--deep**: Execute deep research mode (research-and-report, default)
- **--scope**: Research scope boundaries (optional)
- **--outcomes**: Expected deliverables and target audience (optional)
- **--output**: Output file path (optional)

## Quick Mode Workflow

```
Phase 1: Understanding demand
  └─ Clarify research requirements and context

Phase 2: Searching for URLs
  └─ Identify relevant web sources

Phase 3: Fetching web content
  └─ Retrieve and extract content from sources

Phase 4: Summarizing findings
  └─ Generate quick research report with key insights
```

**Output**: Quick research report with findings and source list

## Deep Mode Workflow

```
Phase 1: Understanding demand in detail
  └─ Comprehensive requirement analysis

Phase 2: Creating research plan
  └─ Structure research into logical chapters
     ├─ Introduction and Overview
     ├─ Current State and Trends
     ├─ Key Players and Solutions
     ├─ Best Practices and Recommendations
     └─ Future Outlook

Phase 3: Searching for URLs
  └─ Identify comprehensive source list

Phase 4: Parallelizing chapter research
  └─ Concurrent research and writing for each chapter
     ├─ Chapter 1 research
     ├─ Chapter 2 research
     ├─ Chapter 3 research
     ├─ Chapter 4 research
     └─ Chapter 5 research

Phase 5: Polishing chapters
  └─ Deduplication and consistency review
     ├─ Remove duplicate information
     ├─ Standardize formatting
     └─ Ensure logical flow

Phase 6: Publishing consolidated report
  └─ Finalize and deliver comprehensive report
     ├─ Executive summary
     ├─ Table of contents
     ├─ All chapters
     └─ Methodology and sources
```

**Output**: Comprehensive research report with structured chapters

## Usage Examples

### Quick Research
```bash
python cli.py researcher --topic "How to implement OAuth" --quick
```
Fast research on OAuth implementation with quick summary.

### Deep Research
```bash
python cli.py researcher --topic "Market analysis of cloud providers" --deep
```
Comprehensive market analysis with structured chapters.

### With Custom Scope
```bash
python cli.py researcher --topic "Cloud security trends" \
  --scope "Focus on 2024-2025, exclude legacy systems" \
  --deep
```

### Save to File
```bash
python cli.py researcher --topic "DevOps best practices" \
  --output research_report.md --deep
```

## Agent Roles

### Quick Mode Agents
- **Demand Analyzer**: Understands research requirements
- **URL Searcher**: Finds relevant web sources
- **Content Fetcher**: Retrieves web content
- **Summarizer**: Generates quick findings

### Deep Mode Agents
- **Demand Analyzer**: Detailed requirement analysis
- **Planner**: Creates structured research plan
- **URL Searcher**: Identifies comprehensive sources
- **Chapter Researchers**: Parallelize chapter research (5 concurrent)
- **Polish Agent**: Reviews and deduplicates chapters
- **Publisher**: Finalizes consolidated report

## Output Formats

### Quick Mode Report
- Research demand summary
- Key findings
- Sources consulted
- Next steps

### Deep Mode Report
- Executive summary
- Table of contents
- 5 structured chapters:
  - Introduction and Overview
  - Current State and Trends
  - Key Players and Solutions
  - Best Practices and Recommendations
  - Future Outlook
- Conclusion
- Methodology

## Integration with straf CLI

```bash
# Quick mode
python cli.py researcher --topic "your topic" --quick

# Deep mode (default)
python cli.py researcher --topic "your topic" --deep

# With output file
python cli.py researcher --topic "your topic" --output report.md --deep
```

## Success Criteria

- Topic is clearly understood
- Appropriate mode selected (quick or deep)
- All workflow phases complete successfully
- Results delivered to user
- Output file created if specified
