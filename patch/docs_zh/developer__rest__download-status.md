
````lms_hstack
`GET /api/v1/models/download/status/:job_id`

**路径参数**
```lms_params
- name: job_id
  type: string
  optional: false
  description: 下载任务的唯一标识符。`job_id` 由[下载](/docs/developer/rest/download)端点在发起下载时返回。
```
:::split:::
```lms_code_snippet
title: 示例请求
variants:
  curl:
    language: bash
    code: |
      curl -H "Authorization: Bearer $LM_API_TOKEN" \
        http://localhost:1234/api/v1/models/download/status/job_493c7c9ded
```
````

````lms_hstack
**响应字段**

返回单个下载任务状态对象。响应内容会随下载状态而变化。

```lms_params
- name: job_id
  type: string
  description: 下载任务的唯一标识符。
- name: status
  type: '"downloading" | "paused" | "completed" | "failed"'
  description: 下载的当前状态。
- name: bytes_per_second
  type: number
  optional: true
  description: 当前下载速度（字节/秒）。当 `status` 为 `downloading` 时存在。
- name: estimated_completion
  type: string
  optional: true
  description: 预计完成时间，ISO 8601 格式。当 `status` 为 `downloading` 时存在。
- name: completed_at
  type: string
  optional: true
  description: 下载完成时间，ISO 8601 格式。当 `status` 为 `completed` 时存在。
- name: total_size_bytes
  type: number
  optional: true
  description: 下载的总字节数。
- name: downloaded_bytes
  type: number
  optional: true
  description: 目前已下载的字节数。
- name: started_at
  type: string
  optional: true
  description: 下载开始时间，ISO 8601 格式。
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
        "status": "completed",
        "total_size_bytes": 2279145003,
        "downloaded_bytes": 2279145003,
        "started_at": "2025-10-03T15:33:23.496Z",
        "completed_at": "2025-10-03T15:43:12.102Z"
      }
```
````
