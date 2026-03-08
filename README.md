# A Collection of VS Code Custom Agents

This repository contains a collection of custom agents designed to enhance the functionality of Visual Studio Code. Each agent is tailored to perform specific tasks, such as code generation, refactoring, testing, and more. The agents leverage various tools and APIs to provide seamless integration with the VS Code environment.

## Agents Pipeline

Currently, the main workflow is as follows:
1. **[Project Research](./agents/ProjectResearch.agent.md)**: This agent is responsible for thoroughly investigating and understanding the codebase
2. **[Planning](./agents/Planner.agent.md)**: This agent creates detailed, actionable plans based on the research findings.
3. **[Implementation](./agents/Code.agent.md)**: This agent executes the implementation based on the plan created.

Leveraging the handoff features to get the workflow seamless, each agent is designed to pass the necessary context and information to the next agent in the workflow, ensuring a smooth transition from research to planning and finally to implementation.

## Notes
- Do I need to use specific skills? Yes, providing specific skills can help the agents perform their tasks more effectively. For example, the Code agent can utilize skills related to code generation, refactoring, and testing to enhance its capabilities.
- The tools may differ from your VS Code tools, so you may need to adjust the tools used by each agent based on your specific setup and requirements.
- The models used in the handoffs are based on the latest available versions at the time of writing. You may want to update them to the latest versions or choose different models based on your preferences and needs.

## Limitations

Currently, I do not know how to create a orchestrator that can manage the workflow and handoffs between agents. Therefore, the workflow is not fully automated, and users will need to manually trigger each agent in sequence. However, i think VS Code will update that feature in the future.

## References:
- The Project Research agent is Project Research agent in Roo Code, I just add <xml> tags and handoffs to fit my workflow.
- The Planner agent is Plan agent in VS Code, I just modify the document directory and handoffs to fit my workflow.
