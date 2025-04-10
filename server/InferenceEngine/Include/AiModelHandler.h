#ifndef AIMODELHANDLER_H
#define AIMODELHANDLER_H

namespace inference {
class AiModelHandler {
private:
    AiModelHandler() = default;

    AiModelHandler(const AiModelHandler&) = delete;
    AiModelHandler& operator=(const AiModelHandler&) = delete;

    AiModelHandler(AiModelHandler&&) = delete;
    AiModelHandler& operator=(AiModelHandler&&) = delete;

    static AiModelHandler* instance;
public:
    static AiModelHandler& GetInstance() {
        if (instance == nullptr) {
            instance = new AiModelHandler();
        }
        return *instance;
    }

    static void ReleaseInstance() {
        if (instance != nullptr) {
            delete instance;
            instance = nullptr;
        }
    }

    bool IntializeModel() { return true; }
    bool IsInitializeModel() { return true; }
};

AiModelHandler* AiModelHandler::instance = nullptr;
}

#endif //AIMODELHANDLER_H