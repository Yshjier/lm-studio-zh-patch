
`lmstudio-python` 为你提供了一组 API，用于与 LLM、嵌入模型和智能体（agentic）流程交互。

## 安装 SDK

`lmstudio-python` 以 PyPI 包的形式提供。你可以使用 pip 安装它。

```lms_code_snippet
  variants:
    pip:
      language: bash
      code: |
        pip install lmstudio
```

源码与开源贡献请访问 GitHub 上的 [lmstudio-python](https://github.com/lmstudio-ai/lmstudio-python)。

## 功能

- 使用 LLM [在聊天中回复](./python/llm-prediction/chat-completion) 或预测[文本补全](./python/llm-prediction/completion)
- 将函数定义为工具，把 LLM 变成完全本地运行的[自主智能体](./python/agent)
- 从内存中[加载](./python/manage-models/loading)、[配置](./python/llm-prediction/parameters)和[卸载](./python/manage-models/loading)模型
- 为文本生成嵌入，等等！

## 快速示例：与 Llama 模型聊天

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen/qwen3-4b-2507")
        result = model.respond("What is the meaning of life?")

        print(result)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model("qwen/qwen3-4b-2507")
            result = model.respond("What is the meaning of life?")

            print(result)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model("qwen/qwen3-4b-2507")
            result = await model.respond("What is the meaning of life?")

            print(result)
```

### 获取本地模型

上面的代码需要 [qwen3-4b-2507](https://lmstudio.ai/models/qwen/qwen3-4b-2507) 模型。
如果你没有该模型，请在终端中运行以下命令来下载它。

```bash
lms get qwen/qwen3-4b-2507
```

在 LM Studio 的 CLI [文档中](./cli/get)了解关于 `lms get` 的更多内容。

# 交互便捷性、确定性的资源管理，还是结构化并发？

如上例所示，使用 LM Studio Python SDK 有三种截然不同的方式。

第一种是交互式便捷 API（在示例中列为 "Python (convenience API)"），它侧重于使用一个默认的 LM Studio 客户端实例，以方便在同步的 Python 提示符下、或在使用 Jupyter notebook 时进行交互。

第二种是同步的作用域资源 API（在示例中列为 "Python (scoped resource API)"），它使用上下文管理器来确保已分配的资源（如网络连接）被确定性地释放，而不是可能一直保持打开，直到整个进程终止。

最后一种是异步结构化并发 API（在示例中列为 "Python (asynchronous API)"），它专为遵循["结构化并发"](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)设计原则的异步程序而设计，以确保处理 SDK 与 API 服务器主机连接的后台任务得到正确管理。不遵循这些设计原则的异步应用，则需要依赖对同步作用域资源 API 的线程化访问，而不能尝试使用 SDK 原生的异步 API。Python SDK 1.5.0 版是首个完全支持异步 API 的版本。

有些示例在交互式便捷 API 和同步作用域资源 API 之间是通用的。这些示例被列为 "Python (synchronous API)"。

## 同步 API 中的超时

_要求的 Python SDK 版本_：**1.5.0**

从 Python SDK 1.5.0 版开始，同步 API 在等待来自 API 服务器的响应或流式事件通知时，默认在 60 秒无活动后超时。

等待响应和事件通知的秒数可以用 `lmstudio.set_sync_api_timeout()` 函数调整。把超时设为 `None` 会完全禁用超时（恢复此前 SDK 版本的行为）。

当前的同步 API 超时可以用 `lmstudio.get_sync_api_timeout()` 函数查询。

## 异步 API 中的超时

_要求的 Python SDK 版本_：**1.5.0**

由于异步协程支持取消，异步 API 中没有实现特定的超时支持。相反，应使用通用的异步超时机制，例如 [`asyncio.wait_for()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for) 或 [`anyio.move_on_after()`](https://anyio.readthedocs.io/en/stable/cancellation.html#timeouts)。
