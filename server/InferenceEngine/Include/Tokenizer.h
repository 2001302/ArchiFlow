#ifndef TOKENIZER_H
#define TOKENIZER_H

#include<AlgorithmicObject.h>
#include <sentencepiece_processor.h>

namespace inference {
class Tokenizer : public AlgorithmicObject {
public:
    void InitializeThis() override;
    void ExcuteThis() override;
};
}
#endif //TOKENIZER_H
