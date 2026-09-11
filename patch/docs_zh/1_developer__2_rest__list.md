
````lms_hstack
`GET /api/v1/models`

此端点没有请求参数。
:::split:::
```lms_code_snippet
title: 示例请求
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models \
        -H "Authorization: Bearer $LM_API_TOKEN"
```
````

---

````lms_hstack
**响应字段**
```lms_params
- name: models
  type: array
  description: 可用模型列表（包括 LLM 和嵌入模型）。
  children:
    - name: type
      type: '"llm" | "embedding"'
      description: 模型类型。
    - name: publisher
      type: string
      description: 模型发布者名称。
    - name: key
      type: string
      description: 模型的唯一标识符。
    - name: display_name
      type: string
      description: 人类可读的模型名称。
    - name: architecture
      type: string | null
      optional: true
      description: 模型架构（例如 "llama"、"mistral"）。嵌入模型不存在此字段。
    - name: quantization
      type: object | null
      description: 模型的量化信息。
      children:
        - name: name
          type: string | null
          description: 量化方法名称。
        - name: bits_per_weight
          type: number | null
          description: 量化每权重位数。
    - name: size_bytes
      type: number
      description: 模型大小（字节）。
    - name: params_string
      type: string | null
      description: 人类可读的参数数量（例如 "7B"、"13B"）。
    - name: loaded_instances
      type: array
      description: 该模型当前已加载的实例列表。
      children:
        - name: id
          type: string
          description: 已加载模型实例的唯一标识符。
        - name: config
          type: object
          description: 已加载实例的配置。
          children:
            - name: context_length
              type: number
              description: 模型的最大上下文长度（token 数）。
            - name: eval_batch_size
              type: number
              optional: true
              description: 评估时单批一起处理的输入 token 数。嵌入模型不存在此字段。
            - name: flash_attention
              type: boolean
              optional: true
              description: 是否启用 Flash Attention 以优化注意力计算。嵌入模型不存在此字段。
            - name: num_experts
              type: number
              optional: true
              description: MoE（混合专家）模型的专家数量。嵌入模型不存在此字段。
            - name: offload_kv_cache_to_gpu
              type: boolean
              optional: true
              description: 是否将 KV 缓存卸载到 GPU 内存。嵌入模型不存在此字段。
    - name: max_context_length
      type: number
      description: 模型支持的最大上下文长度（token 数）。
    - name: format
      type: '"gguf" | "mlx" | null'
      description: 模型文件格式。
    - name: capabilities
      type: object
      optional: true
      description: 模型能力。嵌入模型不存在此字段。
      children:
        - name: vision
          type: boolean
          description: 模型是否支持视觉/图像输入。
        - name: trained_for_tool_use
          type: boolean
          description: 模型是否针对工具/函数调用进行过训练。
    - name: description
      type: string | null
      optional: true
      description: 模型描述。嵌入模型不存在此字段。
```
:::split:::
```lms_code_snippet
title: 响应
variants:
  json:
    language: json
    code: |
      {
        "models": [
          {
            "type": "llm",
            "publisher": "lmstudio-community",
            "key": "gemma-3-270m-it-qat",
            "display_name": "Gemma 3 270m Instruct Qat",
            "architecture": "gemma3",
            "quantization": {
              "name": "Q4_0",
              "bits_per_weight": 4
            },
            "size_bytes": 241410208,
            "params_string": "270M",
            "loaded_instances": [
              {
                "id": "gemma-3-270m-it-qat",
                "config": {
                  "context_length": 4096,
                  "eval_batch_size": 512,
                  "flash_attention": false,
                  "num_experts": 0,
                  "offload_kv_cache_to_gpu": true
                }
              }
            ],
            "max_context_length": 32768,
            "format": "gguf",
            "capabilities": {
              "vision": false,
              "trained_for_tool_use": false
            },
            "description": null
          },
          {
            "type": "embedding",
            "publisher": "gaianet",
            "key": "text-embedding-nomic-embed-text-v1.5-embedding",
            "display_name": "Nomic Embed Text v1.5",
            "quantization": {
              "name": "F16",
              "bits_per_weight": 16
            },
            "size_bytes": 274290560,
            "params_string": null,
            "loaded_instances": [],
            "max_context_length": 2048,
            "format": "gguf"
          }
        ]
      }
```
````
