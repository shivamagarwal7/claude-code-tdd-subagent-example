---
name: driver-navigator-tdd
description: Driver-Navigator pair programming with TDD. Triggers on "implement", "build", "create", "pair program", "tdd".
allowed-tools: Read, Glob, Grep, Bash
---
# Driver-Navigator TDD

navigator agent writes tests and specs. driver agent writes implementation.

## Role Split
| Agent     | Phases | Writes |
|-----------|--------|--------|
| navigator | PLAN, RED, REVIEW | Tests, specs, feedback |
| driver    | GREEN, REFACTOR | Implementation only |

Invoke subagents for executing the workflow

## Handoff Format
```
MODE: [PLAN|RED|GREEN|REVIEW|REFACTOR]
TASK: [what to do]
FILES: [relevant files]
TESTS: [test command]
DONE_WHEN: [success criteria]
```

## Workflow

### 1. PLAN → Navigator
```
MODE: PLAN
TASK: Analyze [requirement], design test strategy
FILES: [relevant source files]
DONE_WHEN: Strategy saved to .claude/handoff/navigator.md
```

### 2. RED → Navigator
```
MODE: RED
TASK: Write failing test for [feature]
FILES: [test file location]
TESTS: [test command]
DONE_WHEN: Test fails with expected error
```
**GATE: Navigator confirms failure before proceeding**

### 3. GREEN → Driver
```
MODE: GREEN
TASK: Minimal code to pass test
FILES: .claude/handoff/navigator.md, [impl files]
TESTS: [test command]
DONE_WHEN: All tests pass
```
**GATE: Driver confirms pass before proceeding**

### 4. REVIEW → Navigator
```
MODE: REVIEW
TASK: Review implementation, decide if refactor needed
FILES: .claude/handoff/driver.md, [changed files]
DONE_WHEN: Review saved to .claude/handoff/navigator.md
```

### 5. REFACTOR → Driver (if needed)
```
MODE: REFACTOR
TASK: Apply improvements from navigator review
FILES: .claude/handoff/navigator.md, [files to change]
TESTS: [test command]
DONE_WHEN: Tests pass, improvements applied
```

## Cycle
```
Navigator: PLAN → RED (writes test, confirms fail)
Driver:    GREEN (implements, confirms pass)
Navigator: REVIEW
Driver:    REFACTOR (if needed)
```
