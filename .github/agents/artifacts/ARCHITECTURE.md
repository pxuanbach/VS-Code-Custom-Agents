# Multi-Agent Development Workflow

## Workflow Diagram

```
[START]
    |
    v
[ANALYZE] --> Requirement Agent
    |
    v
need_architecture? --yes--> [DESIGN] --> Architecture Agent
    |
    no
    |
    v
[PLAN] --> Task Planner Agent
    |
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
    |         |
    |    failed  | passed
    |         v
    +----> Coding Agent
              (fix)
                |
                v
            [DONE]
```

## Agent Roles

| Agent         | Role                           | Input                        | Output                          | Tools                    | Triggers                           |
|---------------|--------------------------------|------------------------------|---------------------------------|--------------------------|------------------------------------|
| Orchestrator  | Coordinates workflow           | User request                 | Delegated tasks to subagents    | `agent`                  | User submits feature/bug/task      |
| Requirement   | Parses and classifies request  | Raw user request             | Structured spec (type, complexity, modules) | `read`, `search` | Analyze requirement, parse ticket  |
| Architecture  | Designs technical solution     | Requirement output           | Technical design document       | `read`, `search`, `execute` | Need architecture, design system   |
| Task Planner  | Breaks work into tasks         | Requirement (+ architecture) | Numbered task list with DoD     | `read`, `search`         | Plan task, break down work         |
| Coding        | Implements single task         | Task description + DoD       | Modified files + verification   | `read`, `edit`, `search`, `create_file` | Implement task, write code     |
| Review        | Reviews code quality           | Task + modified files + DoD  | LGTM or issue list (severity)   | `read`, `search`         | Review code, check quality         |
| Testing       | Generates tests                | Feature + affected modules   | Test files + coverage summary   | `read`, `search`, `create_file`, `edit` | Write tests, generate tests   |
| Validation    | Runs build/test validation     | Project path                 | Pass/fail status per pipeline   | `read`, `search`, `execute` | Validate, build, lint, test       |

## State Transitions

```
START -> ANALYZE -> PLAN -> IMPLEMENT -> REVIEW -> NEXT_TASK
                                                   |
                                        passed -> TEST -> VALIDATE
                                                   |
                                        failed -> IMPLEMENT (fix)
                                                   |
                                        passed -> DONE
```

## Key Principles

1. One task at a time - Coding Agent never receives full plan
2. Sequential iteration - Tasks run in order, review before next
3. Fail-fast retry - Review failures return to Coding immediately
4. Separation of concerns - Each agent has one role only
5. Orchestrator is stateless - Tracks progress through state transitions

## Communication Contract

### Orchestrator -> Coding Agent

```
**Task**: [task ID and description]
**Definition of Done**: [specific criteria]
**Relevant Files**: [paths for context]
```

### Review Agent -> Orchestrator

```
## LGTM | Review Failed
**Task**: [task ID]
**Issues Found**: [count by severity]
```
