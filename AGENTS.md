# SanctaMMO VFX project memory

## Phase transitions and cleanup

- Before advancing from one VFX work phase to the next, push the already committed VFX work to the configured upstream with a normal, non-forced push. A later task-specific instruction that explicitly forbids push takes precedence. If the target branch is dirty, diverged, ambiguous, or the push is rejected, stop and report the exact state; never force-push, reset, stash, clean, or rebase to make it pass.
- At a phase boundary, identify temporary or generated artifacts created by VFX work under `C:\Dev` that are no longer needed after the necessary work has been committed. Remove only those confirmed disposable files at exact paths.
- A commit alone does not make a file obsolete. Keep tracked VFX project files, source references, `.git`, Unreal project files, user data, and any output still needed for reproducibility, review, or future work. Do not bulk-delete repositories or directories.
- If a generated file's origin or ongoing use is unclear, preserve it and ask which exact paths the user means while continuing independent, non-destructive work.

This project preference does not make a local prototype integrated, formally accepted, or canonical. A current task's explicit scope, authority boundaries, and stop conditions still apply.
