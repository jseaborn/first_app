Publish the current changes: $ARGUMENTS

Follow the Publisher role from .agent-context/AGENTS.md:

1. Run the full test suite
2. Run the linter
3. If tests or lint fail, fix issues before proceeding
4. Stage the relevant files (prefer explicit file names over `git add -A`)
5. Create a descriptive commit message:
   - Imperative mood ("Add feature" not "Added feature")
   - Explain WHY, not just WHAT
   - Keep first line under 72 characters
6. Push to the current branch
7. Create a PR if requested, with:
   - Summary (2-3 bullet points)
   - Test plan (what was tested and how)
8. Update .agent-context/MISSION.md with completion status
9. Update .agent-context/MEMORY.md with session outcomes
