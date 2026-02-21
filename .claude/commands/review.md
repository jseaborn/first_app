Review the current changes for quality and correctness: $ARGUMENTS

Follow the Reviewer role from .agent-context/AGENTS.md:

1. Run `git diff` to see all staged and unstaged changes
2. Run `git diff --cached` to see what's staged
3. For each changed file, check against this checklist:
   - **Security**: Any injection, XSS, auth bypass, or OWASP top 10 issues?
   - **Correctness**: Does it match the stated intent?
   - **Tests**: Are the changes covered by tests?
   - **Performance**: Any obvious bottlenecks or N+1 queries?
   - **Style**: Does it follow project conventions from CLAUDE.md?
   - **Complexity**: Is this the simplest solution that works?
4. List issues found with severity levels:
   - CRITICAL: Must fix before merge (security, correctness)
   - WARNING: Should fix (performance, maintainability)
   - NIT: Optional improvement (style, naming)

If CRITICAL issues are found:
- List them clearly
- Do NOT proceed to publish
- Recommend specific fixes

If no critical issues:
- Confirm the changes are ready for /publish
