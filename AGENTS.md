# SanctaMMO VFX project memory

## Phase transitions and cleanup

- Before advancing from one VFX work phase to the next, push the already committed VFX work to the configured upstream with a normal, non-forced push. A later task-specific instruction that explicitly forbids push takes precedence. If the target branch is dirty, diverged, ambiguous, or the push is rejected, stop and report the exact state; never force-push, reset, stash, clean, or rebase to make it pass.
- At a phase boundary, identify obsolete temporary outputs created by the previous phase and remove only exact, confirmed paths. Limit routine cleanup to disposable outputs inside `C:\Dev\SanctaMMO-VFX`.
- Do not bulk-delete under `C:\Dev`, other repositories, `.git`, source references, user data, or any Unreal project. For an explicitly requested deletion outside this VFX workspace, require the exact path list and verify that each target is obsolete before removal.
- If the user says “old files” without naming paths, preserve them and ask which exact files they mean while continuing independent, non-destructive work.

This project preference does not make a local prototype integrated, formally accepted, or canonical. A current task's explicit scope, authority boundaries, and stop conditions still apply.
