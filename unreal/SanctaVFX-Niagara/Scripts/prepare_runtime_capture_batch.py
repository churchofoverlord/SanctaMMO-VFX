"""One scene per actual event group; source hashes and baselines separate from approval."""
import pathlib,json,argparse
R=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--start',type=int,default=0);parser.add_argument('--count',type=int,default=10000);parser.add_argument('--refresh-plan',action='store_true');args=parser.parse_args()
jobs=json.loads((R/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs'];definitions=json.loads((R/'Evidence/gameplay-runtime-definitions.json').read_text(encoding='utf-8'));byform={d['presentation_id']:d for d in definitions['definitions']};cases=[]
for job in jobs[args.start:args.start+args.count]:
 if job['slug'] in definitions['pending_components']:continue
 form=job['form'];definition=byform[form]['asset'];base={'definition':definition,'phase':job['phase'],'count':3,'occupied':3,'element_a':0,'element_b':2,'hold':.65}
 if job['slug']=='ArcaneWeavingIResource':base.update(count=2,max=2)
 if (job['anchor']=='World' and job['phase'] not in ['Impact','FootContact']) or job.get('use_radius') or job.get('use_range'):base.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 else:base.update(camera_x=230,camera_y=-480,camera_z=270)
 if job['slug'].startswith('FootContact'):base['surface']=job['slug'].removeprefix('FootContact')
 if job['form']=='Combat.Guard':base.update(source_y=-55,source_z=110)
 if job['slug'].startswith('CCTaunt'):base.update(source_x=150,source_y=-35)
 if job['slug'].startswith('Basic') and job['phase']=='Release':base.update(source_y=-55,source_z=110)
 if job['slug'].startswith('FootContact'):base.update(camera_x=110,camera_y=-230,camera_z=155,look_z=30)
 if job['slug'].startswith('FootContact'):base.update(position_x=35,position_y=-45)
 if job['slug']=='DodgeStart':base.update(source_x=35,source_y=-45)
 if job['slug']=='DodgeAvoided':base.update(source_y=-45,source_z=110)
 if job['anchor']=='Link':base.update(camera_x=900,camera_y=-1200,camera_z=700,look_x=125,look_z=100,source_y=-55,source_z=110,target_x=250,target_y=0,target_z=100)
 if job['slug'] in ['PressureProvokeImpact','PressureProvokeTankImpact']:base.update(target_x=0,target_y=0,target_z=0)
 if job['form'] in ['bleed-stance','poison-stance']:base.update(camera_x=230,camera_y=-480,camera_z=270,look_x=0,source_y=-55,source_z=75,target_x=0,target_y=-52,target_z=120)
 if job['slug']=='LongJumpHold':base.update(source_z=0,target_x=600,target_y=0,target_z=0,look_x=250,look_z=100)
 if job['slug'].startswith('SeveringCast') or job['slug'].startswith('PiercingStrike') and job['phase']=='Cast':base.update(camera_x=650,camera_y=-1000,camera_z=650,look_x=140)
 if job['slug'] in ['ResurrectHold','BrightStarCast']:base.update(camera_x=1500,camera_y=-1900,camera_z=1400,look_z=170)
 if job['slug']=='ThunderstrikeIISplash':base.update(camera_x=1400,camera_y=-2600,camera_z=1400,look_z=650)
 if job['slug'].startswith('CCFear'):base.update(camera_x=250,camera_y=-650,camera_z=325,look_z=145)
 if job['slug'].startswith('Thunderstrike') and job['phase']=='Strike':base.update(camera_x=1400,camera_y=-2600,camera_z=1400,look_z=650)
 if job['slug']=='DefiantPresenceActive':base.update(camera_x=1700,camera_y=-2100,camera_z=1500,look_z=180)
 if job['slug'].startswith('Rally') and job['phase']=='Cast':base.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 if job['slug']=='IcebergProc':base.update(camera_x=1300,camera_y=-1600,camera_z=1300)
 if job['slug']=='SandShotCast':base.update(camera_x=650,camera_y=-900,camera_z=700,look_x=170,look_z=30)
 if job['slug']=='TempestSappedProc':base.update(camera_x=700,camera_y=-950,camera_z=650)
 if job['anchor']=='Source' and job['phase']=='Movement':base.update(source_z=110)
 if job['phase']=='End':base['release']=.05
 if job['phase']=='Hold' and job['slug'].startswith('Volley'):base.update(camera_x=1300,camera_y=-1600,camera_z=1300,hold=.5,range=1350,cone=25)
 if job['slug'].startswith('Volley') and 'Aim' in job['slug']:base.update(camera_x=2000,camera_y=-2600,camera_z=2000,look_x=900,look_z=0)
 ages=[8.] if job['persistent'] else sorted(set([round(min(.12,job['duration']*.2),3),round(min(.65,job['duration']*.55),3)]))
 if job['slug'] in ['GlacialSpikeIAreaImpact','GlacialSpikeIiAreaImpact']:ages.append(1.1)
 if job['slug']=='ThunderstrikeIStrike':ages.extend([.04,.22]) # separate on/off flicker samples
 if job['slug']=='SandShotCast':ages.append(.3)
 cases.append({**base,'name':'All_'+job['slug']+'_baseline','age':ages[0],'instances':0})
 for i,age in enumerate(ages):cases.append({**base,'name':'All_'+job['slug']+'_'+str(i),'age':age})
(R/'Evidence/runtime-review-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
if args.refresh_plan:
 if args.start!=0 or args.count<len(jobs):raise RuntimeError('Only the complete case list can replace the full plan')
 (R/'Evidence/runtime-capture-plan.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
print(json.dumps({'jobs_in_range':min(args.count,len(jobs)-args.start),'cases':len(cases),'start':args.start}))
