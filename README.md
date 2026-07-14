# A Collection of VS Code Custom Agents

This repository contains a collection of custom agents designed to enhance the functionality of Visual Studio Code. Each agent is tailored to perform specific tasks, such as code generation, refactoring, testing, and more. The agents leverage various tools and APIs to provide seamless integration with the VS Code environment.

## Multi-Agent Development Workflow

Inspired by [Getting AI to Work in Complex Codebases](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md) document, this project implements a **Frequent Intentional Compaction** technique through a harness workflow that coordinates multiple specialized agents.

### Workflow Diagram

```
[START]
    |
    v
[ANALYZE] --> Requirement Agent
    |                   |
    |                   v
    |            [DOC] --> Material Writer (PRD)
    |
    v
need_architecture? --yes--> [DESIGN] --> Architecture Agent
    |                             |
    |                             v
    |                      [DOC] --> Material Writer (Architecture)
    |
    no
    |
    v
[PLAN] --> Task Planner Agent
              |
              v
        [DOC] --> Material Writer (Implementation Plan)

    v
[IMPLEMENT] --> Coding Agent (1 task at a time)
    |
    v
[REVIEW] --> Review Agent
    |
    | failed  | passed
    v         v
Coding   [NEXT_TASK?]
Agent        |
(retry)   --yes--|
    |         |
    |    --no----+
    |         |
    v         v
    |    [TEST] --> Testing Agent
    |         |
    |         v
    |    [VALIDATE] --> Validation Agent
    |         |           |
    |         |           v
    |         |    [DOC] --> Material Writer (Validation Report)
    |         |
    |    failed  | passed
    |         v
    +----> Coding Agent
              (fix)
                |
                v
            [DONE]
```

### Agent Roles

| Agent           | Role                           | Input                        | Output                          | Triggers                        |
|-----------------|--------------------------------|------------------------------|---------------------------------|----------------------------------|
| Orchestrator    | Coordinates workflow           | User request                 | Delegated tasks to subagents    | User submits feature/bug/task    |
| Requirement     | Parses and classifies request  | Raw user request             | Structured spec (type, complexity, modules) | Analyze requirement, parse ticket |
| Architecture    | Designs technical solution     | Requirement output           | Technical design document       | Need architecture, design system |
| Task Planner    | Breaks work into tasks         | Requirement (+ architecture)  | Numbered task list with DoD     | Plan task, break down work      |
| Coding          | Implements single task         | Task description + DoD       | Modified files + verification   | Implement task, write code      |
| Review          | Reviews code quality           | Task + modified files + DoD  | LGTM or issue list (severity)   | Review code, check quality       |
| Testing         | Generates tests                | Feature + affected modules  | Test files + coverage summary   | Write tests, generate tests     |
| Validation      | Runs build/test validation     | Project path                 | Pass/fail status per pipeline   | Validate, build, lint, test      |
| Material Writer | Writes documentation           | Structured output from agents| Markdown documents (PRD, plans, reports) | Write doc, create PRD, draft document |

### Key Principles

1. **One task at a time** - Coding Agent never receives full plan
2. **Sequential iteration** - Tasks run in order, review before next
3. **Fail-fast retry** - Review failures return to Coding immediately
4. **Separation of concerns** - Each agent has one role only
5. **Orchestrator is stateless** - Tracks progress through state transitions

### Communication Contract

**Orchestrator -> Coding Agent:**
```
**Task**: [task ID and description]
**Definition of Done**: [specific criteria]
**Relevant Files**: [paths for context]
```

**Review Agent -> Orchestrator:**
```
## LGTM | Review Failed
**Task**: [task ID]
**Issues Found**: [count by severity]
```

**Agents -> Material Writer:**
```
**Task**: Write [document type]
**Content**: [structured output from the agent]
**Output Path**: [path/to/docs/YYYY-MM-DD-[type]-[name].md]
```

## Notes

- Do I need to use specific skills? Yes, providing specific skills can help the agents perform their tasks more effectively. For example, the Coding agent can utilize skills related to code generation, refactoring, and testing to enhance its capabilities.
- The tools may differ from your VS Code tools, so you may need to adjust the tools used by each agent based on your specific setup and requirements.
- The models used in the handoffs are based on the latest available versions at the time of writing. You may want to update them to the latest versions or choose different models based on your preferences and needs.

## References

- The architecture design follows the [Multi-Agent Development Workflow](./.github/agents/artifacts/ARCHITECTURE.md) pattern.
- The Requirement and Task Planner agents are adapted from [VS Code Plan Agent](https://code.visualstudio.com/docs/copilot/agents/planning).
