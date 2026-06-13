# Coding Agent Lifecycle

This document outlines the granular operational lifecycle for autonomous coding tasks. Every agent intervention must adhere to this structure to ensure safety, maintainability, and correctness.

---

## Phase 1: Research & Discovery (The "Understand" Phase)

1.  **Analyze Directive:** Parse user instructions to identify the core goal, explicit constraints, and implicit requirements.
2.  **Define Scope Boundary:** Determine which files, modules, or services are in-scope versus out-of-scope to prevent "scope creep" or side-effect bugs.
3.  **Map Architectural Context:**
    *   Scan for project-specific conventions (`GEMINI.md`, `README.md`, `CODE_OF_CONDUCT.md`).
    *   Analyze dependency trees and configuration files (`package.json`, `Cargo.toml`, `requirements.txt`).
4.  **Validate Assumptions (Empirical):**
    *   **For Bugs:** Create a **minimal, reproducible test case** (e.g., `repro.test.ts`, `repro.py`) that fails on the current codebase. If it doesn't fail, the bug is not understood.
    *   **For Features:** Perform a Proof-of-Concept (POC) read/investigation to ensure the target APIs or structures exist as assumed.
5.  **Identify Integration Points:** Pinpoint exactly where the new code will interact with legacy code or external services.

---

## Phase 2: Strategy & Design (The "Plan" Phase)

1.  **Propose Architecture:** Draft the design approach, prioritizing idiomatic patterns established in the project.
2.  **Define "Definition of Done":**
    *   List specific unit tests required.
    *   List integration tests required.
    *   Identify necessary documentation updates.
3.  **Establish Verification Benchmarks:** Identify existing "gold standard" tests to ensure no regressions.
4.  **Decompose Work:** Break the task into atomic, single-file sub-tasks. Order them to satisfy dependency requirements.

---

## Phase 3: The Execution Loop (Iterative "Plan -> Act -> Validate")

*For each sub-task:*

1.  **Plan:** State the specific intent of the current sub-task.
2.  **Act (Surgical Update):**
    *   Read surrounding context (not just the target lines) to ensure the edit is contextually aware.
    *   Apply the edit (`replace` or `write_file`).
    *   **Immediately** apply automated formatting (e.g., `prettier --write`, `cargo fmt`).
3.  **Validate (Immediate Feedback):**
    *   **Unit Test:** Run the test specific to the code just changed.
    *   **Compile:** Run the build command to ensure no syntax/type errors.
    *   **Lint:** Run static analysis (e.g., `eslint`, `ruff`).
4.  **Recover (If validation fails):**
    *   Diagnose the failure immediately.
    *   If failure is due to edit, undo and retry.
    *   If failure is due to architectural misunderstanding, return to **Phase 1 (Research)** and adjust the strategy.
5.  **Refactor (Cleanup):**
    *   Verify the code is readable, idiomatic, and documented.
    *   Remove any "temporary" code or debug logs used during this specific sub-task.

---

## Phase 4: Finalization & Verification (The "Ship" Phase)

1.  **Global Verification:**
    *   Run the full project test suite.
    *   Run full workspace linting/type-checking (e.g., `tsc`).
2.  **Cleanup:**
    *   Delete the reproduction script/POC created in Phase 1.
    *   Clean up any temporary scratch files or generated logs.
3.  **Final Sanity Check:**
    *   Confirm the solution meets the user's *original* intent.
    *   Review against `GEMINI.md` conventions one last time.
4.  **Reporting:**
    *   Summarize the changes made.
    *   Identify any residual risks or suggested future improvements.

---

## Key Operational Rules

*   **Validation Over Velocity:** If a test fails, stopping to fix it is faster than ignoring it and debugging later.
*   **Atomic Commits:** Each sub-task edit must result in a functional, compile-passing, test-passing state. Never leave the code in a broken intermediate state.
*   **Zero-Guessing:** If an API usage or convention is unclear, read the code or run a quick discovery search (`grep`) before writing. Do not assume.
