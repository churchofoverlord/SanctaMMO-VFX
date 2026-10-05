"""Preserve completed PIE timings before another capture run overwrites them."""
import argparse, datetime, hashlib, json, math, pathlib, shutil
from runtime_capture_signatures import CaptureSignatures

root = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--log', required=True)
args = parser.parse_args()
read = lambda path: json.loads((root / path).read_text(encoding='utf-8-sig'))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
plan = read('Evidence/runtime-performance-cases.json')
measurements = read('Saved/RuntimeCaptures/frame-costs.json')
by_name = {row['case']: row for row in measurements}
if len(by_name) != len(measurements) or set(by_name) != {case['name'] for case in plan}:
    raise RuntimeError('Performance results do not match the complete case plan')
if [case['instances'] for case in plan] != [0, 1, 16, 48]:
    raise RuntimeError('Unexpected concurrency plan')
log = root / args.log
log_text = log.read_text(encoding='utf-8', errors='replace')
signatures = CaptureSignatures(root)
for case in plan:
    row = by_name[case['name']]
    if row['actual_instances'] != case['instances']:
        raise RuntimeError('Incorrect live instance count: ' + case['name'])
    if row['gpu_samples'] != case['perf_frames']:
        raise RuntimeError('Incomplete GPU sample window: ' + case['name'])
    for key in ['spawn_cpu_ms', 'input_update_cpu_ms', 'gpu_frame_ms']:
        if not math.isfinite(row[key]) or row[key] < 0:
            raise RuntimeError('Invalid timing: ' + case['name'] + '/' + key)
    if row['gpu_frame_ms'] <= 0:
        raise RuntimeError('No GPU measurement: ' + case['name'])
    for key in ['t.IdleWhenNotForeground', 'Slate.bAllowThrottling', 'r.VSync']:
        if row[key] != 0:
            raise RuntimeError('Throttled performance run: ' + key)
    if ('SanctaRuntimeReview admitted: ' + case['name'] + ' count=' + str(case['instances'])) not in log_text:
        raise RuntimeError('Missing admission evidence: ' + case['name'])
    row['component_signature'] = signatures.signature(case)
    row['input'] = case
baseline = by_name[plan[0]['name']]['gpu_frame_ms']
for row in measurements:
    row['whole_viewport_gpu_delta_from_baseline_ms'] = row['gpu_frame_ms'] - baseline
raw = root / 'Evidence/gameplay-runtime-performance-raw.json'
shutil.copyfile(root / 'Saved/RuntimeCaptures/frame-costs.json', raw)
report = {
    'passed': True, 'measured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Total lab PIE viewport GPU frame, 120 samples per case at 0/1/16/48 instances. '
             'Baseline deltas include viewport variation and are not isolated effect timings. '
             'Input update excludes Niagara simulation/rendering. Forced solo QA bypasses '
             'scalability; target hardware, game camera, overdraw and Shipping budgets remain unapproved.',
    'process_exit_code': 0, 'log': args.log, 'log_sha256': sha(log),
    'raw_file': raw.relative_to(root).as_posix(), 'raw_sha256': sha(raw),
    'render_context': signatures.render_context,
    'case_plan_sha256': sha(root / 'Evidence/runtime-performance-cases.json'),
    'rows': measurements, 'production_budget_approved': False,
}
(root / 'Evidence/gameplay-runtime-performance-validation.json').write_text(
    json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({'passed': True, 'instances': [row['actual_instances'] for row in measurements],
                  'gpu_frame_ms': [row['gpu_frame_ms'] for row in measurements]}))
