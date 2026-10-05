#pragma once
#include "CoreMinimal.h"
#include "Animation/AnimNotifies/AnimNotify.h"
#include "SanctaVFXAnimNotify.generated.h"

UCLASS(meta=(DisplayName="Sancta VFX — fase de animação"))
class SANCTAVFXRUNTIME_API USanctaVFXAnimNotify : public UAnimNotify
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Phase=TEXT("Release");
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName SourceSocket;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName TipSocket;
    virtual void Notify(USkeletalMeshComponent* MeshComp,UAnimSequenceBase* Animation,const FAnimNotifyEventReference& EventReference) override;
};
