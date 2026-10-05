"""Neutral review fixtures, owned by the lab, independent of game art."""
import json
import pathlib
import unreal as u

root=pathlib.Path(u.Paths.project_dir())
tools=u.AssetToolsHelpers.get_asset_tools()
lib=u.MaterialEditingLibrary

def fixture_material(name, colour, sculpted=False, opacity=None):
    path='/Game/VFXLab/Review/Fixtures/'+name
    material=u.load_asset(path)
    if material:return material
    material=tools.create_asset(name,'/Game/VFXLab/Review/Fixtures',u.Material,u.MaterialFactoryNew())
    material.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT)
    if opacity is not None:
        material.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT)
        alpha=lib.create_material_expression(material,u.MaterialExpressionConstant,0,180)
        alpha.set_editor_property('r',float(opacity))
        lib.connect_material_property(alpha,'',u.MaterialProperty.MP_OPACITY)
    if sculpted:
        normal=lib.create_material_expression(material,u.MaterialExpressionPixelNormalWS,0,0)
        custom=lib.create_material_expression(material,u.MaterialExpressionCustom,200,0)
        custom.set_editor_property('code','float k=.35+.65*saturate(dot(normalize(N),normalize(float3(-.4,-.6,.8))));return float3(.09,.105,.125)*k;')
        custom.set_editor_property('output_type',u.CustomMaterialOutputType.CMOT_FLOAT3)
        inp=u.CustomInput();inp.set_editor_property('input_name','N');custom.set_editor_property('inputs',[inp])
        lib.connect_material_expressions(normal,'',custom,'N');node=custom
    else:
        node=lib.create_material_expression(material,u.MaterialExpressionConstant3Vector,0,0)
        node.set_editor_property('constant',u.LinearColor(*colour,1))
    lib.connect_material_property(node,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
    lib.recompile_material(material)
    checked=json.loads(u.SanctaVFXLabLibrary.validate_material(material,u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()))
    if not checked['passed']:raise RuntimeError(str(checked))
    if not u.EditorAssetLibrary.save_loaded_asset(material):raise RuntimeError('Fixture not saved')
    return material

floor_material=fixture_material('M_ReviewFloor',(.025,.028,.033))
body_material=fixture_material('M_ReviewBody',(.07,.08,.095),True)
ghost_body_material=fixture_material('M_ReviewBodyGhost',(.07,.08,.095),True,.25)
body_data=json.loads((root/'Source/ReferencePorts/scout-evasion.port.json').read_text())
review_body=u.load_asset('/Game/VFXLab/ReferenceShared/Meshes/'+body_data['layers'][0]['mesh_name'])
if not review_body:raise RuntimeError('Editable reference body mesh missing')
