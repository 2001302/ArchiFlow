#ifndef ALGORITHMICOBJECT_H
#define ALGORITHMICOBJECT_H

#include <vector>

namespace inference
{
class AlgorithmicObject {
public:
    AlgorithmicObject() = default;
  virtual ~AlgorithmicObject() = default;
    void Initialize() const;
    void Excute() const;
    void virtual InitializeThis();
    void virtual ExcuteThis();
private:
    std::vector<AlgorithmicObject> associations;
};
}
#endif //ALGORITHMICOBJECT_H
