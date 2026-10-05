"""Sequential native integration verification, with one commandlet shutdown."""
import unreal as u, pathlib
root = pathlib.Path(u.Paths.project_dir())
for name in ['validate_gameplay_runtime.py', 'validate_basic_routing.py',
             'build_gameplay_terrain.py', 'audit_runtime_migration.py']:
    code = (root / 'Scripts' / name).read_text(encoding='utf-8')
    exec(compile(code.replace('u.SystemLibrary.quit_editor()', ''), name, 'exec'))
u.log('SanctaRuntime complete verification passed')
