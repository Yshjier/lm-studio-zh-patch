
你可以通过向 `.respond()` 方法提供一个 JSON schema 来强制 LLM 使用特定的回复格式。
这能保证模型的输出符合你提供的 schema。

JSON schema 可以直接提供，
也可以通过提供一个实现 `lmstudio.ModelSchema` 协议的对象来提供，
例如 `pydantic.BaseModel` 或 `lmstudio.BaseModel`。

`lmstudio.ModelSchema` 协议定义如下：

```python
@runtime_checkable
class ModelSchema(Protocol):
    """Protocol for classes that provide a JSON schema for their model."""

    @classmethod
    def model_json_schema(cls) -> DictSchema:
        """Return a JSON schema dict describing this model."""
        ...

```

当提供了 schema 时，预测结果的 `parsed` 字段将包含一个符合给定 schema 的字符串键字典
（对于非结构化结果，该字段是一个字符串字段，包含与 `content` 相同的值）。

## 使用基于类的 Schema 定义来强制约束

如果你希望模型生成满足给定 schema 的 JSON，
推荐使用 [`pydantic`](https://docs.pydantic.dev/) 或 [`msgspec`](https://jcristharif.com/msgspec/)
之类的库，提供一个基于类的 schema 定义。

Pydantic 模型原生实现了 `lmstudio.ModelSchema` 协议，
而 `lmstudio.BaseModel` 是 `msgspec.Struct` 的一个子类，它恰当地实现了 `.model_json_schema()`。

#### 定义基于类的 Schema

```lms_code_snippet
  variants:
    "pydantic.BaseModel":
      language: python
      code: |
        from pydantic import BaseModel

        # A class based schema for a book
        class BookSchema(BaseModel):
            title: str
            author: str
            year: int

    "lmstudio.BaseModel":
      language: python
      code: |
        from lmstudio import BaseModel

        # A class based schema for a book
        class BookSchema(BaseModel):
            title: str
            author: str
            year: int

```

#### 生成结构化回复

```lms_code_snippet
  variants:
    "非流式":
      language: python
      code: |
        result = model.respond("Tell me about The Hobbit", response_format=BookSchema)
        book = result.parsed

        print(book)
        #           ^
        # Note that `book` is correctly typed as { title: string, author: string, year: number }

    "流式":
      language: python
      code: |
        prediction_stream = model.respond_stream("Tell me about The Hobbit", response_format=BookSchema)

        # Optionally stream the response
        # for fragment in prediction:
        #   print(fragment.content, end="", flush=True)
        # print()
        # Note that even for structured responses, the *fragment* contents are still only text

        # Get the final structured result
        result = prediction_stream.result()
        book = result.parsed

        print(book)
        #           ^
        # Note that `book` is correctly typed as { title: string, author: string, year: number }
```

## 使用 JSON Schema 来强制约束

你也可以使用 JSON schema 来强制约束结构化回复。

#### 定义 JSON Schema

```python
# A JSON schema for a book
schema = {
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "author": { "type": "string" },
    "year": { "type": "integer" },
  },
  "required": ["title", "author", "year"],
}
```

#### 生成结构化回复

```lms_code_snippet
  variants:
    "非流式":
      language: python
      code: |
        result = model.respond("Tell me about The Hobbit", response_format=schema)
        book = result.parsed

        print(book)
        #     ^
        # Note that `book` is correctly typed as { title: string, author: string, year: number }

    "流式":
      language: python
      code: |
        prediction_stream = model.respond_stream("Tell me about The Hobbit", response_format=schema)

        # Stream the response
        for fragment in prediction:
            print(fragment.content, end="", flush=True)
        print()
        # Note that even for structured responses, the *fragment* contents are still only text

        # Get the final structured result
        result = prediction_stream.result()
        book = result.parsed

        print(book)
        #     ^
        # Note that `book` is correctly typed as { title: string, author: string, year: number }
```

<!--

TODO: Info about structured generation caveats

 ## Overview

Once you have [downloaded and loaded](/docs/basics/index) a large language model,
you can use it to respond to input through the API. This article covers getting JSON structured output, but you can also
[request text completions](/docs/api/sdk/completion),
[request chat responses](/docs/api/sdk/chat-completion), and
[use a vision-language model to chat about images](/docs/api/sdk/image-input).

### Usage

Certain models are trained to output valid JSON data that conforms to
a user-provided schema, which can be used programmatically in applications
that need structured data. This structured data format is supported by both
[`complete`](/docs/api/sdk/completion) and [`respond`](/docs/api/sdk/chat-completion)
methods, and relies on Pydantic in Python and Zod in TypeScript.

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        import { z } from "zod";

        const Book = z.object({
          title: z.string(),
          author: z.string(),
          year: z.number().int()
        })

        const client = new LMStudioClient()
        const llm = client.llm.model()

        const response = llm.respond(
          "Tell me about The Hobbit.",
          { structured: Book },
        )

        console.log(response.content.title)
``` -->
