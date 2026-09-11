
## 背景

- `JIT loading`（即时加载）让你能轻松在其他应用中使用 LM Studio 的模型：无需先手动加载模型即可使用。但这也意味着，即便模型未被使用，也可能一直驻留在内存中。`[默认：启用]`

- （新增）`Idle TTL`（技术上称为 Time-To-Live，生存时间）定义了一个模型在未收到任何请求的情况下可以驻留内存多久。TTL 到期后，模型会自动从内存中卸载。你可以在请求负载中使用 `ttl` 字段来设置 TTL。`[默认：60 分钟]`

- （新增）`Auto-Evict`（自动驱逐）是一项在加载新模型之前先卸载此前通过 JIT 加载的模型的功能。它让客户端应用之间切换模型变得轻松，无需先手动卸载。你可以在"开发者"选项卡 > 服务器设置中启用或禁用它。`[默认：启用]`

## 空闲 TTL

**使用场景**：假设你正在使用 [Zed](https://github.com/zed-industries/zed/blob/main/crates/lmstudio/src/lmstudio.rs#L340)、[Cline](https://github.com/cline/cline/blob/main/src/api/providers/lmstudio.ts) 或 [Continue.dev](https://docs.continue.dev/customize/model-providers/more/lmstudio) 这类应用，与 LM Studio 提供的 LLM 交互。这些应用会利用 JIT，在你首次使用时按需加载模型。

**问题**：当你并未积极使用某个模型时，你可能不希望它一直驻留在内存中。

**解决方案**：为通过 API 请求加载的模型设置 TTL。空闲计时器会在模型每次收到请求时重置，因此在你使用期间它不会消失。如果模型没有执行任何工作，就被视为空闲。空闲 TTL 到期后，模型会自动从内存中卸载。

### 设置应用级默认空闲 TTL

默认情况下，通过 JIT 加载的模型 TTL 为 60 分钟。你可以为任何通过 JIT 加载的模型配置默认 TTL 值，如下所示：

<img src="/assets/marketing/docs/app-default-ttl.png" style="width: 500px; " data-caption="设置默认 TTL 值。除非在请求负载中另行指定，否则将应用于所有 JIT 加载的模型" />

### 在 API 请求中设置单模型 TTL

启用 JIT 加载后，对某个模型的**首次请求**会将其载入内存。你可以在请求负载中为该模型指定 TTL。

这对面向 [OpenAI 兼容 API](/docs/developer/openai-api) 和 [LM Studio REST API](/docs/developer/rest) 的请求均适用：

```diff
curl http://localhost:1234/api/v0/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1-distill-qwen-7b",
+   "ttl": 300,
    "messages": [ ... ]
}'
```

###### 如果该模型通过 JIT 加载，这将为其设置 5 分钟（300 秒）的 TTL。

### 为使用 `lms` 加载的模型设置 TTL

默认情况下，使用 `lms load` 加载的模型没有 TTL，会一直驻留内存，直到你手动卸载。

你可以为使用 `lms` 加载的模型设置 TTL，如下所示：

```bash
lms load <model> --ttl 3600
```

###### 以 1 小时（3600 秒）的 TTL 加载 `<model>`

### 在服务器选项卡中加载模型时指定 TTL

你也可以在服务器选项卡中加载模型时设置 TTL，如下所示

<img src="/assets/marketing/docs/ttl-server-model.png" style="width: 100%;" data-caption="在服务器选项卡中加载模型时设置 TTL 值" />

## 为 JIT 加载的模型配置自动驱逐

通过此设置，你可以确保通过 JIT 加载的新模型会先自动卸载此前加载的模型。

当你希望从另一个应用切换模型、又不希望未使用的模型不断占用内存时，这非常有用。

<img src="/assets/marketing/docs/auto-evict-and-ttl.png" style="width: 500px; margin-top:30px" data-caption="在开发者选项卡 > 服务器设置中启用或禁用 JIT 加载模型的自动驱逐" />

**当自动驱逐开启时**（默认）：

- 同一时间内存中最多保留 `1` 个模型（通过 JIT 加载时）
- 非 JIT 加载的模型不受影响

**当自动驱逐关闭时**：

- 从外部应用切换模型时，此前的模型会继续驻留内存
- 模型会一直保持加载，直到：
  - 其 TTL 到期
  - 你手动卸载它们

此功能与 TTL 协同工作，为你的工作流提供更好的内存管理。

### 术语

`TTL`：Time-To-Live，是借自网络协议和缓存系统的术语。它定义了一个资源在被视为过期并被驱逐之前可以保持分配状态多久。
