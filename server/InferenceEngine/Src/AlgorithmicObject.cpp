#include "AlgorithmicObject.h"

using namespace inference;

void AlgorithmicObject::Initialize() const {
    for (auto x : associations) {
        x.Initialize();
    }
}
void AlgorithmicObject::Excute() const {
    for (auto x : associations) {
        x.Excute();
    }
};
void AlgorithmicObject::InitializeThis(){};
void AlgorithmicObject::ExcuteThis(){};
