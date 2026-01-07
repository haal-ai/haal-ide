# Limitations and Support

## Current Limitations

- **Competency Stability**: Any competency may not always work the same way. Be extra careful and correct the behavior as needed.
- **Prompt Variability**: Despite using battle-tested prompt templates, conversations with LLMs and outcomes of any prompt are never the same. For this reason, it's not simple (possibly not possible) to get regression testing in place - although we are working on this subject.
- **Model Compatibility**: **Recommended**: Use Windsurf with GPT5 Low Reasoning or Medium Reasoning, or GitHub Copilot with Sonnet 3.x. You can try other models but results may vary.
- **Context Management**: The way the agent manages and interferes with context strongly impacts results. If you use your own agents, be extra careful with aspects such as ephemeral memory.
- **Language Support**: We only tested in Globish (basic English). Translating competencies into another language may not deliver the same results. Be careful.
- **Vendor Independence**: Although we tried to make it non-vendor dependent, there may still be some remnants from our first incarnation.
- **Directory Structure**: The structure used to store artifacts produced by prompts is just an example, but prompts are affected if you change folder names.
- **Project Management**: We did not intend to deliver project management features.
- **MCP Support**: OLAF fully supports MCP (Model Context Protocol) servers but this is not enforced - you can integrate with JIRA, Confluence, or other tools as needed.

## Future Development
This repository is not actively maintained or developed. The goal is to share a base set that can be transformed, expanded, and modified by any solo, pro users, or enterprises.

## Support
No official support is provided. While we appreciate contributions, we cannot guarantee that any issues or pull requests will be addressed.
