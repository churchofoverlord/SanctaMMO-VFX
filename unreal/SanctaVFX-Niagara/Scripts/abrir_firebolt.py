import unreal

# Keep the interactive editor open after its startup script finishes.
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
asset = unreal.load_asset('/Game/VFXLab/FireBoltI/NS_FireBoltI')
if asset:
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([asset])
else:
    unreal.log_error('NS_FireBoltI nao foi encontrado em VFXLab/FireBoltI.')
