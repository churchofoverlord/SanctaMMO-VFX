#include "SanctaVFXAnimNotify.h"
#include "SanctaVFXPresentation.h"
#include "Components/SkeletalMeshComponent.h"
void USanctaVFXAnimNotify::Notify(USkeletalMeshComponent* Mesh,UAnimSequenceBase* Animation,const FAnimNotifyEventReference& Reference)
{
    Super::Notify(Mesh,Animation,Reference);
    if (!Mesh || !Mesh->GetOwner()) return;
    if (auto* C=Mesh->GetOwner()->FindComponentByClass<USanctaVFXPresentationComponent>())
        C->PresentAnimationPhase(Phase,SourceSocket,Mesh->DoesSocketExist(TipSocket) ? Mesh->GetSocketLocation(TipSocket) : Mesh->GetComponentLocation());
}
