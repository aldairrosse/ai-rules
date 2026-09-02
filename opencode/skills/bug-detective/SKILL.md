---
name: bug-detective
description: Systematic debugging protocol for investigating errors, collecting structured evidence, forming and testing hypotheses about root causes, applying verified fixes, and cleaning up non-useful traces
---

## Description
Systematic debugging protocol for investigating errors, collecting structured evidence, forming and testing hypotheses about root causes, applying verified fixes, and cleaning up non-useful traces. Treats every bug as a crime scene — gather clues first, hypothesize second, verify third, fix fourth, and discard irrelevant evidence last.


## Trigger
Activate this skill when the user:
- Says "debug this", "investigate this error", "root cause", "what caused this", "why is this failing", or "bug detective"
- Provides an error message, stack trace, crash log, or failing test output and asks for help fixing it
- Describes unexpected behavior without a known cause
- References a known bug report and wants to find the fix route

Do NOT activate for:
- Feature requests or new implementations (no error exists yet)
- Pure code review or refactoring without observed failure
- Configuration or environment setup that hasn't produced an error
- General "how does X work" questions without a specific failure

## Instructions

### Phase 1 — Evidence Collection (ALWAYS start here)

1. **Capture the crime scene**: Read the exact error message, stack trace, logs, or test output the user provides. If none given, ask the user to reproduce and share the full output.
2. **Identify the blast radius**: Determine which files, functions, and modules appear in the trace. Call `trace_path` on the failing function to map callers and callees.
3. **Collect additional evidence**:
   - Read the failing function and its immediate callers with `get_code_snippet` or `codegraph_explore`
   - Search for related error-handling code, guards, or recent changes with `search_graph`
   - Check git history for recent changes in affected files: `git log --oneline -10 -- <file>`
   - If applicable, inspect environment variables, config files, or dependency versions
4. **Document evidence**: Maintain an evidence ledger in your reasoning — each piece tagged with source (file:line, log entry, user statement).

### Phase 2 — Hypothesis Formation

1. **Generate candidate root causes**: Based on evidence, list 1-3 specific hypotheses. Each must be:
   - **Falsifiable**: states a concrete condition that can be proven true or false
   - **Mechanistic**: explains HOW the bug occurs, not just where
   - **Root-level**: targets the actual defect, not a symptom
2. **Rank by likelihood**: Prioritize based on evidence weight, code complexity smells, and recency of changes.
3. **State your leading hypothesis** to the user before testing. Format: "I suspect [ROOT CAUSE] because [EVIDENCE]. Testing by [METHOD]."

### Phase 3 — Verification

1. **Test the leading hypothesis first**:
   - Write a minimal reproduction script or test that isolates the suspected cause
   - Add targeted logging or assertions at the suspected point of failure
   - Trace data flow through the suspected path with actual inputs
2. **If confirmed**: proceed to Fix (Phase 4).
3. **If disproven**: discard the hypothesis explicitly, state why it was wrong, and move to the next candidate. Do NOT skip discarded hypotheses — the user needs to know what was ruled out.
4. **If all hypotheses disproven**: return to Phase 1 and widen evidence collection (check upstream services, race conditions, environment differences, heisenbugs).

### Phase 4 — Fix Application

1. **Propose the fix**: State exactly what to change and why it addresses the root cause.
2. **Apply the fix**: Make the minimal code change that corrects the root cause — no refactoring, no speculative guards, no "while we're here" changes.
3. **Verify the fix**:
   - Run the reproduction test/scenario that previously failed
   - Run existing tests in affected modules
   - If applicable, verify no other callers of the changed function are broken
4. **Regression check**: Verify that the original error no longer reproduces.

### Phase 5 — Evidence Cleanup

1. **Identify non-useful evidence**: List evidence items that were investigated but did not contribute to the root cause finding (red herrings).
2. **State what was ruled out**: One line per discarded hypothesis — what was suspected and why it was wrong.
3. **Keep only the causal chain**: The final report should contain only the evidence that led to the root cause and the fix.
4. **Deliver the final report** with this structure:
   - **Root Cause**: one sentence
   - **Causal Chain**: evidence → hypothesis → verification → fix
   - **Fix**: what changed, where, and why
   - **Ruled Out**: brief list of disproven hypotheses
   - **Verification**: how the fix was confirmed

### PROACTIVE SAVE TRIGGERS

After completing this workflow, call `mem_save` with:
- **Root cause found**: type `bugfix`, content includes the root cause, fix location, and causal chain
- **Novel technique used**: type `discovery`, content describes the debugging approach that worked
- **Edge case uncovered**: type `discovery`, content describes the edge case and how to detect it
- **Hypothesis disproven in a surprising way**: type `discovery`, content captures the unexpected behavior

## Rules

### Must Do
- Always collect evidence BEFORE forming hypotheses — never guess a fix first
- Always read the failing code and its callers before proposing any change
- Always state hypotheses in falsifiable terms
- Always test the leading hypothesis before applying a fix
- Always verify the fix with the original reproduction scenario
- Always deliver a final report with root cause, causal chain, fix, ruled-out items, and verification
- Always mark disproven hypotheses explicitly — the user needs to know what was ruled out

### Must NOT Do
- Never skip hypotheses straight to a fix — even if the cause seems obvious, state it as a hypothesis and verify it
- Never apply a fix without stating which hypothesis it addresses
- Never keep irrelevant evidence in the final report — clean up red herrings
- Never refactor, reformat, or "improve" unrelated code during the fix phase
- Never add speculative guards or defensive checks unless they directly address the root cause
- Never close the investigation without a final report
- Never discard evidence that contradicts a hypothesis — document it and explain why it was misleading

## Examples

### Example 1: Null Pointer Crash

**User**: "My app crashes with `TypeError: Cannot read properties of null (reading 'name')` in `UserProfile.tsx:42`."

**Agent response sequence**:

> **Phase 1 — Evidence**:
> - Crash at `UserProfile.tsx:42`: `user.name` where `user` is null
> - `user` comes from `useUser(id)` hook at line 38
> - `useUser` calls `GET /api/users/:id`, returns `data?.user ?? null`
> - Recent commit 3 hours ago added optimistic cache invalidation

> **Phase 2 — Hypotheses**:
> 1. **H1 (leading)**: The cache invalidation clears the user object before the component re-renders, so `useUser` returns null transiently. Likelihood: high — recent change, matches timing.
> 2. **H2**: The API returns null for valid user IDs under some condition. Likelihood: low — API always returns a user or 404, never null body.

> **Phase 3 — Verify H1**: Added `console.log(user, isLoading)` before line 42. Reproduced — `user` is null while `isLoading` is false right after a mutation. Confirmed.

> **Phase 4 — Fix**: Add `if (!user) return <Skeleton />` guard at line 40.

> **Phase 5 — Report**:
> - Root cause: Optimistic cache clear leaves a null window before revalidation fills the cache
> - Fix: Loading-state guard at `UserProfile.tsx:40`
> - Ruled out: API returning null (API returns 404, not null)
> - Verified: Reproduction scenario no longer crashes

### Example 2: Intermittent Timeout

**User**: "My API endpoint times out sometimes. Logs just show 504. Debug this."

**Agent response sequence**:

> **Phase 1 — Evidence**: Trace `handleCheckout` → calls `chargePayment` → calls `PaymentGateway.charge`. Gateway logs show `charge` succeeds in 200ms normally but 30s+ during timeouts. Database shows payment rows with no gateway transaction ID during timeout windows.

> **Phase 2 — Hypotheses**:
> 1. **H1 (leading)**: `chargePayment` doesn't set a timeout on the gateway HTTP call, so it waits for the gateway's default (60s) when the gateway is slow. Likelihood: high.
> 2. **H2**: Database connection pool exhausts under load, blocking the insert. Likelihood: medium.
> 3. **H3**: Gateway has intermittent degradation. Likelihood: low — gateway status page shows 99.9% uptime.

> **Phase 3 — Verify H1**: Read `chargePayment` — no `http.Client.Timeout` set. Reproduced with a mock slow gateway — call hangs for 60s. Confirmed.

> **Phase 4 — Fix**: Set `http.Client{Timeout: 5 * time.Second}` and handle the timeout error gracefully.

> **Phase 5 — Report**:
> - Root cause: No HTTP client timeout on the payment gateway call
> - Fix: 5-second timeout with error handling in `payment.go:chargePayment`
> - Ruled out: DB pool exhaustion (pool metrics normal during timeouts), gateway degradation (no correlating incidents)
> - Verified: Mock slow gateway now fails fast with timeout error instead of 504

### Example 3: Wrong Output, No Error

**User**: "My order total is sometimes double what it should be. No errors. Debug this."

**Agent response sequence**:

> **Phase 1 — Evidence**: `calculateTotal` in `orders.go` sums `lineItems`. Each `LineItem` has `Price` and `Quantity`. Traced callers → `AddToCart` at `cart.go:88` appends to `cart.Items`. But `RecalculateCart` at `cart.go:120` also appends instead of replacing. Double items on recalc.

> **Phase 2 — Hypotheses**:
> 1. **H1**: `RecalculateCart` mutates the cart by appending instead of rebuilding. Likelihood: high — explains exactly 2x totals on recalculation-triggered events.

> **Phase 3 — Verify H1**: Added assertion `len(cart.Items)` before and after `RecalculateCart`. Cart length doubles on every promo-code application. Confirmed.

> **Phase 4 — Fix**: Change `RecalculateCart` to rebuild `cart.Items = newItems` instead of `cart.Items = append(cart.Items, newItems...)`.

> **Phase 5 — Report**:
> - Root cause: `RecalculateCart` appends to existing items instead of replacing them (`cart.go:120`)
> - Fix: Assign instead of append
> - Ruled out: None — single hypothesis, confirmed
> - Verified: Cart length stable after promo-code application, totals correct
