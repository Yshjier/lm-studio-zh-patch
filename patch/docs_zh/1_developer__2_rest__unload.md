
````lms_hstack
`POST /api/v1/models/unload`

**请求体**
```lms_params
- name: instance_id
  type: string
  optional: false
  description: 要卸载的模型实例的唯一标识符。
```
:::split:::
```lms_code_snippet
title: 示例请求
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/models/unload \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "instance_id": "openai/gpt-oss-20b"
        }'
```
````

---

````lms_hstack
**响应字段**
```lms_params
- name: instance_id
  type: string
  description: 已卸载模型实例的唯一标识符。
```
:::split:::
```lms_code_snippet
title: 响应
variants:
  json:
    language: json
    code: |
      {
        "instance_id": "openai/gpt-oss-20b"
      }
```
````
