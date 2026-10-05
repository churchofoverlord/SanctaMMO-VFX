"""Reuse a frame only when its inputs, selected phase and render dependencies match."""
import hashlib,json,pathlib

class CaptureSignatures:
    def __init__(self,root):
        self.root=pathlib.Path(root);self.cache={}
        read=lambda p:json.loads((self.root/p).read_text(encoding='utf-8-sig'))
        self.definitions={row['asset']:row for row in read('Evidence/gameplay-runtime-definitions.json')['definitions']}
        self.native={row['asset'].split('.')[0]:row for row in read('Evidence/gameplay-runtime-native-assets.json')['assets'].values()}
        body=read('Source/ReferencePorts/scout-evasion.port.json')['layers'][0]['mesh_name']
        fixtures=['Config/DefaultEngine.ini','Scripts/create_runtime_review.py','Scripts/prepare_review_stage.py',
          'Content/VFXLab/Review/Fixtures/M_ReviewFloor.uasset','Content/VFXLab/Review/Fixtures/M_ReviewBody.uasset',
          'Content/Sancta/VFX/Review/Common/M_RuntimeFloorBright.uasset','Content/VFXLab/ReferenceShared/Meshes/'+body+'.uasset']
        self.render_context={'runtime':self.digest('Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXRuntime.dll'),
          'bridge':self.digest('Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXBridge.dll'),
          'fixtures':{path:self.digest(path) for path in fixtures}}

    def digest(self,path):
        path=str(path)
        if path not in self.cache:self.cache[path]=hashlib.sha256((self.root/path).read_bytes()).hexdigest()
        return self.cache[path]

    def asset_file(self,asset):
        return 'Content/'+asset.removeprefix('/Game/').split('.')[0]+'.uasset'

    def signature(self,case,profile='Default'):
        definition=self.definitions[case['definition']]
        phases=[phase for phase in definition['phase_details'] if phase['phase']==case['phase']]
        dependencies={}
        for phase in phases:
            entry=self.native[phase['system'].split('.')[0]]
            source=entry['source'];port=str(pathlib.Path(source).with_suffix('.port.json')).replace('\\','/')
            paths=[source,port,self.asset_file(entry['asset'])]
            paths += [self.asset_file(material['material']) for material in entry['materials']]
            data=json.loads((self.root/port).read_text(encoding='utf-8-sig'))
            for layer in data['layers']:
                paths.append('Content/Sancta/VFX/Common/Meshes/'+layer['mesh_name']+'.uasset')
                if layer.get('attribute_texture'):paths.append('Content/Sancta/VFX/Common/Textures/'+layer['attribute_texture']['name']+'.uasset')
                for uniform in layer['uniforms'].values():
                    if uniform.get('texture_source'):paths.append('Content/Sancta/VFX/Common/Textures/'+uniform['texture_name']+'.uasset')
            for path in paths:dependencies[path]=self.digest(path)
        if case.get('terrain'):
            for name in ['SM_IcebergBody','M_IcebergBody']:
                path='Content/Sancta/VFX/Terrain/Iceberg/'+name+'.uasset';dependencies[path]=self.digest(path)
        payload={'case':case,'profile':profile,'selected_phases':phases,'dependencies':dependencies}
        return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()

    def valid(self,row):
        try:return bool(row.get('capture_input')) and row.get('component_signature')==self.signature(row['capture_input'],row.get('profile','Default'))
        except KeyError:return False # A removed optional phase is no longer current.
