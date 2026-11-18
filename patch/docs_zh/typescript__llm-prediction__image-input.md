
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
    "示例":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model("qwen2-vl-2b-instruct");
```

## 2. 准备图像

使用 `client.files.prepareImage()` 方法获取一个之后可以传给模型的图像句柄。

```lms_code_snippet
  variants:
    "示例":
      language: typescript
      code: |
        const imagePath = "/path/to/image.jpg"; // Replace with the path to your image
        const image = await client.files.prepareImage(imagePath);

```

如果你只有 base64 字符串形式的图像，可以改用 `client.files.prepareImageBase64()` 方法。

```lms_code_snippet
  variants:
    "示例":
      language: typescript
      code: |
        const imageBase64 = "Your base64 string here";
        const image = await client.files.prepareImageBase64(imageBase64);
```

LM Studio 服务器支持 JPEG、PNG 和 WebP 图像格式。

## 3. 在 `.respond()` 中把图像传给模型

通过在 `.respond()` 方法中把图像传给模型来生成预测。

```lms_code_snippet
  variants:
    "示例":
      language: typescript
      code: |
        const prediction = model.respond([
          { role: "user", content: "Describe this image please", images: [image] },
        ]);
```
