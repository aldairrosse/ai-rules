# Error Debugger

## Description

A systematic error debugging skill that follows evidence-based root cause analysis. Creates tests and logs to reproduce errors, forms hypotheses validated by evidence, applies fixes with user confirmation, and cleans up artifacts. Delegates exploration and fix tasks to sub-agents to minimize context consumption.

## Trigger

Activate when:
- User reports an error, bug, or unexpected behavior
- User asks to debug, troubleshoot, or investigate an issue
- User mentions error messages, stack traces, or failing tests
- Phrases: "debug this error", "why is this failing", "fix this bug", "troubleshoot", "investigate error"

Do NOT activate for:
- Feature requests or new functionality
- Code reviews or refactoring requests
- General questions about code behavior
- Performance optimization requests

## Instructions

### Phase 1: Error Triage

1. **Capture the error details** — Ask user for:
   - Exact error message or stack trace
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (language, framework, OS)

2. **Delegate exploration** — Launch a Task agent to:
   - Locate the error source in codebase
   - Identify related functions and call paths
   - Find similar error patterns in codebase history

3. **Assess clarity** — If error details are insufficient or ambiguous, ask user specific questions before proceeding.

### Phase 2: Evidence Gathering

4. **Create minimal reproduction** — Write the smallest test or script that triggers the error
5. **Add targeted logging** — Insert minimal log statements at decision points in the error path
6. **Run reproduction** — Execute the test/script to confirm error occurs

### Phase 3: Hypothesis Formation

7. **Analyze evidence** — Review logs and reproduction output
8. **Form hypotheses** — Based ONLY on observed evidence, list possible root causes:
   - Each hypothesis must cite specific evidence
   - Rank by likelihood based on evidence strength
   - Include confidence level (high/medium/low)

9. **Present to user** — If multiple hypotheses exist, ask user which to pursue first

### Phase 4: Validation

10. **Test hypothesis** — Modify reproduction to confirm or deny each hypothesis
11. **Discard invalid** — Remove hypotheses contradicted by evidence
12. **Confirm root cause** — Only proceed when evidence strongly supports one cause

### Phase 5: Fix Application

13. **Delegate fix** — Launch a Task agent to implement the solution
14. **Verify fix** — Run the original reproduction test to confirm resolution
15. **User confirmation** — Wait for user to confirm error is solved in their context

### Phase 6: Cleanup

16. **Remove artifacts** — Delete debug logs and temporary test files
17. **Preserve value** — If test has ongoing value, suggest converting to permanent test

### PROACTIVE SAVE TRIGGERS

After completing this skill's workflow, call `mem_save` with:
- **title**: "Debugged [error description]"
- **type**: bugfix
- **content**: What the error was, root cause found, fix applied, files changed
- **topic_key**: "debugging/[error-type]" (e.g., "debugging/auth-timeout", "debugging/null-reference")

Also save when:
- Hypothesis formation reveals non-obvious error pattern
- User provides critical context that changes approach
- Fix requires architectural consideration beyond the immediate error

## Rules

### Must Do

- Reproduce error before forming hypotheses — no guessing
- Cite specific evidence for each hypothesis
- Wait for user confirmation before declaring error solved
- Clean up all temporary debugging artifacts
- Delegate exploration and fixes to sub-agents to preserve context
- Ask user when multiple solutions exist or details are unclear

### Must Not Do

- Apply fixes without evidence-based hypothesis
- Skip reproduction step
- Make assumptions about root cause without validation
- Leave debug logs or test files in codebase
- Proceed with ambiguous errors without clarifying with user
- Implement multiple fixes simultaneously

### Edge Cases

- **False functions**: If code calls functions that don't exist or are unreachable, flag immediately
- **Bad configs**: Check configuration files for common mistakes (typos, missing values, wrong types)
- **Inactive blocks**: Identify if error path is inside disabled code blocks or behind feature flags
- **Human-unreadable errors**: If error message is obfuscated or minified, ask user for source maps or original code
- **Multiple errors**: Address one error at a time, starting with the root cause

## Examples

### Example 1: Standard Error Debugging

**User**: "I'm getting a TypeError: Cannot read property 'name' of undefined in my React component"

**Agent response**:
1. Delegates Task agent to locate component and identify potential undefined sources
2. Creates minimal reproduction test case
3. Adds console.log before the failing line
4. Runs reproduction — logs show `user` prop is null on initial render
5. Hypothesis: Missing null check before accessing `user.name`
6. Validates by adding null check — error disappears
7. Delegates fix to add optional chaining: `user?.name`
8. Waits for user confirmation
9. Cleans up console.log

**mem_save**: "Debugged TypeError in UserProfile component — root cause was missing null check on user prop, fixed with optional chaining"

### Example 2: Multiple Hypotheses

**User**: "My API returns 500 error intermittently"

**Agent response**:
1. Delegates Task agent to trace API endpoint and database calls
2. Creates test script that hits endpoint 100 times
3. Adds timing logs around database queries
4. Finds 3 of 100 requests fail with timeout
5. Hypotheses:
   - Database connection pool exhaustion (confidence: medium)
   - Race condition in async middleware (confidence: low)
   - Upstream service timeout (confidence: high — logs show upstream 504)
6. **Asks user**: "Found 3 possible causes. The evidence points to upstream service timeouts. Should I investigate that first?"

**User**: "Yes, investigate upstream first"

7. Validates by adding upstream timeout logging
8. Confirms root cause is third-party service latency
9. Implements retry with exponential backoff
10. Cleans up debug logs

### Example 3: Unclear Error

**User**: "Everything just breaks, nothing works anymore"

**Agent response**:
1. **Asks user**: "I need more details to help. Can you provide:
   - When did this start happening?
   - What were you doing when it broke?
   - Any error messages in console or logs?
   - Did you change anything recently?"

**User**: "It started after I updated npm packages. No error messages, just blank screen."

2. Delegates Task agent to check for breaking changes in recent package updates
3. Creates reproduction: fresh install with updated packages
4. Adds error boundary logging
5. Finds React 18 compatibility issue with older library
6. Hypothesis: Peer dependency mismatch after upgrade
7. Validates by checking package.json against compatibility matrix
8. Fixes by updating incompatible library
9. Cleans up error boundary

---

**Installed for**: opencode
**Version**: 1.0.0
**Author**: Gentle AI Ecosystem