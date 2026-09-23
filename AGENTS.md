# SanctaMMO VFX project memory

## Phase transitions, local copies, and cleanup

- Maintain one local Git checkout of `churchofoverlord/SanctaMMO-VFX` as the current working copy, normally `C:\Dev\SanctaMMO-VFX` on `main` tracking `origin/main`. Do not create another clone or worktree unless the user asks.
- Before advancing from one VFX work phase to the next, push the already committed VFX work to the configured upstream with a normal, non-forced push. A later task-specific instruction that explicitly forbids push takes precedence. If the target branch is dirty, diverged, ambiguous, or the push is rejected, stop and report the exact state; never force-push, reset, stash, clean, or rebase to make it pass.
- At a phase boundary, inspect `C:\Dev` for stale duplicate clones/worktrees of this VFX repository. Keep the most up-to-date checkout. The user authorizes removal of verified obsolete duplicate VFX checkouts after checking their Git status, unique commits, and uncommitted changes.
- A commit alone does not make an ordinary tracked project file obsolete. Remove only confirmed redundant local VFX repository copies or temporary/generated artifacts that are no longer needed, using exact verified paths. Do not remove other repositories, source assets that merely contain VFX-related content, `.git` data of the retained checkout, Unreal project files, or user data.
- If a candidate duplicate has unique commits, uncommitted work, unclear provenance, or an independent purpose, preserve it and report the exact state before deletion.

This project preference does not make a local prototype integrated, formally accepted, or canonical. A current task's explicit scope, authority boundaries, and stop conditions still apply.
