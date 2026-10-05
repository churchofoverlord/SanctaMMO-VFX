"""Interactive test inputs for each current phase, plus the real terrain body."""
import pathlib,json,re,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
jobs=read('Evidence/gameplay-runtime-build-jobs.json')['jobs'];defs=read('Evidence/gameplay-runtime-definitions.json')
byform={d['presentation_id']:d['asset'] for d in defs['definitions']}
if defs['pending_components'] or defs['canonical_pending']:raise RuntimeError('Definitions are still incomplete')
cases=[]
for j in jobs:
 title=re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',re.sub(r'([A-Z]+)([A-Z][a-z])',r'\1 \2',j['slug']))
 title=re.sub(r'\bIi\b','II',title);title=re.sub(r'\bIii\b','III',title)
 c={'name':j['slug'],'title':title,'definition':byform[j['form']],'phase':j['phase'],'count':3,'max':10,'occupied':3,'element_a':0,'element_b':2,'hold':.65}
 if j.get('use_radius') or j.get('use_range') or j['anchor']=='World' and j['phase'] not in ['Impact','FootContact']:c.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 else:c.update(camera_x=230,camera_y=-480,camera_z=270)
 if j['slug'].startswith('FootContact'):c.update(surface=j['slug'].removeprefix('FootContact'),camera_x=110,camera_y=-230,camera_z=155,look_z=30)
 if j['slug'].startswith('FootContact'):c.update(position_x=35,position_y=-45)
 if j['slug']=='DodgeStart':c.update(source_x=35,source_y=-45)
 if j['slug']=='DodgeAvoided':c.update(source_y=-45,source_z=110)
 if j['anchor']=='Link':c.update(camera_x=900,camera_y=-1200,camera_z=700,look_x=125,look_z=100,source_y=-55,source_z=110,target_x=250,target_y=0,target_z=100)
 if j['slug'] in ['PressureProvokeImpact','PressureProvokeTankImpact']:c.update(target_x=0,target_y=0,target_z=0)
 if j['form'] in ['bleed-stance','poison-stance']:c.update(camera_x=230,camera_y=-480,camera_z=270,look_x=0,source_y=-55,source_z=75,target_x=0,target_y=-52,target_z=120)
 if j['slug']=='LongJumpHold':c.update(source_z=0,target_x=600,target_y=0,target_z=0,look_x=250,look_z=100)
 if j['slug'].startswith('SeveringCast') or j['slug'].startswith('PiercingStrike') and j['phase']=='Cast':c.update(camera_x=650,camera_y=-1000,camera_z=650,look_x=140)
 if j['slug'] in ['ResurrectHold','BrightStarCast']:c.update(camera_x=1500,camera_y=-1900,camera_z=1400,look_z=170)
 if j['slug']=='ThunderstrikeIISplash':c.update(camera_x=1400,camera_y=-2600,camera_z=1400,look_z=650)
 if j['slug'].startswith('CCTaunt'):c.update(source_x=150,source_y=-35)
 if j['slug'].startswith('Volley') and 'Aim' in j['slug']:c.update(camera_x=2000,camera_y=-2600,camera_z=2000,look_x=900,look_z=0)
 if j['slug'].startswith('CCFear'):c.update(camera_x=250,camera_y=-650,camera_z=325,look_z=145)
 if j['slug'].startswith('Thunderstrike') and j['phase']=='Strike':c.update(camera_x=1400,camera_y=-2600,camera_z=1400,look_z=650)
 if j['slug']=='DefiantPresenceActive':c.update(camera_x=1700,camera_y=-2100,camera_z=1500,look_z=180)
 if j['slug'].startswith('Rally') and j['phase']=='Cast':c.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 if j['slug']=='IcebergProc':c.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 if j['slug']=='SandShotCast':c.update(camera_x=650,camera_y=-900,camera_z=700,look_x=170,look_z=30)
 if j['slug']=='TempestSappedProc':c.update(camera_x=700,camera_y=-950,camera_z=650)
 if j['anchor']=='Source' and j['phase']=='Movement':c.update(source_z=110)
 if j['form']=='Combat.Guard':c.update(source_y=-55,source_z=110)
 if j['slug'].startswith('Basic') and j['phase']=='Release':c.update(source_y=-55,source_z=110)
 if j['slug']=='ArcaneWeavingIResource':c['max']=2
 cases.append(c)
ice=next(c for c in cases if c['name'].startswith('Iceberg'))
cases.append({**ice,'name':'IcebergTerrainBody','title':'Iceberg — terreno com colisao','terrain':True,'position_x':350,'camera_x':900,'camera_y':-900,'camera_z':650,'look_x':350,'look_z':80})
(R/'Evidence/runtime-viewer-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'phases':len(jobs),'scenes':len(cases),'default_speed':1.0}))
