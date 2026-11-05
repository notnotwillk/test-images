---
name: prove-it
description: Show that Hermes works on this runner, by running a command and reporting what it says. Use when asked to prove or check that the agent works.
version: 1.0.0
metadata:
  hermes:
    tags: [test]
    category: test
---

# Prove it

## When to Use
When someone asks you to prove, check or demonstrate that this agent works.

## Procedure
1. Run `hostname` and `uname -a` in the terminal.
2. Reply with their output, and say the `prove-it` skill ran.

## Verification
The reply names this runner, which only a command run here could know.
