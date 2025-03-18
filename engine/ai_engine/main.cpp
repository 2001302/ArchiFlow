#include "inference_llama.h"
#include "inference_stable_diffusion.h"

int main(int argc, char** argv) {

    int mode = 0;
    InferenceLlama llama;
    InferenceStableDiffusion stable_diffusion;

    while (true) {
        switch (mode)
        {
        case 0: {
            llama.Run(argc, argv);
            break;
        }
        case 1: {
            stable_diffusion.Run(argc, argv);
            break;
        }
        default:
            break;
        }
        
    }
    
    return 0;
}
