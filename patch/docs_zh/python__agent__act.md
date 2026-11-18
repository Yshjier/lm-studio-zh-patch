
## 自动工具调用

我们引入执行"轮次"（round）的概念，用来描述运行一个工具、把其输出提供给 LLM、然后等待 LLM 决定下一步做什么这一组合过程。

**执行轮次**

```
 • run a tool ->
 ↑   • provide the result to the LLM ->
 │       • wait for the LLM to generate a response
 │
 └────────────────────────────────────────┘ └➔ (return)
```

一个模型可能会选择在返回最终结果之前多次运行工具。例如，如果 LLM 在写代码，它可能会选择编译或运行程序、修复错误，然后再运行一次，如此反复，直到得到想要的结果。

基于这一点，我们说 `.act()` API 是一个自动的"多轮"工具调用 API。

### 快速示例

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        def multiply(a: float, b: float) -> float:
            """Given two numbers a and b. Returns the product of them."""
            return a * b

        model = lms.llm("qwen2.5-7b-instruct")
        model.act(
          "What is the result of 12345 multiplied by 54321?",
          [multiply],
          on_message=print,
        )
```

### 对 LLM 来说"使用工具"意味着什么？

LLM 基本上是文本进、文本出的程序。所以你可能会问"LLM 怎么能使用工具呢？"。答案是：有些 LLM 经过训练，会请求人类替它调用工具，并期望工具的输出以某种格式回传给它。

想象你在通过电话为某人提供电脑技术支持。你可能会说"帮我运行这条命令……好，它输出了什么？……好，现在点那里，然后告诉我它显示了什么……"。在这种情况下，你就是那个 LLM！而你是通过电话另一端的人间接地"调用工具"。

### 并行运行多个工具调用

默认情况下，Python SDK 1.4.0 及之后的版本一次只运行一个工具调用请求，
即便模型在单条回复消息中请求了多个工具调用。这能确保请求
被正确处理，即使工具实现并不支持多个并发调用。

当已知工具实现是线程安全的，并且既足够慢又足够频繁、值得并行运行时，
`max_parallel_tool_calls` 选项指定了从单条模型回复中最多会有多少个工具调用请求
被并行处理。该值默认为 1（等待每个工具调用完成后再开始下一个）。把该值设为 `None` 会自动把
并行工具调用的最大数量扩展为进程可用 CPU 核心数的某一倍数。

### 重要：模型选择

为工具使用所选的模型会极大影响性能。

选择模型时的一些通用指导：

- 并非所有模型都能进行智能的工具使用
- 越大越好（即，7B 参数模型的表现通常优于 3B 参数模型）
- 我们观察到 [Qwen2.5-7B-Instruct](https://model.lmstudio.ai/download/lmstudio-community/Qwen2.5-7B-Instruct-GGUF) 在各种各样的场景中表现良好
- 此指导可能会变化

### 示例：多个工具

以下代码演示了如何在单次 `.act()` 调用中提供多个工具。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import math
        import lmstudio as lms

        def add(a: int, b: int) -> int:
            """Given two numbers a and b, returns the sum of them."""
            return a + b

        def is_prime(n: int) -> bool:
            """Given a number n, returns True if n is a prime number."""
            if n < 2:
                return False
            sqrt = int(math.sqrt(n))
            for i in range(2, sqrt):
                if n % i == 0:
                    return False
            return True

        model = lms.llm("qwen2.5-7b-instruct")
        model.act(
          "Is the result of 12345 + 45668 a prime? Think step by step.",
          [add, is_prime],
          on_message=print,
        )
```

### 示例：带创建文件工具的聊天循环

以下代码创建了一个与能够创建文件的 LLM 智能体的对话循环。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import readline # Enables input line editing
        from pathlib import Path

        import lmstudio as lms

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

        def print_fragment(fragment, round_index=0):
            # .act() supplies the round index as the second parameter
            # Setting a default value means the callback is also
            # compatible with .complete() and .respond().
            print(fragment.content, end="", flush=True)

        model = lms.llm()
        chat = lms.Chat("You are a task focused AI assistant")

        while True:
            try:
                user_input = input("You (leave blank to exit): ")
            except EOFError:
                print()
                break
            if not user_input:
                break
            chat.add_user_message(user_input)
            print("Bot: ", end="", flush=True)
            model.act(
                chat,
                [create_file],
                on_message=chat.append,
                on_prediction_fragment=print_fragment,
            )
            print()

```

### 进度回调

与使用工具的智能体进行的复杂交互可能需要一些时间来处理。

任何预测请求的常规进度回调都可使用，
但预期的能力与单轮预测的那些回调不同。

- `on_prompt_processing_progress`：在每一轮预测的提示词处理期间调用。
  以位置参数的形式接收进度比例（浮点数）和轮次索引。
- `on_first_token`：在每一轮预测的提示词处理完成后调用。
  以唯一参数的形式接收轮次索引。
- `on_prediction_fragment`：对客户端收到的每个预测片段调用。
  以位置参数的形式接收预测片段和轮次索引。
- `on_message`：在每一轮预测完成时，用一个助手回复消息调用；
  并在每个工具调用请求完成时，用工具结果消息调用。
  用于把收到的消息追加到一个聊天历史实例，因此
  _不_接收轮次索引作为参数。

以下额外回调可用于监视预测轮次：

- `on_round_start`：在每一轮提交预测请求之前调用。
  以唯一参数的形式接收轮次索引。
- `on_prediction_completed`：在该轮的预测完成之后、
  但任何被请求的工具调用启动之前调用。以唯一参数的形式接收该轮的预测
  结果。一轮预测结果是一个带额外 `round_index` 属性的常规预测结果。
- `on_round_end`：在该轮的任何工具调用请求都已解决之后调用。

最后，应用可以在智能体发出无效工具请求时请求通知：

- `handle_invalid_tool_request`：在一个工具请求无法被处理时调用。
  接收即将被报告的异常，以及导致该问题的原始工具
  请求。当没有工具请求被给出时，这纯粹是一个不可恢复错误的通知，
  在智能体交互抛出给定异常之前发生（允许应用改为抛出自己的异常）。
  当有工具请求被给出时，它表示异常的文本描述不是要在本地抛出，
  而是将作为该失败工具请求的结果回传给智能体。
  在这些情况下，回调可以要么返回 `None` 以表示错误描述应发送给智能体，
  要么在本地抛出给定异常（或另一个异常），要么返回一个文本
  字符串，代替错误描述发送给智能体。

关于定义工具的更多细节，以及一个覆盖无效
工具请求处理、改为在本地抛出所有异常而不是把它们回传给智能体的示例，
参见[工具定义](./tools.md)。
