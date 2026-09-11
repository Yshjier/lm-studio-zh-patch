
---

###### LM Studio 0.4.1

### Anthropic 兼容 API

- 新增 Anthropic 兼容端点：`POST /v1/messages`。
  - 在 LM Studio 中使用 Claude 代码模型
  - 详见文档：[/docs/developer/anthropic-compat](/docs/developer/anthropic-compat)。

---

###### LM Studio 0.4.0

### LM Studio 原生 v1 REST API

- LM Studio 原生 v1 REST API 正式发布，提供 `/api/v1/*` 端点。
  - [通过 API 使用 MCP](/docs/developer/core/mcp)
  - [有状态对话](/docs/developer/rest/stateful-chats)
  - [身份验证](/docs/developer/core/authentication)以及 API 令牌配置
  - 模型[下载](/docs/developer/rest/download)、[加载](/docs/developer/rest/load)和[卸载](/docs/developer/rest/unload)端点
  - 更多细节见[概览](/docs/developer/rest)页面，以及与 OpenAI 兼容端点的[对比](/docs/developer/rest#inference-endpoint-comparison)。

---

###### LM Studio 0.3.29 • 2025‑10‑06

### OpenAI `/v1/responses` 与变体列表

- 新增 OpenAI 兼容端点：`POST /v1/responses`。
  - 通过 `previous_response_id` 实现有状态交互。
  - 自定义工具调用与远程 MCP 支持（可选）。
  - 针对 `openai/gpt‑oss‑20b` 通过 `reasoning.effort` 支持推理。
  - 当 `stream: true` 时通过 SSE 流式输出。
- CLI：`lms ls --variants` 可列出多变体模型的所有变体。
- 文档：[/docs/developer/openai-compat](/docs/developer/openai-compat)。完整发行说明：[/blog/lmstudio-v0.3.29](/blog/lmstudio-v0.3.29)。

---

###### LM Studio 0.3.27 • 2025‑09‑24

### CLI：模型资源估算、状态与中断

- 新增：`lms load --estimate-only <model>` 会在加载前打印预估的 GPU 与总内存占用。遵循 `--context-length` 与 `--gpu`，并采用改进的估算器，现已将 flash attention 与视觉模型纳入计算。
- `lms chat`：按 `Ctrl+C` 可中断正在进行的预测。
- `lms ps --json` 现在会报告每个模型的生成状态以及排队中的预测请求数量。
- 改善了 CLI 在浅色模式下的颜色对比度。
- 见文档：[/docs/cli/local-models/load](/docs/cli/local-models/load)。完整发行说明：[/blog/lmstudio-v0.3.27](/blog/lmstudio-v0.3.27)。

---

###### LM Studio 0.3.26 • 2025‑09‑15

### CLI 日志流：服务器 + 模型

- `lms log stream` 现在支持多个来源与过滤条件。
  - `--source server` 流式输出 HTTP 服务器日志（启动、端点、状态）
  - `--source model --filter input,output` 流式输出格式化后的用户输入与模型输出
  - 追加 `--json` 可获得机器可读日志；`--stats` 会附加 tokens/秒 及相关指标（模型来源）
- 见用法与示例：[/docs/cli/serve/log-stream](/docs/cli/serve/log-stream)。完整发行说明：[/blog/lmstudio-v0.3.26](/blog/lmstudio-v0.3.26)。

---

###### LM Studio 0.3.25 • 2025‑09‑04

### 新增模型支持（API）

- 通过 OpenAI 兼容端点新增对 NVIDIA Nemotron‑Nano‑v2 的支持，包含工具调用 [‡](/blog/lmstudio-v0.3.25)。
- 为 `/v1/embeddings` 端点新增对 Google EmbeddingGemma 的支持 [‡](/blog/lmstudio-v0.3.25)。

---

###### LM Studio 0.3.24 • 2025‑08‑28

### Seed‑OSS 工具调用与模板修复

- 新增对 ByteDance/Seed‑OSS 的支持，包括 OpenAI 兼容 API 中的工具调用与提示词模板兼容性修复 [‡](/blog/lmstudio-v0.3.24)。
- 修复了某些提示词模板下工具调用未被解析的问题 [‡](/blog/lmstudio-v0.3.24)。

---

###### LM Studio 0.3.23 • 2025‑08‑12

### 推理内容与工具调用可靠性

- 对于 `POST /v1/chat/completions` 上的 `gpt‑oss`，推理内容从 `message.content` 移出，改为放入 `choices.message.reasoning`（非流式）与 `choices.delta.reasoning`（流式），与 `o3‑mini` 对齐 [‡](/blog/lmstudio-v0.3.23)。
- 工具名称在提供给模型前会被规范化（如 snake_case），以提升工具调用的可靠性 [‡](/blog/lmstudio-v0.3.23)。
- 修复了某些含工具的 `POST /v1/chat/completions` 请求报错（如 "reading 'properties'"）以及非流式工具调用失败的问题 [‡](/blog/lmstudio-v0.3.23)。

---

###### LM Studio 0.3.19 • 2025‑07‑21

### 流式输出与工具调用的缺陷修复

- 修正了 OpenAI 兼容流式响应返回的用量统计 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.19#:~:text=,OpenAI%20streaming%20responses%20were%20incorrect)。
- 改进了通过流式 API 处理并行工具调用的方式 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.19#:~:text=,API%20were%20not%20handled%20correctly)。
- 修复了某些 Mistral 模型工具调用的解析 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.19#:~:text=,Ryzen%20AI%20PRO%20300%20series)。

---

###### LM Studio 0.3.18 • 2025‑07‑10

### 流式选项与工具调用改进

- 为 OpenAI 兼容端点新增 `stream_options` 对象支持。将 `stream_options.include_usage` 设为 `true` 会在流式输出期间返回提示词与补全的 token 用量 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.18#:~:text=%2A%20Added%20support%20for%20%60,to%20support%20more%20prompt%20templates)。
- 流式端点返回的错误现在遵循 OpenAI 客户端期望的正确格式 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.18#:~:text=,with%20proper%20chat%20templates)。
- 为使用正确对话模板的 Mistral v13 tokenizer 模型新增工具调用支持 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.18#:~:text=,with%20proper%20chat%20templates)。
- `response_format.type` 字段现在在对话补全请求中接受 `"text"` [‡](https://lmstudio.ai/blog/lmstudio-v0.3.18#:~:text=,that%20are%20split%20across%20multiple)。
- 修复了跨多个分块被拆分的并行工具调用被丢弃，以及工具定义中根级 `$defs` 被剥离的缺陷 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.18#:~:text=,being%20stripped%20in%20tool%20definitions)。

---

###### LM Studio 0.3.17 • 2025‑06‑25

### 工具调用可靠性与 token 计数更新

- token 计数现在包含系统提示词与工具定义 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.17#:~:text=,have%20a%20URL%20in%20the)。这使 UI 与 API 的用量报告都更加准确。
- 工具调用参数 token 在生成时即时流式输出 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.17#:~:text=Build%206)，提升了使用流式函数调用时的响应速度。
- 多项修复提升了 MCP 与工具调用的可靠性，包括正确处理省略 `parameters` 对象的工具，以及防止 MCP 服务器重载时卡死 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.17#:~:text=,tool%20calls%20would%20hang%20indefinitely)。

---

###### LM Studio 0.3.16 • 2025‑05‑23

### `GET /models` 中的模型能力

- OpenAI 兼容 REST API（`/api/v0`）现在会在 `GET /models` 响应中返回 `capabilities` 数组。每个模型都会列出其支持的能力（如 `"tool_use"`）[‡](https://lmstudio.ai/blog/lmstudio-v0.3.16#:~:text=,response)，使客户端可以程序化地发现支持工具的模型。
- 修复了一个流式缺陷：在首批流式工具调用数据包之后会追加空函数名字符串 [‡](https://lmstudio.ai/blog/lmstudio-v0.3.16#:~:text=%2A%20Bugfix%3A%20%5BOpenAI,packet%20of%20streamed%20function%20calls)。

---

###### [👾 LM Studio 0.3.15](/blog/lmstudio-v0.3.15) • 2025-04-24

### 改进的工具使用 API 支持

类 OpenAI REST API 现在支持 `tool_choice` 参数：

```json
{
  "tool_choice": "auto" // or "none", "required"
}
```

- `"tool_choice": "none"` — 模型不会调用工具
- `"tool_choice": "auto"` — 由模型自行决定
- `"tool_choice": "required"` — 模型必须调用工具（仅 llama.cpp）

分块响应现在会在适当时候设置 `"finish_reason": "tool_calls"`。

---

###### [👾 LM Studio 0.3.14](/blog/lmstudio-v0.3.14) • 2025-03-27

### [API/SDK] 预设支持

RESTful API 与 SDK 支持在请求中指定预设。

_(示例待补充)_

###### [👾 LM Studio 0.3.10](/blog/lmstudio-v0.3.10) • 2025-02-18

### 推测解码 API

通过 `"draft_model"` 在 API 请求中启用推测解码：

```json
{
  "model": "deepseek-r1-distill-qwen-7b",
  "draft_model": "deepseek-r1-distill-qwen-0.5b",
  "messages": [ ... ]
}
```

响应现在会包含用于推测解码的 `stats` 对象：

```json
"stats": {
  "tokens_per_second": ...,
  "draft_model": "...",
  "total_draft_tokens_count": ...,
  "accepted_draft_tokens_count": ...,
  "rejected_draft_tokens_count": ...,
  "ignored_draft_tokens_count": ...
}
```

---

###### [👾 LM Studio 0.3.9](blog/lmstudio-v0.3.9) • 2025-01-30

### 空闲 TTL 与自动驱逐

为通过 API 请求加载的模型设置 TTL（单位：秒）（文档文章：[空闲 TTL 与自动驱逐](/docs/developer/core/ttl-and-auto-evict)）

```diff
curl http://localhost:1234/api/v0/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1-distill-qwen-7b",
    "messages": [ ... ]
+   "ttl": 300,
}'
```

使用 `lms`：

```
lms load --ttl <seconds>
```

### 对话补全响应中独立的 `reasoning_content`

对于 DeepSeek R1 模型，可在单独的字段中获取推理内容。详见[此处](/blog/lmstudio-v0.3.9#separate-reasoningcontent-in-chat-completion-responses)。

在「应用设置 > 开发者」中开启。

---

###### [👾 LM Studio 0.3.6](blog/lmstudio-v0.3.6) • 2025-01-06

### 工具与函数调用 API

通过类 OpenAI API 使用任何支持工具使用与函数调用的 LLM。

文档：[工具使用与函数调用](/docs/developer/core/tools)。

---

###### [👾 LM Studio 0.3.5](blog/lmstudio-v0.3.5) • 2024-10-22

### 推出 `lms get`：从终端下载模型

你现在可以用关键词直接从终端下载模型

```bash
lms get deepseek-r1
```

或使用完整的 Hugging Face URL

```bash
lms get <hugging face url>
```

要只筛选 MLX 模型，在命令中加 `--mlx`。

```bash
lms get deepseek-r1 --mlx
```
