#ifndef TEST_H
#define TEST_H
#include<iostream>
#include<gtest.h>
#include <onnxruntime_cxx_api.h>
#include <sentencepiece_processor.h>
#include <vector>
#include <string>
#include <random>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <memory>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}

#endif //TEST_H


/*

class LlamaOnnxModel {
private:
    Ort::Env env;
    Ort::SessionOptions session_options;
    std::unique_ptr<Ort::Session> session;
    std::unique_ptr<sentencepiece::SentencePieceProcessor> tokenizer;

    Ort::AllocatorWithDefaultOptions allocator;
    std::vector<std::string> input_names;
    std::vector<std::string> output_names;

    // 모델 정보
    int vocab_size;
    int bos_token_id;
    int eos_token_id;

    // 난수 생성기
    std::mt19937 rng;

public:
    LlamaOnnxModel(const std::string& model_path, const std::string& tokenizer_path)
        : env(ORT_LOGGING_LEVEL_WARNING, "llama-inference"),
          rng(std::random_device{}()) {

        std::cout << "모델 초기화 중..." << std::endl;

        // ONNX Runtime 세션 설정
        session_options.SetIntraOpNumThreads(4);
        session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

        // 가능한 경우 CUDA 사용
        Ort::ThrowOnError(OrtSessionOptionsAppendExecutionProvider_CUDA(session_options, 0));

        // 모델 로드
        std::cout << "ONNX 모델 로드 중: " << model_path << std::endl;
        session = std::make_unique<Ort::Session>(env, model_path.c_str(), session_options);
        std::cout << "모델 로드 완료!" << std::endl;

        // 입력 및 출력 이름 가져오기
        GetModelInfo();

        // 토크나이저 로드
        std::cout << "토크나이저 로드 중: " << tokenizer_path << std::endl;
        tokenizer = std::make_unique<sentencepiece::SentencePieceProcessor>();
        const auto status = tokenizer->Load(tokenizer_path);
        if (!status.ok()) {
            throw std::runtime_error("토크나이저 로드 실패: " + status.ToString());
        }

        // 토크나이저 특수 토큰 ID 설정
        bos_token_id = 1;  // 일반적인 LLaMA 토크나이저의 BOS 토큰 ID
        eos_token_id = 2;  // 일반적인 LLaMA 토크나이저의 EOS 토큰 ID
        vocab_size = tokenizer->GetPieceSize();

        std::cout << "초기화 완료!" << std::endl;
    }

    void GetModelInfo() {
        // 입력 노드 이름 가져오기
        size_t num_input_nodes = session->GetInputCount();
        input_names.reserve(num_input_nodes);

        for (size_t i = 0; i < num_input_nodes; i++) {
            char* input_name = session->GetInputName(i, allocator);
            input_names.push_back(input_name);
            allocator.Free(input_name);
        }

        // 출력 노드 이름 가져오기
        size_t num_output_nodes = session->GetOutputCount();
        output_names.reserve(num_output_nodes);

        for (size_t i = 0; i < num_output_nodes; i++) {
            char* output_name = session->GetOutputName(i, allocator);
            output_names.push_back(output_name);
            allocator.Free(output_name);
        }

        std::cout << "입력 노드: ";
        for (const auto& name : input_names) {
            std::cout << name << " ";
        }
        std::cout << std::endl;

        std::cout << "출력 노드: ";
        for (const auto& name : output_names) {
            std::cout << name << " ";
        }
        std::cout << std::endl;
    }

    std::vector<int64_t> Tokenize(const std::string& text) {
        std::vector<int> token_ids;
        tokenizer->Encode(text, &token_ids);

        // int64_t로 변환 (ONNX Runtime 요구사항)
        std::vector<int64_t> tokens(token_ids.begin(), token_ids.end());
        return tokens;
    }

    std::string Detokenize(const std::vector<int64_t>& tokens) {
        std::vector<int> token_ids(tokens.begin(), tokens.end());
        std::string text;
        tokenizer->Decode(token_ids, &text);
        return text;
    }

    // 소프트맥스 함수
    std::vector<float> Softmax(const std::vector<float>& logits) {
        std::vector<float> probs(logits.size());
        float max_val = *std::max_element(logits.begin(), logits.end());
        float sum = 0.0f;

        for (size_t i = 0; i < logits.size(); i++) {
            probs[i] = std::exp(logits[i] - max_val);
            sum += probs[i];
        }

        for (size_t i = 0; i < probs.size(); i++) {
            probs[i] /= sum;
        }

        return probs;
    }

    // top-p 샘플링을 위한 필터링
    std::vector<float> TopPFilter(const std::vector<float>& probs, float top_p) {
        std::vector<float> filtered_probs = probs;

        // (인덱스, 확률) 쌍 생성
        std::vector<std::pair<size_t, float>> indexed_probs;
        for (size_t i = 0; i < probs.size(); i++) {
            indexed_probs.push_back({i, probs[i]});
        }

        // 확률 기준으로 내림차순 정렬
        std::sort(indexed_probs.begin(), indexed_probs.end(),
                 [](const auto& a, const auto& b) { return a.second > b.second; });

        // 누적 확률 계산 및 top_p 이상에 해당하는 토큰 마스킹
        float cumulative_prob = 0.0f;
        for (size_t i = 0; i < indexed_probs.size(); i++) {
            cumulative_prob += indexed_probs[i].second;
            if (cumulative_prob > top_p) {
                for (size_t j = i + 1; j < indexed_probs.size(); j++) {
                    filtered_probs[indexed_probs[j].first] = 0.0f;
                }
                break;
            }
        }

        return filtered_probs;
    }

    // 확률 분포에서 토큰 샘플링
    int64_t SampleToken(const std::vector<float>& probs) {
        std::discrete_distribution<int64_t> dist(probs.begin(), probs.end());
        return dist(rng);
    }

    // 로짓에 반복 패널티 적용
    void ApplyRepetitionPenalty(std::vector<float>& logits,
                              const std::vector<int64_t>& input_ids,
                              float penalty) {
        for (const auto& token_id : input_ids) {
            if (token_id >= 0 && token_id < static_cast<int64_t>(logits.size())) {
                if (logits[token_id] > 0) {
                    logits[token_id] /= penalty;
                } else {
                    logits[token_id] *= penalty;
                }
            }
        }
    }

    std::string Generate(const std::string& prompt, int max_length = 100,
                      float temperature = 0.7f, float top_p = 0.9f,
                      float repetition_penalty = 1.1f) {
        // 입력 토큰화
        std::vector<int64_t> input_ids = Tokenize(prompt);

        // 생성 시작 시간
        auto start_time = std::chrono::high_resolution_clock::now();

        // 생성 과정
        for (int i = 0; i < max_length; i++) {
            // 배치 차원 추가 (배치 크기 = 1)
            std::vector<int64_t> batch_input_ids = {input_ids};

            // 입력 텐서 차원 계산
            std::vector<int64_t> input_dims = {1, static_cast<int64_t>(input_ids.size())};

            // 어텐션 마스크 생성 (모든 토큰에 대해 1)
            std::vector<int64_t> attention_mask(input_ids.size(), 1);
            std::vector<int64_t> batch_attention_mask = {attention_mask};

            // ONNX Runtime 입력 텐서 생성
            std::vector<Ort::Value> ort_inputs;

            // 입력 ID 텐서
            Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(
                OrtAllocatorType::OrtArenaAllocator, OrtMemType::OrtMemTypeDefault);

            ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                memory_info, input_ids.data(), input_ids.size(), input_dims.data(), input_dims.size()));

            // 어텐션 마스크 텐서
            ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                memory_info, attention_mask.data(), attention_mask.size(), input_dims.data(), input_dims.size()));

            // 위치 ID가 필요한 경우 (모델에 따라 다름)
            if (std::find(input_names.begin(), input_names.end(), "position_ids") != input_names.end()) {
                std::vector<int64_t> position_ids(input_ids.size());
                for (size_t pos = 0; pos < position_ids.size(); pos++) {
                    position_ids[pos] = static_cast<int64_t>(pos);
                }

                ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                    memory_info, position_ids.data(), position_ids.size(), input_dims.data(), input_dims.size()));
            }

            // 추론 실행
            auto output_tensors = session->Run(
                Ort::RunOptions{nullptr},
                input_names.data(),
                ort_inputs.data(),
                ort_inputs.size(),
                output_names.data(),
                output_names.size());

            // 로짓 추출 (출력의 첫 번째 텐서, 마지막 토큰의 로짓)
            auto* logits_data = output_tensors[0].GetTensorData<float>();
            auto logits_shape = output_tensors[0].GetTensorTypeAndShapeInfo().GetShape();

            // logits 형태: [batch_size, sequence_length, vocab_size]
            int64_t batch_size = logits_shape[0];        // 보통 1
            int64_t sequence_length = logits_shape[1];   // 입력 시퀀스 길이
            int64_t vocab_size = logits_shape[2];        // 어휘 크기

            // 마지막 토큰의 로짓 추출 (배치 크기 1 가정)
            std::vector<float> last_token_logits(vocab_size);
            int64_t offset = (sequence_length - 1) * vocab_size; // 마지막 토큰 위치

            for (int64_t j = 0; j < vocab_size; j++) {
                last_token_logits[j] = logits_data[offset + j];
            }

            // 반복 패널티 적용
            if (repetition_penalty != 1.0f) {
                ApplyRepetitionPenalty(last_token_logits, input_ids, repetition_penalty);
            }

            // 온도 적용
            if (temperature != 1.0f && temperature > 0.0f) {
                for (auto& logit : last_token_logits) {
                    logit /= temperature;
                }
            }

            // 확률 분포 계산
            std::vector<float> probs = Softmax(last_token_logits);

            // top-p 샘플링 적용
            if (top_p < 1.0f) {
                probs = TopPFilter(probs, top_p);

                // 재정규화
                float sum = std::accumulate(probs.begin(), probs.end(), 0.0f);
                if (sum > 0.0f) {
                    for (auto& p : probs) {
                        p /= sum;
                    }
                } else {
                    // 모든 확률이 0인 경우 균일 분포 사용
                    for (auto& p : probs) {
                        p = 1.0f / probs.size();
                    }
                }
            }

            // 다음 토큰 샘플링
            int64_t next_token = SampleToken(probs);

            // 종료 토큰이면 생성 중단
            if (next_token == eos_token_id) {
                break;
            }

            // 다음 토큰 추가
            input_ids.push_back(next_token);

            // 진행 상황 표시 (10 토큰마다)
            if ((i + 1) % 10 == 0) {
                std::cout << "." << std::flush;
            }
        }

        // 생성 종료 시간
        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end_time - start_time;
        std::cout << "\n생성 시간: " << elapsed.count() << "초" << std::endl;

        // 결과 디코딩
        std::string generated_text = Detokenize(input_ids);
        return generated_text;
    }

    // 간단한 탐욕적 생성 (온도 = 0)
    std::string GenerateGreedy(const std::string& prompt, int max_length = 100) {
        // 입력 토큰화
        std::vector<int64_t> input_ids = Tokenize(prompt);

        for (int i = 0; i < max_length; i++) {
            // ONNX 세션 입력 준비
            std::vector<int64_t> input_dims = {1, static_cast<int64_t>(input_ids.size())};
            std::vector<int64_t> attention_mask(input_ids.size(), 1);

            Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(
                OrtAllocatorType::OrtArenaAllocator, OrtMemType::OrtMemTypeDefault);

            std::vector<Ort::Value> ort_inputs;

            ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                memory_info, input_ids.data(), input_ids.size(), input_dims.data(), input_dims.size()));

            ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                memory_info, attention_mask.data(), attention_mask.size(), input_dims.data(), input_dims.size()));

            // 위치 ID 추가 (필요한 경우)
            if (std::find(input_names.begin(), input_names.end(), "position_ids") != input_names.end()) {
                std::vector<int64_t> position_ids(input_ids.size());
                for (size_t pos = 0; pos < position_ids.size(); pos++) {
                    position_ids[pos] = static_cast<int64_t>(pos);
                }

                ort_inputs.push_back(Ort::Value::CreateTensor<int64_t>(
                    memory_info, position_ids.data(), position_ids.size(), input_dims.data(), input_dims.size()));
            }

            // 추론 실행
            auto output_tensors = session->Run(
                Ort::RunOptions{nullptr},
                input_names.data(),
                ort_inputs.data(),
                ort_inputs.size(),
                output_names.data(),
                output_names.size());

            // 로짓 추출
            auto* logits_data = output_tensors[0].GetTensorData<float>();
            auto logits_shape = output_tensors[0].GetTensorTypeAndShapeInfo().GetShape();

            int64_t sequence_length = logits_shape[1];
            int64_t vocab_size = logits_shape[2];

            // 마지막 토큰의 로짓 추출
            std::vector<float> last_token_logits(vocab_size);
            int64_t offset = (sequence_length - 1) * vocab_size;

            for (int64_t j = 0; j < vocab_size; j++) {
                last_token_logits[j] = logits_data[offset + j];
            }

            // argmax 계산
            int64_t next_token = std::distance(
                last_token_logits.begin(),
                std::max_element(last_token_logits.begin(), last_token_logits.end())
            );

            // 종료 토큰이면 생성 중단
            if (next_token == eos_token_id) {
                break;
            }

            // 다음 토큰 추가
            input_ids.push_back(next_token);
        }

        // 결과 디코딩
        std::string generated_text = Detokenize(input_ids);
        return generated_text;
    }
};


int main(int argc, char* argv[]) {
    try {
        // 모델 및 토크나이저 경로
        std::string model_path = "path/to/model.onnx";
        std::string tokenizer_path = "path/to/tokenizer.model";

        // 커맨드 라인 인수 확인
        if (argc >= 2) model_path = argv[1];
        if (argc >= 3) tokenizer_path = argv[2];

        // 모델 초기화
        LlamaOnnxModel llama_model(model_path, tokenizer_path);

        // 프롬프트 설정
        std::string prompt = "안녕하세요, 저는 LLaMA 모델입니다. 오늘의 주제는";

        std::cout << "프롬프트: " << prompt << std::endl;
        std::cout << "생성 중..." << std::endl;

        // 텍스트 생성
        std::string output = llama_model.Generate(prompt, 100, 0.7, 0.9, 1.1);

        std::cout << "\n생성된 텍스트:\n" << output << std::endl;

    } catch (const Ort::Exception& e) {
        std::cerr << "ONNX Runtime 오류: " << e.what() << std::endl;
        return 1;
    } catch (const std::exception& e) {
        std::cerr << "오류: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}


 */