#include "CascadeToNiagaraConverterModule.h"
#include "Modules/ModuleManager.h"
#include "NiagaraMessageManager.h"
#include "Framework/Application/SlateApplication.h"
#include "Interfaces/ISlateNullRendererModule.h"
DEFINE_LOG_CATEGORY(LogFXConverter);
const FName FNiagaraConverterMessageTopics::VerboseConversionEventTopicName = "SanctaVFXVerbose";
const FName FNiagaraConverterMessageTopics::ConversionEventTopicName = "SanctaVFXAuthoring";
class FSanctaVFXBridgeModule : public IModuleInterface
{
public:
    virtual void StartupModule() override {
        // Niagara's renderer paste path builds property widgets even in a commandlet.
        // A null renderer supplies the required Slate services without showing windows.
        if (IsRunningCommandlet() && !FSlateApplication::IsInitialized()) {
            auto Renderer = FModuleManager::LoadModuleChecked<ISlateNullRendererModule>("SlateNullRenderer").CreateSlateNullRenderer();
            FSlateApplication::InitializeAsStandaloneApplication(Renderer);
        }
        auto* Manager = FNiagaraMessageManager::Get();
        Manager->RegisterMessageTopic(FNiagaraConverterMessageTopics::VerboseConversionEventTopicName);
        Manager->RegisterMessageTopic(FNiagaraConverterMessageTopics::ConversionEventTopicName);
        Manager->RegisterAdditionalMessageLogTopic(FNiagaraConverterMessageTopics::ConversionEventTopicName);
    }
};
IMPLEMENT_MODULE(FSanctaVFXBridgeModule, SanctaVFXBridge);
