# Agent Specializations

These definitions guide how Claude Code's sub-agent system (Task tool) should be
used. When spawning sub-agents, reference these roles for consistent behavior.

## Researcher
- **Role**: Explore codebase, read documentation, analyze problems
- **Tools**: Read, Glob, Grep, WebFetch, WebSearch
- **Output**: Summary with specific file:line references and recommendations
- **When to use**: Before any implementation work
- **Sub-agent type**: Explore (for codebase) or general-purpose (for web research)

## Implementer
- **Role**: Write code, create files, make targeted changes
- **Tools**: Read, Edit, Write, Bash (build/test only)
- **Rules**:
  - Always run tests after changes
  - Never skip linting
  - Minimal changes — don't refactor adjacent code
- **When to use**: After research is complete and plan is approved

## Reviewer
- **Role**: Review code changes for quality, security, and correctness
- **Tools**: Read, Grep, Bash (git diff only)
- **Checklist**:
  - [ ] Security: No injection, XSS, auth bypass, OWASP top 10
  - [ ] Correctness: Does it match the stated intent?
  - [ ] Tests: Are changes covered?
  - [ ] Performance: Any obvious bottlenecks?
  - [ ] Style: Follows project conventions?
- **When to use**: After implementation, before commit

## Publisher
- **Role**: Commit, push, create PRs, update docs
- **Tools**: Bash (git commands only), Edit (changelog/docs)
- **Rules**:
  - Descriptive commit messages (imperative mood, explain why)
  - PR descriptions with summary and test plan
  - Update MEMORY.md with session outcomes
- **When to use**: After review passes

## Routing Rules

```
New task         → Researcher → Plan → User Approval → Implementer → Reviewer → Publisher
Bug report       → Researcher → Implementer → Reviewer → Publisher
Feature request  → Researcher → Plan → User Approval → Implementer → Reviewer → Publisher
Refactor         → Researcher → Reviewer (current) → Implementer → Reviewer (new) → Publisher
Documentation    → Researcher → Implementer → Reviewer → Publisher
```

## Escalation
- If Reviewer finds critical issues → back to Implementer
- If tests fail after implementation → fix before proceeding
- If scope is unclear → ask user before proceeding
