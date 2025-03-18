#ifndef _Inference_
#define _Inference_

template<typename TParam>
class Inference
{
public:
	Inference() {};
	~Inference() {};
	
	virtual void SetParam(TParam parameter) {};
	virtual void Initialize() {};
	virtual void PreProcessing() {};
	virtual void Execute() {};
	virtual void PostProcessing() {};
};
#endif