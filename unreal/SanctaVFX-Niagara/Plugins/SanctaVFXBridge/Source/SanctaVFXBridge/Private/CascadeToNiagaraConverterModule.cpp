
#include "Modules/ModuleManager.h"

#include "Framework/Application/SlateApplication.h"
#include "Interfaces/ISlateNullRendererModule.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Containers/Ticker.h"
#include "Editor.h"
#include "PlayInEditorDataTypes.h"
#include "Widgets/SWindow.h"
#include "SanctaVFXReviewActor.h"
#include "EngineUtils.h"
#include "Engine/World.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Settings/LevelEditorPlaySettings.h"
#include "UObject/StrongObjectPtr.h"
class FSanctaVFXBridgeModule : public IModuleInterface
{
    TSharedPtr<SWindow> ReviewWindow;
    FTSTicker::FDelegateHandle ReviewTicker;
    TStrongObjectPtr<ULevelEditorPlaySettings> ReviewSettings;
public:
    virtual void StartupModule() override {
        // Niagara's renderer paste path builds property widgets even in a commandlet.
        // A null renderer supplies the required Slate services without showing windows.
        if (IsRunningCommandlet() && !FSlateApplication::IsInitialized()) {
            auto Renderer = FModuleManager::LoadModuleChecked<ISlateNullRendererModule>("SlateNullRenderer").CreateSlateNullRenderer();
            FSlateApplication::InitializeAsStandaloneApplication(Renderer);
        }
        if (!IsRunningCommandlet() && FParse::Param(FCommandLine::Get(),TEXT("SanctaReview"))) {
            ReviewTicker=FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([this](float){
                if (!GEditor || !FSlateApplication::IsInitialized()) return true;
                if (FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get().IsLoadingAssets()) return true;
                auto* World=GEditor->GetEditorWorldContext().World();
                if (!World) return true;
                ASanctaVFXReviewActor* Stage=nullptr;
                for (TActorIterator<ASanctaVFXReviewActor> It(World);It;++It) { Stage=*It; break; }
                if (!Stage || GEditor->IsPlaySessionInProgress()) return true;
                ReviewWindow=SNew(SWindow).Title(FText::FromString(TEXT("Sancta - Visualizador VFX"))).ClientSize(FVector2D(1280,720)).SupportsMaximize(true).SupportsMinimize(true);
                FSlateApplication::Get().AddWindow(ReviewWindow.ToSharedRef());
                FRequestPlaySessionParams Params;
                ReviewSettings.Reset(DuplicateObject<ULevelEditorPlaySettings>(GetDefault<ULevelEditorPlaySettings>(),GetTransientPackage()));
                ReviewSettings->SetPlayNetMode(EPlayNetMode::PIE_Standalone);
                ReviewSettings->SetRunUnderOneProcess(true);
                ReviewSettings->SetPlayNumberOfClients(1);
                Params.EditorPlaySettings=ReviewSettings.Get();
                Params.SessionDestination=EPlaySessionDestinationType::InProcess;
                Params.WorldType=EPlaySessionWorldType::PlayInEditor;
                Params.CustomPIEWindow=ReviewWindow;
                Params.GameModeOverride=ASanctaVFXReviewGameMode::StaticClass();
                Params.bAllowOnlineSubsystem=false;
                GEditor->RequestPlaySession(Params);
                return false;
            }),1.f);
        }
    }
    virtual void ShutdownModule() override {
        if (ReviewTicker.IsValid()) FTSTicker::GetCoreTicker().RemoveTicker(ReviewTicker);
        ReviewWindow.Reset();
        ReviewSettings.Reset();
    }
};
IMPLEMENT_MODULE(FSanctaVFXBridgeModule, SanctaVFXBridge);
