
````lms_hstack
`POST /api/v1/models/download`

**请求体**
```lms_params
- name: model
  type: string
  optional: false
  description: 要下载的模型。接受[模型目录](https://lmstudio.ai/models)标识符（例如 `openai/gpt-oss-20b`）和精确的 Hugging Face 链接（例如 `https://huggingface.co/lmstudio-community/gpt-oss-20b-GGUF`）
- name: quantization
  type: string
  optional: true
  description: 要下载的模型的量化级别（例如 `Q4_K_M`）。仅支持 Hugging Face 链接。
```
:::split:::
```lms_code_snippet
title: 示例请求
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/download \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro"
        }'
```
````

````lms_hstack
**响应字段**

返回下载任务状态对象。响应内容会随下载状态而变化。

```lms_params
- name: job_id
  type: string
  optional: true
  description: 下载任务的唯一标识符。当 `status` 为 `already_downloaded` 时不存在。
- name: status
  type: '"downloading" | "paused" | "completed" | "failed" | "already_downloaded"'
  description: 下载的当前状态。
- name: completed_at
  type: string
  optional: true
  description: 下载完成时间，ISO 8601 格式。当 `status` 为 `completed` 时存在。
- name: total_size_bytes
  type: number
  optional: true
  description: 下载的总字节数。当 `status` 为 `already_downloaded` 时不存在。
- name: started_at
  type: string
  optional: true
  description: 下载开始时间，ISO 8601 格式。当 `status` 为 `already_downloaded` 时不存在。
```
:::split:::
```lms_code_snippet
title: 响应
variants:
  json:
    language: json
    code: |
      {
        "job_id": "job_493c7c9ded",
        "status": "downloading",
        "total_size_bytes": 2279145003,
        "started_at": "2025-10-03T15:33:23.496Z"
      }
```
````
