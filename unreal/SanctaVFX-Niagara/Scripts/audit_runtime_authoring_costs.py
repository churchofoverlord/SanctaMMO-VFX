"""Inventory current geometry without presenting counts as measured GPU costs."""
import json,pathlib,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
manifest='Evidence/gameplay-runtime-build-jobs.json'
rows=[]
for job in read(manifest)['jobs']:
    layers=[]
    for layer in read(job['source'])['layers']:
        geometry=layer['geometry'];vertices=len(geometry['position'])//3
        triangles=len(geometry['index'])//3 if geometry.get('index') is not None else vertices//3
        layers.append({'pool':layer['pool_index'],'instances':layer['count'],'vertices_per_mesh':vertices,
          'triangles_per_mesh':triangles,'estimated_instanced_triangles':layer['count']*triangles,
          'blend':layer['blending'],'lighting':layer.get('lighting','unlit')})
    rows.append({'component':job['slug'],'phase':job['phase'],'anchor':job['anchor'],
      'importance':job['importance'],'persistent':job['persistent'],'duration':job['duration'],
      'renderer_groups':len(layers),'mesh_particles_per_instance':sum(layer['instances'] for layer in layers),
      'estimated_instanced_triangles':sum(layer['estimated_instanced_triangles'] for layer in layers),'layers':layers})
report={'scope':'Current runtime authoring counts. Renderer groups are not measured draw calls; triangle totals do not measure overdraw or GPU time. The game camera/hardware and starting budgets still require profiling.',
  'jobs_manifest_sha256':hashlib.sha256((root/manifest).read_bytes()).hexdigest(),
  'components':len(rows),'rows':rows,'max_mesh_particles_per_instance':max(row['mesh_particles_per_instance'] for row in rows),
  'max_renderer_groups':max(row['renderer_groups'] for row in rows),'production_budget_approved':False}
(root/'Evidence/gameplay-runtime-authoring-cost-inventory.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({key:report[key] for key in ['components','max_mesh_particles_per_instance','max_renderer_groups']}))
