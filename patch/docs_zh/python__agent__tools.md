
你可以把工具定义为普通的 Python 函数，并在 `act()` 调用中把它们传给模型。
或者，可以用 `lmstudio.ToolFunctionDef` 来定义工具，以便控制
传给语言模型的名称和描述。

## 工具的构成

按以下示例之一来把函数定义为工具（第一种方式
通常是最方便的）：

```lms_code_snippet
  variants:
    "Python 函数":
      language: python
      code: |
        # Type hinted functions with clear names and docstrings
        # may be used directly as tool definitions
        def add(a: int, b: int) -> int:
            """Given two numbers a and b, returns the sum of them."""
            # The SDK ensures arguments are coerced to their specified types
            return a + b

        # Pass `add` directly to `act()` as a tool definition

    "ToolFunctionDef.from_callable":
      language: python
      code: |
        from lmstudio import ToolFunctionDef

        def cryptic_name(a: int, b: int) -> int:
            return a + b

        # Type hinted functions with cryptic names and missing or poor docstrings
        # can be turned into clear tool definitions with `from_callable`
        tool_def = ToolFunctionDef.from_callable(
          cryptic_name,
          name="add",
          description="Given two numbers a and b, returns the sum of them."
        )
        # Pass `tool_def` to `act()` as a tool definition

    "ToolFunctionDef":
      language: python
      code: |
        from lmstudio import ToolFunctionDef

        def cryptic_name(a, b):
            return a + b

        # Functions without type hints can be used without wrapping them
        # at runtime by defining a tool function directly.
        tool_def = ToolFunctionDef(
          name="add",
          description="Given two numbers a and b, returns the sum of them.",
          parameters={
            "a": int,
            "b": int,
          },
          implementation=cryptic_name,
        )
        # Pass `tool_def` to `act()` as a tool definition

```

**重要**：工具的名称、描述以及参数定义都会被传给模型！

这意味着你的措辞会影响生成的质量。请务必始终为工具提供清晰的描述，以便模型知道如何使用它。

## 具有外部效应的工具（如操作电脑或调用 API）

工具还可以具有外部效应，例如创建文件、调用程序甚至 API。通过实现具有外部效应的工具，
你基本上可以把 LLM 变成能在你本机上执行任务的自主智能体。

## 示例：`create_file_tool`

### 工具定义

```lms_code_snippet
  title: "create_file_tool.py"
  variants:
    Python:
      language: python
      code: |
        from pathlib import Path

        def create_file(name: str, content: str):
            """Create a file with the given name and content."""
            dest_path = Path(name)
            if dest_path.exists():
                return "Error: File already exists."
            try:
                dest_path.write_text(content, encoding="utf-8")
            except Exception as exc:
                return "Error: {exc!r}"
            return "File created."

```

### 使用 `create_file` 工具的示例代码：

```lms_code_snippet
  title: "example.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms
        from create_file_tool import create_file

        model = lms.llm("qwen2.5-7b-instruct")
        model.act(
          "Please create a file named output.txt with your understanding of the meaning of life.",
          [create_file],
        )
```

## 处理工具调用错误

默认情况下，Python SDK 1.3.0 及之后的版本会自动把工具调用所抛出的
异常转换为文本，并回报给语言模型。
在很多情况下，以这种方式得知错误后，语言模型要么能够调整它的请求以避免失败，
要么能够把该失败当作对其请求的一个有效响应接受（试想这样一个提示词：`Attempt to divide 1 by 0
using the provided tool. Explain the result.`，其中预期的
响应是对 Python 解释器在被告知除以零时抛出的 `ZeroDivisionError` 异常所做的解释）。

这种错误处理行为可以用 `handle_invalid_tool_request`
回调来覆盖。例如，以下代码把错误处理回退为在客户端本地抛出异常：

```lms_code_snippet
  title: "example.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        def divide(numerator: float, denominator: float) -> float:
            """Divide the given numerator by the given denominator. Return the result."""
            return numerator / denominator

        model = lms.llm("qwen2.5-7b-instruct")
        chat = Chat()
        chat.add_user_message(
            "Attempt to divide 1 by 0 using the tool. Explain the result."
        )

        def _raise_exc_in_client(
            exc: LMStudioPredictionError, request: ToolCallRequest | None
        ) -> None:
            raise exc

        act_result = llm.act(
            chat,
            [divide],
            handle_invalid_tool_request=_raise_exc_in_client,
        )
```

当一个工具请求被传入时，回调的结果按如下方式处理：

- `None`：原始异常文本不加修改地传给 LLM
- 一个字符串：返回的字符串代替原始异常文本传给 LLM
- 抛出一个异常（无论是传入的异常还是新异常）：
  所抛出的异常在客户端本地传播，终止预测过程

如果没有工具请求被传入，该回调调用只是一个通知，
异常无法被转换为文本以回传给 LLM
（尽管它仍可被替换为另一个异常）。这些情况
表明与服务器 API 的预期通信发生了失败，意味着预测过程
无法合理地继续进行，因此如果回调没有抛出异常，调用代码将直接抛出原始异常。
