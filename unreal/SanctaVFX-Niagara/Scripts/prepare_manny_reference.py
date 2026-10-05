"""Read-only copy of the game's rig for the independent lab; never publish Epic assets."""
import argparse, datetime, hashlib, json, pathlib, shutil

R = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--game-root', default='C:/Dev/SanctaMMO-Foundation-5.8')
args = parser.parse_args()
game = pathlib.Path(args.game_root).resolve()
source = game / 'Content/Characters/Mannequins'
target = R / 'Content/Characters/Mannequins'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
if game == R or not (source / 'Meshes/SKM_Manny_Simple.uasset').is_file():
    raise RuntimeError('Actual game Manny source missing')
rows = []
for path in sorted(source.rglob('*')):
    if not path.is_file():
        continue
    relative = path.relative_to(source)
    destination = target / relative
    digest = sha(path)
    if not destination.is_file() or sha(destination) != digest:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    if sha(destination) != digest:
        raise RuntimeError('Copy verification failed: ' + str(relative))
    rows.append({'path': 'Content/Characters/Mannequins/' + relative.as_posix(),
                 'sha256': digest, 'bytes': path.stat().st_size})
character = game / 'Source/SanctaMMO/Private/Characters/SanctaCharacter.cpp'
text = character.read_text(encoding='utf-8-sig')
report = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source_project': str(game), 'mesh': '/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple',
          'skeleton': '/Game/Characters/Mannequins/Meshes/SK_Mannequin',
          'game_native_default_mesh': 'SKM_Quinn_Simple' if 'Meshes/SKM_Quinn_Simple' in text else 'inspect_source',
          'character_source_sha256': sha(character), 'foundation_modified': False,
          'local_only': True, 'publish_assets': False, 'files': rows}
(R / 'Evidence/gameplay-manny-local-reference.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({'copied_and_verified': len(rows), 'bytes': sum(x['bytes'] for x in rows),
                  'mesh': report['mesh'], 'native_default': report['game_native_default_mesh']}))
