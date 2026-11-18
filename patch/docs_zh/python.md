`lmstudio-python` 提供一组 API，用于与 LLM、嵌入模型及智能体流程交互。

## 安装 SDK

`lmstudio-python` 以 PyPI 包形式发布，可以用 pip 安装。

```bash
pip install lmstudio
```

源码与开源贡献请访问 GitHub 上的 [lmstudio-python](https://github.com/lmstudio-ai/lmstudio-python)。

## 功能

* 使用 LLM 在[对话中回复](/docs/python/llm-prediction/chat-completion)或预测[文本补全](/docs/python/llm-prediction/completion)
* 把函数定义为工具，将 LLM 变成完全在本地运行的[自主智能体](/docs/python/agent)
* 从内存中[加载](/docs/python/manage-models/loading)、[配置](/docs/python/llm-prediction/parameters)和[卸载](/docs/python/manage-models/loading)模型
* 为文本生成嵌入向量等更多能力！

## 快速示例：与 Llama 模型对话

```lms_code_snippet
variants:
  Python（便捷 API）:
    language: python
    code: |-
      import lmstudio as lms

      model = lms.llm("qwen/qwen3-4b-2507")
      result = model.respond("What is the meaning of life?")

      print(result)
  Python（作用域资源 API）:
    language: python
    code: |-
      import lmstudio as lms

      with lms.Client() as client:
          model = client.llm.model("qwen/qwen3-4b-2507")
          result = model.respond("What is the meaning of life?")

          print(result)
  Python（异步 API）:
    language: python
    code: >-
      # Note: assumes use of an async function or the "python -m asyncio"
      asynchronous REPL

      # Requires Python SDK version 1.5.0 or later

      import lmstudio as lms


      async with lms.AsyncClient() as client:
          model = await client.llm.model("qwen/qwen3-4b-2507")
          result = await model.respond("What is the meaning of life?")

          print(result)

```

### 获取本地模型

上面的代码需要 [qwen3-4b-2507](/models/qwen/qwen3-4b-2507) 模型。
如果还没有该模型，在终端运行以下命令下载。

```bash
lms get qwen/qwen3-4b-2507
```

关于 `lms get` 的更多说明，见 LM Studio CLI [此处](/docs/cli/local-models/get)。

# 交互式便捷、确定性资源管理，还是结构化并发？

如上例所示，使用 LM Studio Python SDK 有三种不同方式。

第一种是交互式便捷 API（示例中标注为“Python（便捷 API）”），侧重于使用默认的 LM Studio 客户端实例，以便在同步 Python 提示符或 Jupyter 笔记本中便捷交互。

第二种是同步作用域资源 API（示例中标注为“Python（作用域资源 API）”），使用上下文管理器确保已分配资源（如网络连接）被确定性释放，而不是可能一直保持打开直到整个进程终止。

最后一种是异步结构化并发 API（示例中标注为“Python（异步 API）”），面向遵循[“结构化并发”](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)设计原则的异步程序，以确保处理 SDK 与 API 服务器主机连接的后台任务得到正确管理。不遵循这些设计原则的异步应用，需要通过线程访问同步作用域资源 API，而不应尝试使用 SDK 的原生异步 API。Python SDK 1.5.0 是首个完整支持异步 API 的版本。

部分示例同时适用于交互式便捷 API 和同步作用域资源 API。这些示例标注为“Python（同步 API）”。

## 同步 API 中的超时

*所需 Python SDK 版本*：**1.5.0**

从 Python SDK 1.5.0 开始，同步 API 在等待 API 服务器响应或流式事件通知时，若 60 秒无活动则默认超时。

等待响应和事件通知的秒数可通过 `lmstudio.set_sync_api_timeout()` 函数调整。把超时设为 `None` 可完全禁用超时（恢复旧版 SDK 的行为）。

当前同步 API 超时可通过 `lmstudio.get_sync_api_timeout()` 函数查询。

## 异步 API 中的超时

*所需 Python SDK 版本*：**1.5.0**

由于异步协程支持取消，异步 API 未实现专门的超时支持。应改用通用的异步超时机制，例如 [`asyncio.wait_for()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for) 或 [`anyio.move_on_after()`](https://anyio.readthedocs.io/en/stable/cancellation.html#timeouts)。
