
工具调用（Tool use）让 LLM 能够通过 `/v1/chat/completions` 和 `v1/responses` 端点（[了解更多](/docs/developer/openai-compat)）请求调用外部函数和 API，经由 LM Studio 的 REST API（或任意 OpenAI 客户端）。这将其功能远远扩展到文本输出之外。

<hr>

## 快速上手

### 1. 将 LM Studio 作为服务器启动

若要在你自己的代码中以编程方式使用 LM Studio，请将 LM Studio 作为本地服务器运行。

你可以在 LM Studio 的"开发者"选项卡中打开服务器，也可以通过 `lms` CLI：

```bash
lms server start
```

###### 运行 `npx lmstudio install-cli` 安装 `lms`

这将允许你通过 REST API 与 LM Studio 交互。关于 LM Studio REST API 的介绍，请参见 [REST API 概览](/docs/developer/rest)。

### 2. 加载模型

你可以在 LM Studio 的"聊天"或"开发者"选项卡中加载模型，也可以通过 `lms` CLI：

```bash
lms load
```

### 3. 复制、粘贴并运行一个示例！

- `Curl`
  - [单轮工具调用请求](#example-using-curl)
- `Python`
  - [单轮工具调用 + 工具使用](#single-turn-example)
  - [多轮示例](#multi-turn-example)
  - [进阶智能体示例](#advanced-agent-example)

## 工具使用

### 究竟什么是"工具使用"？

工具使用描述的是：

- LLM 输出文本，请求调用某些函数（LLM 无法直接执行代码）
- 你的代码执行这些函数
- 你的代码把结果回传给 LLM。

### 高层流程

```xml
┌──────────────────────────┐
│ SETUP: LLM + Tool list   │
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│    Get user input        │◄────┐
└──────────┬───────────────┘     │
           ▼                     │
┌──────────────────────────┐     │
│ LLM prompted w/messages  │     │
└──────────┬───────────────┘     │
           ▼                     │
     Needs tools?                │
      │         │                │
    Yes         No               │
      │         │                │
      ▼         └────────────┐   │
┌─────────────┐              │   │
│Tool Response│              │   │
└──────┬──────┘              │   │
       ▼                     │   │
┌─────────────┐              │   │
│Execute tools│              │   │
└──────┬──────┘              │   │
       ▼                     ▼   │
┌─────────────┐          ┌───────────┐
│Add results  │          │  Normal   │
│to messages  │          │ response  │
└──────┬──────┘          └─────┬─────┘
       │                       ▲
       └───────────────────────┘
```

### 深入流程

当在请求体的 `tools` 参数中提供函数定义时，LM Studio 通过 `/v1/chat/completions` 端点支持工具使用。工具以函数定义数组的形式指定，描述其参数和用法，例如：

它遵循 OpenAI 的 [函数调用](https://platform.openai.com/docs/guides/function-calling) API 的相同格式，预期可通过 OpenAI 客户端 SDK 使用。

本示例流程中我们将使用 [lmstudio-community/Qwen2.5-7B-Instruct-GGUF](https://model.lmstudio.ai/download/lmstudio-community/Qwen2.5-7B-Instruct-GGUF) 作为模型。

1. 你向 LLM 提供一个工具列表。这些是模型可以_请求_调用的工具。
   例如：

```json
// the list of tools is model-agnostic
[
  {
    "type": "function",
    "function": {
      "name": "get_delivery_date",
      "description": "Get the delivery date for a customer's order",
      "parameters": {
        "type": "object",
        "properties": {
          "order_id": {
            "type": "string"
          }
        },
        "required": ["order_id"]
      }
    }
  }
]
```

该列表会根据模型的聊天模板被注入到模型的 `system` 提示中。对于 `Qwen2.5-Instruct`，它看起来像这样：

```json
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{"type": "function", "function": {"name": "get_delivery_date", "description": "Get the delivery date for a customer's order", "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}}}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call><|im_end|>
```

**重要**：模型只能_请求_调用这些工具，因为 LLM _无法_直接调用函数、API 或任何其他工具。它们只能输出文本，随后可以对文本进行解析，以编程方式调用这些函数。

2. 被提示后，LLM 可以决定：
   - (a) 调用一个或多个工具

   ```xml
   User: Get me the delivery date for order 123
   Model: <tool_call>
   {"name": "get_delivery_date", "arguments": {"order_id": "123"}}
   </tool_call>
   ```

   - (b) 正常回复

   ```xml
   User: Hi
   Model: Hello! How can I assist you today?
   ```

3. LM Studio 把模型输出的文本解析为符合 OpenAI 规范的 `chat.completion` 响应对象。
   - 如果模型被赋予了 `tools` 的访问权，LM Studio 会尝试把工具调用解析进 `chat.completion` 响应对象的 `response.choices[0].message.tool_calls` 字段。
   - 如果 LM Studio 无法解析出任何**格式正确**的工具调用，它会直接把响应返回到标准的 `response.choices[0].message.content` 字段。
   - **注意**：较小的模型以及未针对工具使用训练过的模型可能会输出格式不正确的工具调用，导致 LM Studio 无法将其解析进 `tool_calls` 字段。当你没有按预期收到 `tool_calls` 时，这对排错很有用。以下是一个格式不正确的 `Qwen2.5-Instruct` 工具调用示例：

   ```xml
   <tool_call>
   ["name": "get_delivery_date", function: "date"]
   </tool_call>
   ```

   > 请注意，这里的括号是错误的，且该调用不符合 `name, argument` 格式。

4. 你的代码解析 `chat.completion` 响应，检查来自模型的工具调用，然后以模型指定的参数调用相应的工具。接着你的代码把以下两项都加入 `messages` 数组并回传给模型：
   1. 模型的工具调用消息
   2. 工具调用的结果

   ```python
   # pseudocode, see examples for copy-paste snippets
   if response.has_tool_calls:
       for each tool_call:
           # Extract function name & args
           function_to_call = tool_call.name     # e.g. "get_delivery_date"
           args = tool_call.arguments            # e.g. {"order_id": "123"}

           # Execute the function
           result = execute_function(function_to_call, args)

           # Add result to conversation
           add_to_messages([
               ASSISTANT_TOOL_CALL_MESSAGE,      # The request to use the tool
               TOOL_RESULT_MESSAGE               # The tool's response
           ])
   else:
       # Normal response without tools
       add_to_messages(response.content)
   ```

5. 随后 LLM 会在更新后的 messages 数组（但不带工具访问权）下再次被提示。这是因为：
   - LLM 已经在对话历史中拥有工具结果
   - 我们希望 LLM 向用户给出最终回复，而不是继续调用更多工具
   ```python
   # Example messages
   messages = [
       {"role": "user", "content": "When will order 123 be delivered?"},
       {"role": "assistant", "function_call": {
           "name": "get_delivery_date",
           "arguments": {"order_id": "123"}
       }},
       {"role": "tool", "content": "2024-03-15"},
   ]
   response = client.chat.completions.create(
       model="lmstudio-community/qwen2.5-7b-instruct",
       messages=messages
   )
   ```
   这次调用之后的 `response.choices[0].message.content` 字段可能类似于：
   ```xml
   Your order #123 will be delivered on March 15th, 2024
   ```
6. 循环回到流程的第 2 步继续

注意：这是工具使用中较为 `pedantic`（严格）的流程。不过，你完全可以按最适合自己用例的方式进行调整。

## 支持的模型

通过 LM Studio，**所有**模型都支持至少某种程度的工具使用。

不过，目前有两个支持级别，可能会影响使用体验的质量：原生（Native）与默认（Default）。

具有原生工具使用支持的模型会在应用中带有锤子徽章，并且在工具使用场景中通常表现更好。

### 原生工具使用支持

"原生"工具使用支持意味着以下两者同时成立：

1. 模型具有支持工具使用的聊天模板（通常意味着该模型针对工具使用进行了训练）
   - 这正是用于把 `tools` 数组格式化进系统提示、并告诉模型如何格式化工具调用的依据
   - 示例：[Qwen2.5-Instruct 聊天模板](https://huggingface.co/mlx-community/Qwen2.5-7B-Instruct-4bit/blob/c26a38f6a37d0a51b4e9a1eb3026530fa35d9fed/tokenizer_config.json#L197)
2. LM Studio 支持该模型的工具使用格式
   - 这是 LM Studio 把聊天历史正确输入到聊天模板、并把模型输出的工具调用解析进 `chat.completion` 对象的必要条件

目前在 LM Studio 中具有原生工具使用支持的模型（可能变动）：

- Qwen
  - `GGUF` [lmstudio-community/Qwen2.5-7B-Instruct-GGUF](https://model.lmstudio.ai/download/lmstudio-community/Qwen2.5-7B-Instruct-GGUF) (4.68 GB)
  - `MLX` [mlx-community/Qwen2.5-7B-Instruct-4bit](https://model.lmstudio.ai/download/mlx-community/Qwen2.5-7B-Instruct-4bit) (4.30 GB)
- Llama-3.1、Llama-3.2
  - `GGUF` [lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF](https://model.lmstudio.ai/download/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF) (4.92 GB)
  - `MLX` [mlx-community/Meta-Llama-3.1-8B-Instruct-8bit](https://model.lmstudio.ai/download/mlx-community/Meta-Llama-3.1-8B-Instruct-8bit) (8.54 GB)
- Mistral
  - `GGUF` [bartowski/Ministral-8B-Instruct-2410-GGUF](https://model.lmstudio.ai/download/bartowski/Ministral-8B-Instruct-2410-GGUF) (4.67 GB)
  - `MLX` [mlx-community/Ministral-8B-Instruct-2410-4bit](https://model.lmstudio.ai/download/mlx-community/Ministral-8B-Instruct-2410-4bit) (4.67 GB GB)

### 默认工具使用支持

"默认"工具使用支持意味着以下**之一**成立：

1. 模型没有支持工具使用的聊天模板（通常意味着该模型未针对工具使用进行训练）
2. LM Studio 目前不支持该模型的工具使用格式

在底层，默认工具使用的实现方式是：

- 给模型一个自定义系统提示和默认的工具调用格式
- 把 `tool` 角色消息转换为 `user` 角色，以便不含 `tool` 角色的聊天模板兼容
- 把 `assistant` 角色的 `tool_calls` 转换为默认工具调用格式

结果会因模型而异。

你可以在终端中运行 `lms log stream`，然后向一个不支持原生工具使用的模型发送带 `tools` 的聊天补全请求，来查看默认格式。默认格式可能变动。

<details>
<summary>展开查看默认工具调用格式的示例</summary>

```bash
-> % lms log stream
Streaming logs from LM Studio

timestamp: 11/13/2024, 9:35:15 AM
type: llm.prediction.input
modelIdentifier: gemma-2-2b-it
modelPath: lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf
input: "<start_of_turn>system
You are a tool-calling AI. You can request calls to available tools with this EXACT format:
[TOOL_REQUEST]{"name": "tool_name", "arguments": {"param1": "value1"}}[END_TOOL_REQUEST]

AVAILABLE TOOLS:
{
  "type": "toolArray",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_delivery_date",
        "description": "Get the delivery date for a customer's order",
        "parameters": {
          "type": "object",
          "properties": {
            "order_id": {
              "type": "string"
            }
          },
          "required": [
            "order_id"
          ]
        }
      }
    }
  ]
}

RULES:
- Only use tools from AVAILABLE TOOLS
- Include all required arguments
- Use one [TOOL_REQUEST] block per tool
- Never use [TOOL_RESULT]
- If you decide to call one or more tools, there should be no other text in your message

Examples:
"Check Paris weather"
[TOOL_REQUEST]{"name": "get_weather", "arguments": {"location": "Paris"}}[END_TOOL_REQUEST]

"Send email to John about meeting and open browser"
[TOOL_REQUEST]{"name": "send_email", "arguments": {"to": "John", "subject": "meeting"}}[END_TOOL_REQUEST]
[TOOL_REQUEST]{"name": "open_browser", "arguments": {}}[END_TOOL_REQUEST]

Respond conversationally if no matching tools exist.<end_of_turn>
<start_of_turn>user
Get me delivery date for order 123<end_of_turn>
<start_of_turn>model
"
```

如果模型完全按照该格式来调用工具，即：

```
[TOOL_REQUEST]{"name": "get_delivery_date", "arguments": {"order_id": "123"}}[END_TOOL_REQUEST]
```

那么 LM Studio 就能像对原生支持的模型那样，把这些工具调用解析进 `chat.completions` 对象。

</details>

所有不具备原生工具使用支持的模型都会有默认工具使用支持。

## Example using `curl`

此示例演示模型如何使用 `curl` 工具请求一次工具调用。

在 Mac 或 Linux 上运行此示例，可使用任意终端。在 Windows 上，请使用 [Git Bash](https://git-scm.com/download/win)。

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "lmstudio-community/qwen2.5-7b-instruct",
    "messages": [{"role": "user", "content": "What dell products do you have under $50 in electronics?"}],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "search_products",
          "description": "Search the product catalog by various criteria. Use this whenever a customer asks about product availability, pricing, or specifications.",
          "parameters": {
            "type": "object",
            "properties": {
              "query": {
                "type": "string",
                "description": "Search terms or product name"
              },
              "category": {
                "type": "string",
                "description": "Product category to filter by",
                "enum": ["electronics", "clothing", "home", "outdoor"]
              },
              "max_price": {
                "type": "number",
                "description": "Maximum price in dollars"
              }
            },
            "required": ["query"],
            "additionalProperties": false
          }
        }
      }
    ]
  }'
```

`/v1/chat/completions` 识别的所有参数都会被遵循，可用工具的数组应在 `tools` 字段中提供。

如果模型认为用户消息最好通过工具调用来满足，那么响应字段 `choices[0].message.tool_calls` 中会提供一个工具调用请求对象数组。

顶层响应对象的 `finish_reason` 字段也会被填充为 `"tool_calls"`。

对上述 `curl` 请求的一个示例响应如下：

```bash
{
  "id": "chatcmpl-gb1t1uqzefudice8ntxd9i",
  "object": "chat.completion",
  "created": 1730913210,
  "model": "lmstudio-community/qwen2.5-7b-instruct",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "tool_calls",
      "message": {
        "role": "assistant",
        "tool_calls": [
          {
            "id": "365174485",
            "type": "function",
            "function": {
              "name": "search_products",
              "arguments": "{\"query\":\"dell\",\"category\":\"electronics\",\"max_price\":50}"
            }
          }
        ]
      }
    }
  ],
  "usage": {
    "prompt_tokens": 263,
    "completion_tokens": 34,
    "total_tokens": 297
  },
  "system_fingerprint": "lmstudio-community/qwen2.5-7b-instruct"
}
```

用大白话说，上述响应可以理解为模型在说：

> "请调用 `search_products` 函数，参数为：
>
> - `query` 参数传 'dell'，
> - `category` 参数传 'electronics'
> - `max_price` 参数传 '50'
>
> 然后把结果给我"

`tool_calls` 字段需要被解析后才能调用真正的函数/API。下面的示例演示了如何做到。

## Examples using `python`

工具使用与 python 这类编程语言搭配时大放异彩，你可以在其中实现 `tools` 字段所指定的函数，在模型请求时以编程方式调用它们。

### Single-turn example

下面是一个简单的单轮（模型只被调用一次）示例，让模型能够调用一个名为 `say_hello` 的函数，该函数会向控制台打印一句问候：

`single-turn-example.py`

```python
from openai import OpenAI

# Connect to LM Studio
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Define a simple function
def say_hello(name: str) -> str:
    print(f"Hello, {name}!")

# Tell the AI about our function
tools = [
    {
        "type": "function",
        "function": {
            "name": "say_hello",
            "description": "Says hello to someone",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The person's name"
                    }
                },
                "required": ["name"]
            }
        }
    }
]

# Ask the AI to use our function
response = client.chat.completions.create(
    model="lmstudio-community/qwen2.5-7b-instruct",
    messages=[{"role": "user", "content": "Can you say hello to Bob the Builder?"}],
    tools=tools
)

# Get the name the AI wants to use a tool to say hello to
# (Assumes the AI has requested a tool call and that tool call is say_hello)
tool_call = response.choices[0].message.tool_calls[0]
name = eval(tool_call.function.arguments)["name"]

# Actually call the say_hello function
say_hello(name) # Prints: Hello, Bob the Builder!

```

在控制台中运行此脚本应得到类似以下的结果：

```xml
-> % python single-turn-example.py
Hello, Bob the Builder!
```

试着修改下面代码中的名字

```python
messages=[{"role": "user", "content": "Can you say hello to Bob the Builder?"}]
```

看看模型如何用不同的名字调用 `say_hello` 函数。

### Multi-turn example

现在来看一个稍微复杂一些的示例。

在这个示例中，我们将：

1. 让模型能够调用 `get_delivery_date` 函数
2. 把调用该函数的结果回传给模型，以便它能以纯文本方式满足用户的请求

<details>
<summary><code>multi-turn-example.py</code>（点击展开）</summary>

```python
from datetime import datetime, timedelta
import json
import random
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "lmstudio-community/qwen2.5-7b-instruct"


def get_delivery_date(order_id: str) -> datetime:
    # Generate a random delivery date between today and 14 days from now
    # in a real-world scenario, this function would query a database or API
    today = datetime.now()
    random_days = random.randint(1, 14)
    delivery_date = today + timedelta(days=random_days)
    print(
        f"\nget_delivery_date function returns delivery date:\n\n{delivery_date}",
        flush=True,
    )
    return delivery_date


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_delivery_date",
            "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID.",
                    },
                },
                "required": ["order_id"],
                "additionalProperties": False,
            },
        },
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user.",
    },
    {
        "role": "user",
        "content": "Give me the delivery date and time for order number 1017",
    },
]

# LM Studio
response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
)

print("\nModel response requesting tool call:\n", flush=True)
print(response, flush=True)

# Extract the arguments for get_delivery_date
# Note this code assumes we have already determined that the model generated a function call.
tool_call = response.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)

order_id = arguments.get("order_id")

# Call the get_delivery_date function with the extracted order_id
delivery_date = get_delivery_date(order_id)

assistant_tool_call_request_message = {
    "role": "assistant",
    "tool_calls": [
        {
            "id": response.choices[0].message.tool_calls[0].id,
            "type": response.choices[0].message.tool_calls[0].type,
            "function": response.choices[0].message.tool_calls[0].function,
        }
    ],
}

# Create a message containing the result of the function call
function_call_result_message = {
    "role": "tool",
    "content": json.dumps(
        {
            "order_id": order_id,
            "delivery_date": delivery_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
    ),
    "tool_call_id": response.choices[0].message.tool_calls[0].id,
}

# Prepare the chat completion call payload
completion_messages_payload = [
    messages[0],
    messages[1],
    assistant_tool_call_request_message,
    function_call_result_message,
]

# Call the OpenAI API's chat completions endpoint to send the tool call result back to the model
# LM Studio
response = client.chat.completions.create(
    model=model,
    messages=completion_messages_payload,
)

print("\nFinal model response with knowledge of the tool call result:\n", flush=True)
print(response.choices[0].message.content, flush=True)

```

</details>

在控制台中运行此脚本应得到类似以下的结果：

```xml
-> % python multi-turn-example.py

Model response requesting tool call:

ChatCompletion(id='chatcmpl-wwpstqqu94go4hvclqnpwn', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='377278620', function=Function(arguments='{"order_id":"1017"}', name='get_delivery_date'), type='function')]))], created=1730916196, model='lmstudio-community/qwen2.5-7b-instruct', object='chat.completion', service_tier=None, system_fingerprint='lmstudio-community/qwen2.5-7b-instruct', usage=CompletionUsage(completion_tokens=24, prompt_tokens=223, total_tokens=247, completion_tokens_details=None, prompt_tokens_details=None))

get_delivery_date function returns delivery date:

2024-11-19 13:03:17.773298

Final model response with knowledge of the tool call result:

Your order number 1017 is scheduled for delivery on November 19, 2024, at 13:03 PM.
```

### Advanced agent example

在上述原则的基础上，我们可以把 LM Studio 模型与本地定义的函数结合起来，创建一个"智能体（agent）"——一个把语言模型与自定义函数配对、以理解请求并执行超出基础文本生成的动作的系统。

下面示例中的智能体可以：

1. 在你的默认浏览器中打开安全的 URL
2. 检查当前时间
3. 分析你文件系统中的目录

<details>
<summary><code>agent-chat-example.py</code>（点击展开）</summary>

```python
import json
from urllib.parse import urlparse
import webbrowser
from datetime import datetime
import os
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
model = "lmstudio-community/qwen2.5-7b-instruct"


def is_valid_url(url: str) -> bool:

    try:
        result = urlparse(url)
        return bool(result.netloc)  # Returns True if there's a valid network location
    except Exception:
        return False


def open_safe_url(url: str) -> dict:
    # List of allowed domains (expand as needed)
    SAFE_DOMAINS = {
        "lmstudio.ai",
        "github.com",
        "google.com",
        "wikipedia.org",
        "weather.com",
        "stackoverflow.com",
        "python.org",
        "docs.python.org",
    }

    try:
        # Add http:// if no scheme is present
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Validate URL format
        if not is_valid_url(url):
            return {"status": "error", "message": f"Invalid URL format: {url}"}

        # Parse the URL and check domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        base_domain = ".".join(domain.split(".")[-2:])

        if base_domain in SAFE_DOMAINS:
            webbrowser.open(url)
            return {"status": "success", "message": f"Opened {url} in browser"}
        else:
            return {
                "status": "error",
                "message": f"Domain {domain} not in allowed list",
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_current_time() -> dict:
    """Get the current system time with timezone information"""
    try:
        current_time = datetime.now()
        timezone = datetime.now().astimezone().tzinfo
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        return {
            "status": "success",
            "time": formatted_time,
            "timezone": str(timezone),
            "timestamp": current_time.timestamp(),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def analyze_directory(path: str = ".") -> dict:
    """Count and categorize files in a directory"""
    try:
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "file_types": {},
            "total_size_bytes": 0,
        }

        for entry in os.scandir(path):
            if entry.is_file():
                stats["total_files"] += 1
                ext = os.path.splitext(entry.name)[1].lower() or "no_extension"
                stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                stats["total_size_bytes"] += entry.stat().st_size
            elif entry.is_dir():
                stats["total_dirs"] += 1
                # Add size of directory contents
                for root, _, files in os.walk(entry.path):
                    for file in files:
                        try:
                            stats["total_size_bytes"] += os.path.getsize(os.path.join(root, file))
                        except (OSError, FileNotFoundError):
                            continue

        return {"status": "success", "stats": stats, "path": os.path.abspath(path)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


tools = [
    {
        "type": "function",
        "function": {
            "name": "open_safe_url",
            "description": "Open a URL in the browser if it's deemed safe",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to open",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current system time with timezone information",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_directory",
            "description": "Analyze the contents of a directory, counting files and folders",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to analyze. Defaults to current directory if not specified.",
                    },
                },
                "required": [],
            },
        },
    },
]


def process_tool_calls(response, messages):
    """Process multiple tool calls and return the final response and updated messages"""
    # Get all tool calls from the response
    tool_calls = response.choices[0].message.tool_calls

    # Create the assistant message with tool calls
    assistant_tool_call_message = {
        "role": "assistant",
        "tool_calls": [
            {
                "id": tool_call.id,
                "type": tool_call.type,
                "function": tool_call.function,
            }
            for tool_call in tool_calls
        ],
    }

    # Add the assistant's tool call message to the history
    messages.append(assistant_tool_call_message)

    # Process each tool call and collect results
    tool_results = []
    for tool_call in tool_calls:
        # For functions with no arguments, use empty dict
        arguments = (
            json.loads(tool_call.function.arguments)
            if tool_call.function.arguments.strip()
            else {}
        )

        # Determine which function to call based on the tool call name
        if tool_call.function.name == "open_safe_url":
            result = open_safe_url(arguments["url"])
        elif tool_call.function.name == "get_current_time":
            result = get_current_time()
        elif tool_call.function.name == "analyze_directory":
            path = arguments.get("path", ".")
            result = analyze_directory(path)
        else:
            # llm tried to call a function that doesn't exist, skip
            continue

        # Add the result message
        tool_result_message = {
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id,
        }
        tool_results.append(tool_result_message)
        messages.append(tool_result_message)

    # Get the final response
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    return final_response


def chat():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can open safe web links, tell the current time, and analyze directory contents. Use these capabilities whenever they might be helpful.",
        }
    ]

    print(
        "Assistant: Hello! I can help you open safe web links, tell you the current time, and analyze directory contents. What would you like me to do?"
    )
    print("(Type 'quit' to exit)")

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Check for quit command
        if user_input.lower() == "quit":
            print("Assistant: Goodbye!")
            break

        # Add user message to conversation
        messages.append({"role": "user", "content": user_input})

        try:
            # Get initial response
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
            )

            # Check if the response includes tool calls
            if response.choices[0].message.tool_calls:
                # Process all tool calls and get final response
                final_response = process_tool_calls(response, messages)
                print("\nAssistant:", final_response.choices[0].message.content)

                # Add assistant's final response to messages
                messages.append(
                    {
                        "role": "assistant",
                        "content": final_response.choices[0].message.content,
                    }
                )
            else:
                # If no tool call, just print the response
                print("\nAssistant:", response.choices[0].message.content)

                # Add assistant's response to messages
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    }
                )

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            exit(1)


if __name__ == "__main__":
    chat()

```

</details>

在控制台中运行此脚本即可与智能体对话：

```xml
-> % python agent-example.py
Assistant: Hello! I can help you open safe web links, tell you the current time, and analyze directory contents. What would you like me to do?
(Type 'quit' to exit)

You: What time is it?

Assistant: The current time is 14:11:40 (EST) as of November 6, 2024.

You: What time is it now?

Assistant: The current time is 14:13:59 (EST) as of November 6, 2024.

You: Open lmstudio.ai

Assistant: The link to lmstudio.ai has been opened in your default web browser.

You: What's in my current directory?

Assistant: Your current directory at `/Users/matt/project` contains a total of 14 files and 8 directories. Here's the breakdown:

- Files without an extension: 3
- `.mjs` files: 2
- `.ts` (TypeScript) files: 3
- Markdown (`md`) file: 1
- JSON files: 4
- TOML file: 1

The total size of these items is 1,566,990,604 bytes.

You: Thank you!

Assistant: You're welcome! If you have any other questions or need further assistance, feel free to ask.

You:
```

### Streaming

当通过 `/v1/chat/completions`（`stream=true`）进行流式输出时，工具调用会分块发送。函数名和参数会通过 `chunk.choices[0].delta.tool_calls.function.name` 和 `chunk.choices[0].delta.tool_calls.function.arguments` 分片发送。

例如，要调用 `get_current_weather(location="San Francisco")`，每个 `chunk.choices[0].delta.tool_calls[0]` 对象中流式输出的 `ChoiceDeltaToolCall` 会像这样：

```py
ChoiceDeltaToolCall(index=0, id='814890118', function=ChoiceDeltaToolCallFunction(arguments='', name='get_current_weather'), type='function')
ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='{"', name=None), type=None)
ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='location', name=None), type=None)
ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='":"', name=None), type=None)
ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='San Francisco', name=None), type=None)
ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='"}', name=None), type=None)
```

这些分块必须在整个流中累积，才能形成完整的函数签名以供执行。

下面的示例展示了如何通过 `/v1/chat/completions` 流式端点（`stream=true`）创建一个简单的、带工具增强的聊天机器人。

<details>
<summary><code>tool-streaming-chatbot.py</code>（点击展开）</summary>

```python
from openai import OpenAI
import time

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODEL = "lmstudio-community/qwen2.5-7b-instruct"

TIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current time, only if asked",
        "parameters": {"type": "object", "properties": {}},
    },
}

def get_current_time():
    return {"time": time.strftime("%H:%M:%S")}

def process_stream(stream, add_assistant_label=True):
    """Handle streaming responses from the API"""
    collected_text = ""
    tool_calls = []
    first_chunk = True

    for chunk in stream:
        delta = chunk.choices[0].delta

        # Handle regular text output
        if delta.content:
            if first_chunk:
                print()
                if add_assistant_label:
                    print("Assistant:", end=" ", flush=True)
                first_chunk = False
            print(delta.content, end="", flush=True)
            collected_text += delta.content

        # Handle tool calls
        elif delta.tool_calls:
            for tc in delta.tool_calls:
                if len(tool_calls) <= tc.index:
                    tool_calls.append({
                        "id": "", "type": "function",
                        "function": {"name": "", "arguments": ""}
                    })
                tool_calls[tc.index] = {
                    "id": (tool_calls[tc.index]["id"] + (tc.id or "")),
                    "type": "function",
                    "function": {
                        "name": (tool_calls[tc.index]["function"]["name"] + (tc.function.name or "")),
                        "arguments": (tool_calls[tc.index]["function"]["arguments"] + (tc.function.arguments or ""))
                    }
                }
    return collected_text, tool_calls

def chat_loop():
    messages = []
    print("Assistant: Hi! I am an AI agent empowered with the ability to tell the current time (Type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})

        # Get initial response
        response_text, tool_calls = process_stream(
            client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=[TIME_TOOL],
                stream=True,
                temperature=0.2
            )
        )

        if not tool_calls:
            print()

        text_in_first_response = len(response_text) > 0
        if text_in_first_response:
            messages.append({"role": "assistant", "content": response_text})

        # Handle tool calls if any
        if tool_calls:
            tool_name = tool_calls[0]["function"]["name"]
            print()
            if not text_in_first_response:
                print("Assistant:", end=" ", flush=True)
            print(f"**Calling Tool: {tool_name}**")
            messages.append({"role": "assistant", "tool_calls": tool_calls})

            # Execute tool calls
            for tool_call in tool_calls:
                if tool_call["function"]["name"] == "get_current_time":
                    result = get_current_time()
                    messages.append({
                        "role": "tool",
                        "content": str(result),
                        "tool_call_id": tool_call["id"]
                    })

            # Get final response after tool execution
            final_response, _ = process_stream(
                client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    stream=True
                ),
                add_assistant_label=False
            )

            if final_response:
                print()
                messages.append({"role": "assistant", "content": final_response})

if __name__ == "__main__":
    chat_loop()
```

</details>

在控制台中运行此脚本即可与机器人对话：

```xml
-> % python tool-streaming-chatbot.py
Assistant: Hi! I am an AI agent empowered with the ability to tell the current time (Type 'quit' to exit)

You: Tell me a joke, then tell me the current time

Assistant: Sure! Here's a light joke for you: Why don't scientists trust atoms? Because they make up everything.

Now, let me get the current time for you.

**Calling Tool: get_current_time**

The current time is 18:49:31. Enjoy your day!

You:
```

## 社区

与其他 LM Studio 用户交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。
