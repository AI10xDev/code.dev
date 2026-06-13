# Phase 3: The Execution Loop

```text
+-----------------------------------------------------------+
|              Phase 3: The Execution Loop                  |
+-----------------------------------------------------------+
| For each sub-task:                                        |
|                                                           |
| 1. Plan: State intent.                                    |
|                                                           |
| 2. Act (Surgical Update):                                 |
|    - Read context.                                        |
|    - Apply edit (replace/write).                          |
|    - Auto-format.                                         |
|                                                           |
| 3. Validate (Immediate Feedback):                         |
|    - Unit test.                                           |
|    - Build (compile).                                     |
|    - Lint.                                                |
|                                                           |
| 4. Recover (If validation fails):                         |
|    - Diagnose.                                            |
|    - Undo & retry OR return to Phase 1.                   |
|                                                           |
| 5. Refactor (Cleanup):                                    |
|    - Ensure readability/docs.                             |
|    - Remove temp/debug code.                              |
|                                                           |
+-----------------------------------------------------------+
```
