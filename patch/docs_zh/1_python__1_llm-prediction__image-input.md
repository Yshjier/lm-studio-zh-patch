
_要求的 Python SDK 版本_：**1.1.0**

有些模型（称为 VLM，视觉语言模型）可以接受图像作为输入。你可以用 `.respond()` 方法把图像传给模型。

### 前置条件：获取一个 VLM（视觉语言模型）

如果你还没有 VLM，可以用以下命令下载一个像 `qwen2-vl-2b-instruct` 这样的模型：

```bash
lms get qwen2-vl-2b-instruct
```

## 1. 实例化模型

连接到 LM Studio 并获取你想使用的 VLM（视觉语言模型）的句柄。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen2-vl-2b-instruct")

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model("qwen2-vl-2b-instruct")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model("qwen2-vl-2b-instruct")

```

## 2. 准备图像

使用 `prepare_image()` 函数或 `files` 命名空间方法，
获取一个之后可以传给模型的图像句柄。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        image_path = "/path/to/image.jpg" # Replace with the path to your image
        image_handle = lms.prepare_image(image_path)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            image_path = "/path/to/image.jpg" # Replace with the path to your image
            image_handle = client.files.prepare_image(image_path)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            image_path = "/path/to/image.jpg" # Replace with the path to your image
            image_handle = await client.files.prepare_image(image_path)

```

如果你只有图像的原始数据，你可以直接把原始数据作为 bytes 对象传入，
而无需先把它写到磁盘。由于这一特性，二进制文件系统路径_不_受支持（因为它们会被当作
格式错误的图像数据处理，而不是文件系统路径）。

二进制 IO 对象也可作为本地文件输入被接受。

LM Studio 服务器支持 JPEG、PNG 和 WebP 图像格式。

## 3. 在 `.respond()` 中把图像传给模型

通过在 `.respond()` 方法中把图像传给模型来生成预测。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        image_path = "/path/to/image.jpg" # Replace with the path to your image
        image_handle = lms.prepare_image(image_path)
        model = lms.llm("qwen2-vl-2b-instruct")
        chat = lms.Chat()
        chat.add_user_message("Describe this image please", images=[image_handle])
        prediction = model.respond(chat)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            image_path = "/path/to/image.jpg" # Replace with the path to your image
            image_handle = client.files.prepare_image(image_path)
            model = client.llm.model("qwen2-vl-2b-instruct")
            chat = lms.Chat()
            chat.add_user_message("Describe this image please", images=[image_handle])
            prediction = model.respond(chat)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            image_path = "/path/to/image.jpg" # Replace with the path to your image
            image_handle = client.files.prepare_image(image_path)
            model = await client.llm.model("qwen2-vl-2b-instruct")
            chat = lms.Chat()
            chat.add_user_message("Describe this image please", images=[image_handle])
            prediction = await model.respond(chat)

```
