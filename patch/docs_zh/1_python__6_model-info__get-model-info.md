
你可以从一个已加载的模型实例访问关于该模型本身的一般信息和元数据。

在下面的示例中，可以把 LLM 引用替换为
嵌入模型引用，而无需任何其他改动。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()

        print(model.get_info())

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()

            print(model.get_info())

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model()

            print(await model.get_info())

```

## 示例输出

```python
LlmInstanceInfo.from_dict({
  "architecture": "qwen2",
  "contextLength": 4096,
  "displayName": "Qwen2.5 7B Instruct 1M",
  "format": "gguf",
  "identifier": "qwen2.5-7b-instruct",
  "instanceReference": "lpFZPBQjhSZPrFevGyY6Leq8",
  "maxContextLength": 1010000,
  "modelKey": "qwen2.5-7b-instruct-1m",
  "paramsString": "7B",
  "path": "lmstudio-community/Qwen2.5-7B-Instruct-1M-GGUF/Qwen2.5-7B-Instruct-1M-Q4_K_M.gguf",
  "sizeBytes": 4683073888,
  "trainedForToolUse": true,
  "type": "llm",
  "vision": false
})
```
