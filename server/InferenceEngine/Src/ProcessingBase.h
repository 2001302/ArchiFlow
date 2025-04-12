#ifndef INFERENCEPROCESSINGBASE_H
#define INFERENCEPROCESSINGBASE_H

#include "AlgorithmicObject.h"

namespace inference {
class ProcessingBase : public AlgorithmicObject {
public:
    void InitializeThis() override;
    void ExcuteThis() override;
};
}

#endif //INFERENCEPROCESSINGBASE_H
