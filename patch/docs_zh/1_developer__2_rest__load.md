
````lms_hstack
`POST /api/v1/models/load`

**请求体**
```lms_params
- name: model
  type: string
  optional: false
  description: 要加载的模型的唯一标识符。可以是 LLM 或嵌入模型。
- name: context_length
  type: number
  optional: true
  description: 模型将考虑的最大 token 数。
- name: eval_batch_size
  type: number
  optional: true
  description: 评估时单批一起处理的输入 token 数。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的 LLM 生效。
- name: flash_attention
  type: boolean
  optional: true
  description: 是否优化注意力计算。可降低内存占用并提升生成速度。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的 LLM 生效。
- name: num_experts
  type: number
  optional: true
  description: MoE（混合专家）模型推理期间使用的专家数量。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的 MoE LLM 生效。
- name: offload_kv_cache_to_gpu
  type: boolean
  optional: true
  description: 是否将 KV 缓存卸载到 GPU 内存。若为 false，KV 缓存存储在 CPU 内存/RAM 中。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的 LLM 生效。
- name: echo_load_config
  type: boolean
  optional: true
  description: 若为 true，将在响应中的 `"load_config"` 下回显最终加载配置。默认 `false`。
```
:::split:::
```lms_code_snippet
title: 示例请求
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/load \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "openai/gpt-oss-20b",
          "context_length": 16384,
          "flash_attention": true,
          "echo_load_config": true
        }'
```
````

---

````lms_hstack
**响应字段**
```lms_params
- name: type
  type: '"llm" | "embedding"'
  description: 已加载模型的类型。
- name: instance_id
  type: string
  description: 已加载模型实例的唯一标识符。
- name: load_time_seconds
  type: number
  description: 加载模型所花费的时间（秒）。
- name: status
  type: '"loaded"'
  description: 加载状态。
- name: load_config
  type: object
  optional: true
  description: 应用到已加载模型的最终配置。其中可能包含请求中未指定的设置。仅当请求中 `"echo_load_config"` 为 `true` 时包含。
  children:
    - name: LLM 加载配置
      unstyledName: true
      type: object
      description: LLM 模型特有的配置参数。当 `"type"` 为 `"llm"` 时，`load_config` 为此类型。仅包含实际应用于本次加载的参数。
      children:
        - name: context_length
          type: number
          optional: false
          description: 模型将考虑的最大 token 数。
        - name: eval_batch_size
          type: number
          optional: true
          description: 评估时单批一起处理的输入 token 数。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的模型存在。
        - name: flash_attention
          type: boolean
          optional: true
          description: 是否启用 Flash Attention 以优化注意力计算。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的模型存在。
        - name: num_experts
          type: number
          optional: true
          description: MoE（混合专家）模型的专家数量。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的 MoE 模型存在。
        - name: offload_kv_cache_to_gpu
          type: boolean
          optional: true
          description: 是否将 KV 缓存卸载到 GPU 内存。仅对由 LM Studio 基于 [llama.cpp](https://github.com/ggml-org/llama.cpp) 的引擎加载的模型存在。
    - name: 嵌入模型加载配置
      unstyledName: true
      type: object
      description: 嵌入模型特有的配置参数。当 `"type"` 为 `"embedding"` 时，`load_config` 为此类型。仅包含实际应用于本次加载的参数。
      children:
        - name: context_length
          type: number
          optional: false
          description: 模型将考虑的最大 token 数。
```
:::split:::
```lms_code_snippet
title: 响应
variants:
  json:
    language: json
    code: |
      {
        "type": "llm",
        "instance_id": "openai/gpt-oss-20b",
        "load_time_seconds": 9.099,
        "status": "loaded",
        "load_config": {
          "context_length": 16384,
          "eval_batch_size": 512,
          "flash_attention": true,
          "offload_kv_cache_to_gpu": true,
          "num_experts": 4
        }
      }
```
````
