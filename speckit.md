# Spec Kit — Workshop Cheatsheet

## Install

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

## Init a project

```bash
specify init . --integration copilot
```

## The 7-Step Workflow

```
Step 1  specify init              Bootstrap project
Step 2  /speckit.constitution     Project principles (coding standards, quality rules)
Step 3  /speckit.specify          Requirements — WHAT & WHY (no tech stack yet!)
Step 4  /speckit.clarify          Fill gaps via structured Q&A
Step 5  /speckit.plan             Tech blueprint — NOW add stack, architecture
Step 6  /speckit.tasks            Break plan into ordered, parallelizable tasks
Step 7  /speckit.implement        AI executes tasks systematically
```

## Optional commands

```
/speckit.analyze        Cross-artifact consistency check (after tasks, before implement)
/speckit.checklist      Quality checklist for requirements ("unit tests for English")
/speckit.taskstoissues  Convert tasks to issues
```
