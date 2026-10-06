#include "SanctaVFXMannyReview.h"
#include "Animation/AnimSequence.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/SceneComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "Engine/GameViewportClient.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/PlayerController.h"
#include "Camera/PlayerCameraManager.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "NiagaraComponent.h"
#include "NiagaraSystem.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "HAL/FileManager.h"
#include "ImageUtils.h"
#include "UnrealClient.h"
#include "ShaderCompiler.h"
#include "InputCoreTypes.h"
#include "Editor.h"
#include "Containers/Ticker.h"
#include "DrawDebugHelpers.h"
#include "SanctaVFXTerrain.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"

namespace {
const float Scales[]={.8f,1.f,1.2f};
const TCHAR* PoseNames[]={TEXT("Repouso"),TEXT("Ataque"),TEXT("Corrida"),TEXT("Esquiva")};
const TCHAR* ViewNames[]={TEXT("3/4"),TEXT("Frente"),TEXT("Lado")};
double Number(const TSharedPtr<FJsonObject>& J,const TCHAR* Key,double Default){double V;return J->TryGetNumberField(Key,V)?V:Default;}
TSharedPtr<FJsonValue> VectorJSON(FVector V) {
    return MakeShared<FJsonValueArray>(TArray<TSharedPtr<FJsonValue>>{
        MakeShared<FJsonValueNumber>(V.X),MakeShared<FJsonValueNumber>(V.Y),MakeShared<FJsonValueNumber>(V.Z)});
}
AActor* Proxy(UWorld* W) {
    auto* A=W->SpawnActor<AActor>();auto* Root=NewObject<USceneComponent>(A);
    A->SetRootComponent(Root);Root->RegisterComponentWithWorld(W);return A;
}
}
ASanctaVFXMannyReview::ASanctaVFXMannyReview(){PrimaryActorTick.TickGroup=TG_PostUpdateWork;}
void ASanctaVFXMannyReview::BeginPlay()
{
    Super::BeginPlay();Effect->DeactivateImmediate();Effect->SetVisibility(false);bSlow=bPaused=false;
    Audit=FParse::Param(FCommandLine::Get(),TEXT("SanctaMannyAudit"));
    if(Audit)ScaleIndex=0;
    FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(CasesJSON),Cases);
    if(!Cases.IsEmpty())Cases[0]->AsObject()->TryGetBoolField(TEXT("full_catalog"),FullCatalog);
    AuditEnd=Cases.Num();
    if(Audit){int32 Count=0;FParse::Value(FCommandLine::Get(),TEXT("SanctaMannyStart="),AuditFirst);FParse::Value(FCommandLine::Get(),TEXT("SanctaMannyCount="),Count);
        AuditFirst=FMath::Clamp(AuditFirst,0,Cases.Num());AuditEnd=Count>0?FMath::Min(Cases.Num(),AuditFirst+Count):Cases.Num();CaseIndex=CatalogIndex=AuditFirst;}
    for(const auto& C:Cases){CatalogMaps.Add(C->AsObject()->GetStringField(TEXT("name")));CatalogTitles.Add(C->AsObject()->GetStringField(TEXT("title")));}
    auto* Mesh=LoadObject<USkeletalMesh>(nullptr,TEXT("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"));
    auto MakeManny=[&](AActor*& A,USkeletalMeshComponent*& M){
        A=Proxy(GetWorld());M=NewObject<USkeletalMeshComponent>(A);M->SetupAttachment(A->GetRootComponent());
        M->SetSkeletalMeshAsset(Mesh);M->SetRelativeLocation(FVector(0,0,-96));M->SetRelativeRotation(FRotator(0,-90,0));
        M->SetCollisionEnabled(ECollisionEnabled::NoCollision);M->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
        M->RegisterComponentWithWorld(GetWorld());M->SetComponentTickEnabled(false);M->SetAnimationMode(EAnimationMode::AnimationSingleNode);
    };
    AActor* SA=nullptr;AActor* TA=nullptr;USkeletalMeshComponent* SM=nullptr;USkeletalMeshComponent* TM=nullptr;
    MakeManny(SA,SM);MakeManny(TA,TM);SourceActor=SA;TargetActor=TA;SourceMesh=SM;TargetMesh=TM;
    SourceProxy=Proxy(GetWorld());TargetProxy=Proxy(GetWorld());
    ProjectileProxy=Proxy(GetWorld());
    Presentation=NewObject<USanctaVFXPresentationComponent>(SourceProxy);Presentation->RegisterComponentWithWorld(GetWorld());Presentation->SetComponentTickEnabled(false);
    TargetLife=NewObject<USanctaVFXPresentationComponent>(TargetProxy);TargetLife->RegisterComponentWithWorld(GetWorld());TargetLife->LifeId=FGuid::NewGuid();
    const TCHAR* Paths[]={TEXT("/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle"),TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01"),
        TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd"),TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Dash")};
    for(const auto* Path:Paths)Poses.Add(LoadObject<UAnimSequence>(nullptr,Path));
    if(!Mesh||Poses.Contains(nullptr)||Cases.IsEmpty()){Passed=false;Finish();return;}
    for(const auto* Bone:{TEXT("root"),TEXT("pelvis"),TEXT("head"),TEXT("hand_l"),TEXT("hand_r"),TEXT("lowerarm_l"),TEXT("lowerarm_r"),TEXT("foot_l"),TEXT("foot_r"),TEXT("HandGrip_R")})
        if(!SourceMesh->DoesSocketExist(FName(Bone))){Passed=false;UE_LOG(LogTemp,Error,TEXT("Manny required bone/socket missing: %s"),Bone);}
    Repeat();
}
void ASanctaVFXMannyReview::Repeat(){
    if(ReviewTerrain){ReviewTerrain->RemoveTerrain();ReviewTerrain->Destroy();ReviewTerrain=nullptr;}
    if(Presentation)Presentation->ResetForLife(FGuid::NewGuid());Started=bReady=CompileRequested=false;Wait=PlaybackTime=PoseTime=0;
    if(Cases.IsValidIndex(CaseIndex))ArmMask=Cases[CaseIndex]->AsObject()->GetIntegerField(TEXT("arm_mask"));
}
void ASanctaVFXMannyReview::TogglePause(){bPaused=!bPaused;}
void ASanctaVFXMannyReview::ToggleSlow(){bSlow=!bSlow;}
void ASanctaVFXMannyReview::OpenIndex(int32 I){if(Cases.IsEmpty())return;CaseIndex=CatalogIndex=(I%Cases.Num()+Cases.Num())%Cases.Num();Repeat();}
void ASanctaVFXMannyReview::SetPose(float Time)
{
    const float S=Scales[ScaleIndex];const float Yaw=Audit?SampleIndex*73.f:20.f*FMath::Sin(Time*.5f);
    const FVector Move=Audit?FVector(42*SampleIndex,-17*SampleIndex,0):FVector(30*FMath::Sin(Time*.7f),0,0);
    SourceActor->SetActorScale3D(FVector(S));SourceActor->SetActorLocationAndRotation(Move+FVector(0,0,96*S),FRotator(0,Yaw,0));
    TargetActor->SetActorScale3D(FVector(S));TargetActor->SetActorLocationAndRotation(FVector(330,0,96*S),FRotator(0,180+Yaw*.3f,0));
    for(auto* M:{SourceMesh.Get(),TargetMesh.Get()}){
        if(!M->GetSingleNodeInstance()||M->GetSingleNodeInstance()->GetCurrentAsset()!=Poses[PoseIndex])M->SetAnimation(Poses[PoseIndex]);
        M->SetPosition(Time,false);M->TickAnimation(0,false);M->RefreshBoneTransforms();M->UpdateComponentToWorld();
    }
}
void ASanctaVFXMannyReview::UpdateRig(float Age)
{
    const auto J=Cases[CaseIndex]->AsObject();const FString Binding=J->GetStringField(TEXT("binding"));
    const float S=Scales[ScaleIndex];
    const bool OnTarget=Binding.StartsWith(TEXT("target"))||Binding==TEXT("head");
    const bool Spatial=Binding==TEXT("world")||Binding==TEXT("projectile")||Binding==TEXT("ground_link");
    SourceMesh->SetVisibility(!OnTarget,true);TargetMesh->SetVisibility(OnTarget||Binding==TEXT("beam")||Spatial,true);
    AnchorRotation=OnTarget?TargetActor->GetActorQuat():SourceActor->GetActorQuat();
    if(Binding==TEXT("chest"))AnchorRotation=AnchorRotation*FQuat(FVector::UpVector,PI*.5f);
    const FQuat Q=AnchorRotation;
    const FVector Root=SourceMesh->GetSocketLocation(TEXT("root"));
    Origin=Root;Endpoint=TargetMesh->GetSocketLocation(TEXT("spine_03"));
    if(Binding==TEXT("target_root"))Origin=TargetMesh->GetSocketLocation(TEXT("root"));
    if(Binding==TEXT("hand_elbow")){
        // Both arms share the owner's root. Four independent vectors below
        // place the authored slots; a per-side mask provides an isolated view.
        Endpoint=SourceMesh->GetSocketLocation(FName(*J->GetStringField(TEXT("endpoint_bone"))));
    }else if(Binding==TEXT("both_arms")){
        Endpoint=SourceMesh->GetSocketLocation(TEXT("lowerarm_r"));
    }else if(Binding==TEXT("weapon")){
        FString GripBone;J->TryGetStringField(TEXT("bone"),GripBone);if(GripBone.IsEmpty())GripBone=TEXT("HandGrip_R");
        const FTransform Grip=SourceMesh->GetSocketTransform(FName(*GripBone));Origin=Grip.GetLocation();
        const FVector BladeDirection=(Origin-SourceMesh->GetSocketLocation(GripBone.EndsWith(TEXT("L"))?TEXT("lowerarm_l"):TEXT("lowerarm_r"))).GetSafeNormal();
        Endpoint=Origin+BladeDirection*Number(J,TEXT("weapon_length_cm"),75)*S;
        // A debug shaft covered the thin luminous trail. Mark only endpoints.
        DrawDebugPoint(GetWorld(),Origin,3,FColor(110,125,145),false,-1);
        DrawDebugPoint(GetWorld(),Endpoint,3,FColor(110,125,145),false,-1);
    }else if(Binding==TEXT("head")){
        Origin=TargetMesh->GetSocketLocation(TEXT("head"))+FVector(0,0,(20-180)*S);
    }else if(Binding==TEXT("waist")){
        Origin=SourceMesh->GetSocketLocation(TEXT("pelvis"))-FVector(0,0,100*S);
    }else if(Binding==TEXT("chest")){
        // Guard's aO is zero: its local plane has no authored body height.
        // Place it in front of the chest and turn its sagittal plane sideways.
        Origin=SourceMesh->GetSocketLocation(TEXT("spine_03"))+SourceActor->GetActorForwardVector()*25*S;
    }else if(Binding==TEXT("target_chest")){
        Origin=TargetMesh->GetSocketLocation(TEXT("spine_03"))-FVector(0,0,162*S);
    }else if(Binding==TEXT("beam")||Binding==TEXT("cast_hand")){
        Origin=SourceMesh->GetSocketLocation(TEXT("hand_r"));
    }else if(Binding==TEXT("foot")){
        Origin=SourceMesh->GetSocketLocation(TEXT("foot_r"));Origin.Z=0;
    }else if(Binding==TEXT("source_body")||Binding==TEXT("target_body")){
        auto* Mesh=OnTarget?TargetMesh.Get():SourceMesh.Get();
        Origin=Mesh->GetSocketLocation(TEXT("spine_03"))-FVector(0,0,Number(J,TEXT("authored_height_cm"),100)*S);
    }else if(Binding==TEXT("target_contact")){
        // A confirmed contact lies on the visible surface, not inside the torso.
        // This plane is a lab fixture; game integration must use the actual hit.
        Origin=TargetMesh->GetSocketLocation(TEXT("spine_03"))+TargetActor->GetActorForwardVector()*30*S;
    }else if(Binding==TEXT("target_face")){
        Origin=TargetMesh->GetSocketLocation(TEXT("head"))-FVector(0,0,Number(J,TEXT("authored_height_cm"),175)*S);
    }else if(Binding==TEXT("weapon_muzzle")){
        Origin=SourceMesh->GetSocketLocation(TEXT("HandGrip_R"));
        Origin+=(Origin-SourceMesh->GetSocketLocation(TEXT("lowerarm_r"))).GetSafeNormal()*Number(J,TEXT("weapon_length_cm"),35)*S;
    }else if(Binding==TEXT("world")){
        // Explicit fixed world centre: moving bones must never drag a hazard.
        Origin=FVector(330,0,0);AnchorRotation=FQuat::Identity;
    }else if(Binding==TEXT("ground_link")){
        Origin=Root;Endpoint=TargetMesh->GetSocketLocation(TEXT("root"));
    }else if(Binding==TEXT("projectile")){
        const FVector Launch=SourceMesh->GetSocketLocation(TEXT("hand_r"));
        const FVector Hit=TargetMesh->GetSocketLocation(TEXT("spine_03"));
        Origin=FMath::Lerp(Launch,Hit,Audit?(SampleIndex==0?.25f:.65f):FMath::Fmod(Age,1.f));
        AnchorRotation=(Hit-Launch).Rotation().Quaternion();
    }
    const FQuat ResolvedQ=AnchorRotation;
    SourceProxy->SetActorLocationAndRotation(Origin,ResolvedQ);TargetProxy->SetActorLocationAndRotation(Origin,ResolvedQ);
    ProjectileProxy->SetActorLocationAndRotation(Origin,ResolvedQ);
    Inputs.Position=Origin;Inputs.Endpoint=Endpoint;Inputs.Direction=ResolvedQ.GetAxisX();Inputs.PhaseAge=Age;
    if(ReviewTerrain)ReviewTerrain->SetActorLocationAndRotation(Origin,ResolvedQ);
    UpdateCamera();
    Presentation->UpdatePresentation(Inputs);
    if(auto* N=Presentation->GetActiveComponent(FName(*J->GetStringField(TEXT("component")))))ApplyFixtureBasis(N);
}
void ASanctaVFXMannyReview::UpdateCamera()
{
    const FString Binding=Cases[CaseIndex]->AsObject()->GetStringField(TEXT("binding"));
    const bool OnTarget=Binding.StartsWith(TEXT("target"))||Binding==TEXT("head");
    auto* Actor=OnTarget?TargetActor.Get():SourceActor.Get();auto* Mesh=OnTarget?TargetMesh.Get():SourceMesh.Get();
    const float S=Scales[ScaleIndex];
    if(FullCatalog){
        const auto J=Cases[CaseIndex]->AsObject();const bool World=Binding==TEXT("world"),Projectile=Binding==TEXT("projectile");
        FVector Focus=Mesh->GetSocketLocation(TEXT("root"))+FVector(0,0,Number(J,TEXT("camera_focus_height_cm"),105)*S);
        if(World)Focus=Origin+FVector(0,0,Number(J,TEXT("camera_focus_height_cm"),105)*S);
        if(Projectile)Focus=Origin;
        if(Binding==TEXT("beam")||Binding==TEXT("ground_link"))Focus=(Origin+Endpoint)*.5;
        Focus+=AnchorRotation.GetAxisX()*Number(J,TEXT("camera_focus_forward_cm"),0)*S;
        const float Distance=Number(J,TEXT("camera_horizontal_cm"),515)*S;
        FVector Horizontal=ViewIndex==1?Actor->GetActorForwardVector():ViewIndex==2?-Actor->GetActorRightVector():
            (Actor->GetActorForwardVector()-Actor->GetActorRightVector()).GetSafeNormal();
        const FVector Offset=Horizontal*Distance+FVector(0,0,Number(J,TEXT("camera_elevation_cm"),135)*S);
        Camera->SetWorldLocation(Focus+Offset);Camera->SetWorldRotation((-Offset).Rotation());return;
    }
    const FVector Focus=(Binding==TEXT("beam")?
        (SourceMesh->GetSocketLocation(TEXT("root"))+TargetMesh->GetSocketLocation(TEXT("root")))*.5:
        Mesh->GetSocketLocation(TEXT("root")))+FVector(0,0,105*S);
    const FVector Horizontal=ViewIndex==1?Actor->GetActorForwardVector()*515:
        ViewIndex==2?-Actor->GetActorRightVector()*515:
        Actor->GetActorForwardVector()*365-Actor->GetActorRightVector()*365;
    const FVector Offset=(Horizontal+FVector(0,0,135))*S*(Binding==TEXT("beam")?1.5f:1.f);
    Camera->SetWorldLocation(Focus+Offset);Camera->SetWorldRotation((-Offset).Rotation());
}
void ASanctaVFXMannyReview::ApplyFixtureBasis(UNiagaraComponent* C)
{
    // World dimensions belong to gameplay and never inherit character scale.
    const float S=FullCatalog&&Cases[CaseIndex]->AsObject()->GetStringField(TEXT("anchor"))==TEXT("World")?1.f:Scales[ScaleIndex];const FQuat Q=AnchorRotation;
    const FVector D=Q.UnrotateVector(Endpoint-Origin)/S;
    const FLinearColor ThreeEndpoint(D.Y/100,D.Z/100,-D.X/100,0);
    auto Colour=[](FVector V){return FLinearColor(V.X,V.Y,V.Z,0);};
    auto RigPoint=[&](const TCHAR* Bone){const FVector P=Q.UnrotateVector(SourceMesh->GetSocketLocation(FName(Bone))-Origin)/S;return FLinearColor(P.Y/100,P.Z/100,-P.X/100,0);};
    for(const auto& Object:C->GetOverrideParameters().GetUObjects())if(auto* M=Cast<UMaterialInstanceDynamic>(Object.Get())){
        // Lab adapter: native API currently has no skeletal uniform-scale input.
        // Override the private instance basis after the API update, never a shared asset.
        M->SetVectorParameterValue(TEXT("RuntimeBasisX"),Colour(Q.GetAxisX()*S));
        M->SetVectorParameterValue(TEXT("RuntimeBasisY"),Colour(Q.GetAxisY()*S));
        M->SetVectorParameterValue(TEXT("RuntimeBasisZ"),Colour(Q.GetAxisZ()*S));
        M->SetVectorParameterValue(TEXT("RuntimeEndpoint"),ThreeEndpoint);
        M->SetVectorParameterValue(TEXT("RuntimeRightOrigin"),RigPoint(TEXT("hand_r")));
        M->SetVectorParameterValue(TEXT("RuntimeRightEndpoint"),RigPoint(TEXT("lowerarm_r")));
        M->SetVectorParameterValue(TEXT("RuntimeLeftOrigin"),RigPoint(TEXT("hand_l")));
        M->SetVectorParameterValue(TEXT("RuntimeLeftEndpoint"),RigPoint(TEXT("lowerarm_l")));
        M->SetScalarParameterValue(TEXT("RuntimeArmMask"),ArmMask);
    }
    C->SetSystemFixedBounds(FBox(FVector(-1500*S),FVector(1500*S)));C->SetPaused(bPaused);
}
bool ASanctaVFXMannyReview::Capture(const FString& Name,bool Baseline)
{
    auto* N=Presentation->GetActiveComponent(FName(*Cases[CaseIndex]->AsObject()->GetStringField(TEXT("component"))));
    if(N)N->SetVisibility(!Baseline);
    if(ReviewTerrain)ReviewTerrain->SetActorHiddenInGame(Baseline);
    if(auto* PC=UGameplayStatics::GetPlayerController(this,0))if(PC->PlayerCameraManager)PC->PlayerCameraManager->UpdateCamera(0.f);
    FViewport* V=GetWorld()->GetGameViewport()?GetWorld()->GetGameViewport()->Viewport:nullptr;
    if(V)V->Draw(false);TArray<FColor> Pixels;bool Ok=V&&GetViewportScreenShot(V,Pixels);
    if(Ok){for(auto& P:Pixels)P.A=255;const auto Size=V->GetSizeXY();TArray64<uint8> PNG;
        FImageUtils::PNGCompressImageArray(Size.X,Size.Y,Pixels,PNG);const FString Dir=FPaths::ProjectSavedDir()/CaptureDirectory();
        IFileManager::Get().MakeDirectory(*Dir,true);Ok=FFileHelper::SaveArrayToFile(PNG,*(Dir/Name));}
    if(N)N->SetVisibility(true);if(ReviewTerrain)ReviewTerrain->SetActorHiddenInGame(false);return Ok;
}
FString ASanctaVFXMannyReview::CaptureDirectory() const{return FullCatalog?TEXT("MannyFullCaptures"):TEXT("MannyCaptures");}
void ASanctaVFXMannyReview::RecordSample()
{
    const auto J=Cases[CaseIndex]->AsObject();auto* C=Presentation->GetActiveComponent(FName(*J->GetStringField(TEXT("component"))));
    auto Row=MakeShared<FJsonObject>();Row->SetStringField(TEXT("case"),J->GetStringField(TEXT("name")));Row->SetNumberField(TEXT("pose"),PoseIndex);
    Row->SetNumberField(TEXT("scale"),Scales[ScaleIndex]);Row->SetNumberField(TEXT("sample"),SampleIndex);
    Row->SetField(TEXT("origin"),VectorJSON(Origin));Row->SetField(TEXT("endpoint"),VectorJSON(Endpoint));
    Row->SetField(TEXT("actor_origin"),VectorJSON(SourceActor->GetActorLocation()));
    Row->SetField(TEXT("hand_r"),VectorJSON(SourceMesh->GetSocketLocation(TEXT("hand_r"))));
    Row->SetField(TEXT("hand_l"),VectorJSON(SourceMesh->GetSocketLocation(TEXT("hand_l"))));
    Row->SetField(TEXT("head"),VectorJSON(TargetMesh->GetSocketLocation(TEXT("head"))));
    const float BasisScale=FullCatalog&&J->GetStringField(TEXT("anchor"))==TEXT("World")?1.f:Scales[ScaleIndex];
    Row->SetNumberField(TEXT("cue_scale"),BasisScale);
    const float Error=C?FVector::Distance(C->GetComponentLocation(),Origin):1.e6f;
    Row->SetNumberField(TEXT("origin_error_cm"),Error);bool Ok=C&&Error<.01f&&Presentation->GetActiveCount()==1;
    if(C){
        int32 Materials=0;float EndpointError=0,ScaleError=0;
        const FVector D=AnchorRotation.UnrotateVector(Endpoint-Origin)/BasisScale;
        for(const auto& Obj:C->GetOverrideParameters().GetUObjects())if(auto* M=Cast<UMaterialInstanceDynamic>(Obj.Get())){
            ++Materials;const auto E=M->K2_GetVectorParameterValue(TEXT("RuntimeEndpoint"));
            EndpointError=FMath::Max(EndpointError,(FVector(E.R,E.G,E.B)-FVector(D.Y,D.Z,-D.X)/100).Size());
            const auto Z=M->K2_GetVectorParameterValue(TEXT("RuntimeBasisZ"));ScaleError=FMath::Max(ScaleError,FMath::Abs(FVector(Z.R,Z.G,Z.B).Size()-BasisScale));
        }
        Row->SetNumberField(TEXT("dynamic_materials"),Materials);Row->SetNumberField(TEXT("endpoint_error_m"),EndpointError);Row->SetNumberField(TEXT("scale_error"),ScaleError);
        Ok&=Materials>0&&EndpointError<.001f&&ScaleError<.001f;
        const FString Binding=J->GetStringField(TEXT("binding"));
        if(Binding==TEXT("both_arms")||Binding==TEXT("hand_elbow")){
            float ArmError=0;const TCHAR* Params[]={TEXT("RuntimeRightOrigin"),TEXT("RuntimeRightEndpoint"),TEXT("RuntimeLeftOrigin"),TEXT("RuntimeLeftEndpoint")};
            const TCHAR* Bones[]={TEXT("hand_r"),TEXT("lowerarm_r"),TEXT("hand_l"),TEXT("lowerarm_l")};
            for(const auto& Obj:C->GetOverrideParameters().GetUObjects())if(auto* M=Cast<UMaterialInstanceDynamic>(Obj.Get()))for(int32 K=0;K<4;++K){
                const FVector V=AnchorRotation.UnrotateVector(SourceMesh->GetSocketLocation(FName(Bones[K]))-Origin)/Scales[ScaleIndex];
                const FLinearColor Value=M->K2_GetVectorParameterValue(FName(Params[K]));
                ArmError=FMath::Max(ArmError,(FVector(Value.R,Value.G,Value.B)-FVector(V.Y,V.Z,-V.X)/100).Size());
            }
            Row->SetNumberField(TEXT("arm_binding_error_m"),ArmError);
            Row->SetNumberField(TEXT("arm_mask"),ArmMask);
            Row->SetNumberField(TEXT("arm_separation_cm"),FVector::Distance(SourceMesh->GetSocketLocation(TEXT("hand_r")),SourceMesh->GetSocketLocation(TEXT("hand_l"))));
            Ok&=ArmError<.001f&&Row->GetNumberField(TEXT("arm_separation_cm"))>1;
        }
    }
    if(ScaleIndex==1&&SampleIndex==1){
        TArray<TSharedPtr<FJsonValue>> Images;const int32 PreviousView=ViewIndex;
        for(ViewIndex=0;ViewIndex<3;++ViewIndex){
            UpdateCamera();
            SkillClass=FString::Printf(TEXT("Manny | %s | %.1fx | %s | P: pose E: escala V: vista B: bracos"),PoseNames[PoseIndex],Scales[ScaleIndex],ViewNames[ViewIndex]);
            const FString Name=FString::Printf(TEXT("%s_pose%d_view%d.png"),*J->GetStringField(TEXT("name")),PoseIndex,ViewIndex);
            const bool Image=Capture(Name,false);const bool Base=Capture(Name.Replace(TEXT(".png"),TEXT("_baseline.png")),true);
            auto ImageRow=MakeShared<FJsonObject>();ImageRow->SetNumberField(TEXT("view"),ViewIndex);ImageRow->SetStringField(TEXT("image"),TEXT("Saved/MannyCaptures/")+Name);
            ImageRow->SetStringField(TEXT("image"),TEXT("Saved/")+CaptureDirectory()+TEXT("/")+Name);
            ImageRow->SetBoolField(TEXT("saved"),Image&&Base);Images.Add(MakeShared<FJsonValueObject>(ImageRow));Ok&=Image&&Base;
            if(ViewIndex==0&&J->GetStringField(TEXT("binding"))==TEXT("both_arms")){
                const int32 PreviousMask=ArmMask;TArray<TSharedPtr<FJsonValue>> Arms;
                for(int32 Mask:{1,2}){
                    ArmMask=Mask;ApplyFixtureBasis(C);
                    const FString ArmName=Name.Replace(TEXT(".png"),Mask==1?TEXT("_right.png"):TEXT("_left.png"));
                    const bool Saved=Capture(ArmName,false);auto Arm=MakeShared<FJsonObject>();Arm->SetNumberField(TEXT("mask"),Mask);
                    Arm->SetStringField(TEXT("image"),TEXT("Saved/")+CaptureDirectory()+TEXT("/")+ArmName);Arm->SetBoolField(TEXT("saved"),Saved);Ok&=Saved;
                    Arms.Add(MakeShared<FJsonValueObject>(Arm));
                }
                ArmMask=PreviousMask;ApplyFixtureBasis(C);ImageRow->SetArrayField(TEXT("isolated_arms"),Arms);
            }
        }
        ViewIndex=PreviousView;UpdateCamera();Row->SetArrayField(TEXT("images"),Images);
    }
    Row->SetBoolField(TEXT("passed"),Ok);Passed&=Ok;Results.Add(MakeShared<FJsonValueObject>(Row));
}
void ASanctaVFXMannyReview::WriteResults(bool Complete)
{
    auto Report=MakeShared<FJsonObject>();Report->SetBoolField(TEXT("passed"),Passed);Report->SetArrayField(TEXT("samples"),Results);
    Report->SetNumberField(TEXT("cases"),AuditEnd-AuditFirst);Report->SetBoolField(TEXT("complete"),Complete);
    Report->SetNumberField(TEXT("first"),AuditFirst);Report->SetNumberField(TEXT("end"),AuditEnd);
    Report->SetStringField(TEXT("catalog_json"),CasesJSON);
    Report->SetBoolField(TEXT("cleanup_passed"),Complete&&(!Presentation||Presentation->GetActiveCount()==0));
    Report->SetStringField(TEXT("scope"),TEXT("Manny local live bone sampling and lab proxy/basis adapter. Not game combat animation, final weapons, GAS or production approval."));
    FString Out;FJsonSerializer::Serialize(Report,TJsonWriterFactory<>::Create(&Out));
    const FString Name=FullCatalog?FString::Printf(TEXT("rig-results-%d-%d.json"),AuditFirst,AuditEnd):TEXT("rig-results.json");
    const FString Dir=FPaths::ProjectSavedDir()/CaptureDirectory();IFileManager::Get().MakeDirectory(*Dir,true);
    FFileHelper::SaveStringToFile(Out,*(Dir/Name));
}
void ASanctaVFXMannyReview::Finish()
{
    if(Presentation){Presentation->ResetForLife(FGuid::NewGuid());Passed&=Presentation->GetActiveCount()==0;}
    if(ReviewTerrain){ReviewTerrain->RemoveTerrain();ReviewTerrain->Destroy();ReviewTerrain=nullptr;}
    WriteResults(true);
    GEditor->RequestEndPlayMap();SetActorTickEnabled(false);const uint8 Code=Passed?0:1;
    FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([Code](float){if(GEditor&&GEditor->IsPlaySessionInProgress())return true;FPlatformMisc::RequestExitWithStatus(false,Code);return false;}),.5f);
}
void ASanctaVFXMannyReview::Tick(float Delta)
{
    if(!ViewReady)if(auto* PC=UGameplayStatics::GetPlayerController(this,0)){
        PC->SetViewTarget(this);PC->ClientSetHUD(ASanctaVFXReviewHUD::StaticClass());PC->bShowMouseCursor=true;
        FInputModeGameAndUI Mode;Mode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);PC->SetInputMode(Mode);ViewReady=true;
    }
    if(!Audit)if(auto* PC=UGameplayStatics::GetPlayerController(this,0)){
        if(PC->WasInputKeyJustPressed(EKeys::Right))OpenIndex(CaseIndex+1);
        if(PC->WasInputKeyJustPressed(EKeys::Left))OpenIndex(CaseIndex-1);
        if(PC->WasInputKeyJustPressed(EKeys::SpaceBar))TogglePause();if(PC->WasInputKeyJustPressed(EKeys::S))ToggleSlow();if(PC->WasInputKeyJustPressed(EKeys::R))Repeat();
        if(PC->WasInputKeyJustPressed(EKeys::P)){PoseIndex=(PoseIndex+1)%4;Repeat();}
        if(PC->WasInputKeyJustPressed(EKeys::E)){ScaleIndex=(ScaleIndex+1)%3;Repeat();}
        if(PC->WasInputKeyJustPressed(EKeys::V)){ViewIndex=(ViewIndex+1)%3;}
        if(PC->WasInputKeyJustPressed(EKeys::B)){ArmMask=ArmMask==3?1:ArmMask==1?2:3;}
    }
    Wait+=Delta;if(!Cases.IsValidIndex(CaseIndex)){Finish();return;}const auto J=Cases[CaseIndex]->AsObject();
    SkillTitle=J->GetStringField(TEXT("title"));SkillClass=FString::Printf(TEXT("Manny | %s | %.1fx | %s | P: pose E: escala V: vista B: bracos"),PoseNames[PoseIndex],Scales[ScaleIndex],ViewNames[ViewIndex]);
    if(!Started){
        if(!CompileRequested){
            Definition=LoadObject<USanctaVFXDefinition>(nullptr,*J->GetStringField(TEXT("definition")));
            if(!Definition){Passed=false;Finish();return;}
            FString Override;J->TryGetStringField(TEXT("system_override"),Override);
            if(!Override.IsEmpty()){
                Definition=DuplicateObject<USanctaVFXDefinition>(Definition,this);
                auto* Variant=LoadObject<UNiagaraSystem>(nullptr,*Override);
                if(!Variant){Passed=false;Finish();return;}
                for(auto& P:Definition->Phases)if(P.Phase==FName(*J->GetStringField(TEXT("phase"))))P.System=Variant;
            }
            for(const auto& P:Definition->Phases)P.System->RequestCompile(false);CompileRequested=true;
        }
        bool Ready=true;for(const auto& P:Definition->Phases)Ready&=P.System->IsReadyToRun();
        if(!Ready||(GShaderCompilingManager&&GShaderCompilingManager->IsCompiling())||Wait<.6f)return;
        Presentation->Definitions={Definition};Inputs=FSanctaVFXEvent();Inputs.FormId=Definition->FormId;Inputs.Phase=FName(*J->GetStringField(TEXT("phase")));
        const bool OnTarget=J->GetStringField(TEXT("binding")).StartsWith(TEXT("target"))||J->GetStringField(TEXT("binding"))==TEXT("head");
        Camera->SetRelativeLocation(OnTarget?FVector(430,-360,240):FVector(150,-460,250));
        Camera->SetRelativeRotation(((OnTarget?FVector(330,0,85):FVector(130,0,110))-Camera->GetRelativeLocation()).Rotation());
        Inputs.ExecutionId=FGuid::NewGuid();Inputs.StateId=FGuid::NewGuid();Inputs.Source=SourceProxy;Inputs.Target=TargetProxy;Inputs.Projectile=ProjectileProxy;Inputs.TargetLifeId=TargetLife->LifeId;
        Inputs.bAdmitted=Inputs.bApplied=Inputs.bConfirmedHit=true;Inputs.ConfirmedProcMask=MAX_int32;Inputs.Surface=TEXT("Stone");
        Inputs.ResourceCount=4;Inputs.ResourceMax=10;Inputs.ElementA=0;Inputs.ElementB=1;Inputs.OccupiedMask=3;
        const auto* P=Definition->Phases.FindByPredicate([&](const FSanctaVFXPhase& P){return P.Phase==Inputs.Phase;});
        if(P){Inputs.ModeSnapshot=P->RequiredModeSnapshot;Inputs.StanceSnapshot=P->RequiredStanceSnapshot;Inputs.Relation=P->RequiredRelation;
            Inputs.Radius=P->ReferenceRadius;Inputs.Range=P->ReferenceRange;Inputs.ConeAngle=P->ReferenceConeAngle;
            Inputs.Surface=P->RequiredSurface.IsNone()?FName(TEXT("Stone")):P->RequiredSurface;
            if(P->Gate==ESanctaVFXGate::NaturalEnd){Inputs.bNaturalEnd=true;Presentation->EndState(Inputs.StateId,ESanctaVFXEndReason::Natural);}
            if(P->Gate==ESanctaVFXGate::Cleanse){Inputs.bCleansed=true;Presentation->EndState(Inputs.StateId,ESanctaVFXEndReason::Cleanse);}}
        TSharedPtr<FJsonObject> Fixture;
        if(J->HasField(TEXT("fixture_inputs")))Fixture=J->GetObjectField(TEXT("fixture_inputs"));
        if(Fixture){Inputs.ResourceCount=Number(Fixture,TEXT("count"),3);Inputs.ResourceMax=Number(Fixture,TEXT("max"),10);
            Inputs.OccupiedMask=Number(Fixture,TEXT("occupied"),3);Inputs.ElementA=Number(Fixture,TEXT("element_a"),0);Inputs.ElementB=Number(Fixture,TEXT("element_b"),2);
            Inputs.CastProgress=Number(Fixture,TEXT("hold"),.65);Inputs.ReleaseAge=Number(Fixture,TEXT("release"),-1);
            Inputs.Range=Number(Fixture,TEXT("range"),Inputs.Range);Inputs.ConeAngle=Number(Fixture,TEXT("cone"),Inputs.ConeAngle);}
        bool Terrain=false;J->TryGetBoolField(TEXT("terrain"),Terrain);
        SetPose(0);UpdateRig(.2f);
        if(Terrain){ReviewTerrain=GetWorld()->SpawnActor<ASanctaVFXTerrain>();ReviewTerrain->SetActorLocation(Origin);
            ReviewTerrain->InitializeTerrain(LoadObject<UStaticMesh>(nullptr,TEXT("/Game/Sancta/VFX/Terrain/Iceberg/SM_IcebergBody")),LoadObject<UMaterialInterface>(nullptr,TEXT("/Game/Sancta/VFX/Terrain/Iceberg/M_IcebergBody")),FVector::OneVector);}
        const int32 Created=Presentation->Present(Inputs);auto* C=Presentation->GetActiveComponent(FName(*J->GetStringField(TEXT("component"))));
        if(Created!=1||!C){Passed=false;Finish();return;}
        C->SetForceSolo(true);C->SetAllowScalability(false);C->SetCastShadow(false);C->SetVariableFloat(TEXT("User.CueLifetime"),Audit?30.f:1.e9f);C->ReinitializeSystem();
        Started=bReady=true;Wait=0;UE_LOG(LogTemp,Display,TEXT("Manny case ready: %d/%d %s"),CaseIndex+1,Cases.Num(),*J->GetStringField(TEXT("name")));
    }
    if(Wait<.75f)return;
    if(Audit){
        SetPose(Poses[PoseIndex]->GetPlayLength()*(SampleIndex==0?.2f:.65f));
        UpdateRig(Number(J,TEXT("audit_age"),J->GetBoolField(TEXT("persistent"))?1.f:.2f));
        // A render tick after the new bone pose lets Niagara's shader see the inputs.
        if(Wait<(FullCatalog?.82f:1.f))return;RecordSample();Wait=.75f;
        if(++SampleIndex==2){SampleIndex=0;if(++ScaleIndex==3){ScaleIndex=0;if(++PoseIndex==4){PoseIndex=0;++CaseIndex;CatalogIndex=CaseIndex;Repeat();if(FullCatalog)WriteResults(false);}}}
        if(CaseIndex>=AuditEnd)Finish();
    }else{
        if(!bPaused){const float Dt=Delta*(bSlow?1.f/3.f:1.f);PlaybackTime+=Dt;PoseTime+=Dt;}
        SetPose(FMath::Fmod(PoseTime,Poses[PoseIndex]->GetPlayLength()));
        const float Age=J->GetBoolField(TEXT("persistent"))?PlaybackTime:FMath::Fmod(PlaybackTime,Number(J,TEXT("loop_duration"),2.f));
        UpdateRig(Age);if(auto* C=Presentation->GetActiveComponent(FName(*J->GetStringField(TEXT("component")))))C->SetCustomTimeDilation(bPaused?0:(bSlow?1.f/3.f:1.f));
    }
}
