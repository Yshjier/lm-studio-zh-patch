
你可以通过向 `.respond()` 方法提供一个 schema（JSON 或 `zod`）来强制 LLM 使用特定的回复格式。这能保证模型的输出符合你提供的 schema。

## 使用 `zod` Schema 来强制约束

如果你希望模型生成满足给定 schema 的 JSON，推荐使用
[`zod`](https://zod.dev/) 来提供该 schema。当提供了 `zod` schema 时，预测结果将包含一个额外的 `parsed` 字段，其中是解析、校验并带有类型的结果。

#### 定义 `zod` Schema

```ts
import { z } from "zod";

// A zod schema for a book
const bookSchema = z.object({
  title: z.string(),
  author: z.string(),
  year: z.number().int(),
});
```

#### 生成结构化回复

```lms_code_snippet
  variants:
    "非流式":
      language: typescript
      code: |
        const result = await model.respond("Tell me about The Hobbit.",
          { structured: bookSchema },
          maxTokens: 100, // Recommended to avoid getting stuck
        );

        const book = result.parsed;
        console.info(book);
        //           ^
        // Note that `book` is now correctly typed as { title: string, author: string, year: number }

    "流式":
      language: typescript
      code: |
        const prediction = model.respond("Tell me about The Hobbit.",
          { structured: bookSchema },
          maxTokens: 100, // Recommended to avoid getting stuck
        );

        for await (const { content } of prediction) {
          process.stdout.write(content);
        }
        process.stdout.write("\n");

        // Get the final structured result
        const result = await prediction.result();
        const book = result.parsed;

        console.info(book);
        //           ^
        // Note that `book` is now correctly typed as { title: string, author: string, year: number }
```

## 使用 JSON Schema 来强制约束

你也可以使用 JSON schema 来强制约束结构化回复。

#### 定义 JSON Schema

```ts
// A JSON schema for a book
const schema = {
  type: "object",
  properties: {
    title: { type: "string" },
    author: { type: "string" },
    year: { type: "integer" },
  },
  required: ["title", "author", "year"],
};
```

#### 生成结构化回复

```lms_code_snippet
  variants:
    "非流式":
      language: typescript
      code: |
        const result = await model.respond("Tell me about The Hobbit.", {
          structured: {
            type: "json",
            jsonSchema: schema,
          },
          maxTokens: 100, // Recommended to avoid getting stuck
        });

        const book = JSON.parse(result.content);
        console.info(book);
    "流式":
      language: typescript
      code: |
        const prediction = model.respond("Tell me about The Hobbit.", {
          structured: {
            type: "json",
            jsonSchema: schema,
          },
          maxTokens: 100, // Recommended to avoid getting stuck
        });

        for await (const { content } of prediction) {
          process.stdout.write(content);
        }
        process.stdout.write("\n");

        const result = await prediction.result();
        const book = JSON.parse(result.content);

        console.info("Parsed", book);
```

```lms_warning
结构化生成的工作原理是约束模型只生成符合所提供 schema 的 token。这保证了正常情况下输出的有效性，但带来两个重要的限制：

1. 模型（尤其是较小的模型）有时可能会卡在未闭合的结构中（如一个未闭合的方括号），此时它们"忘记"自己处于这种结构中，又因 schema 要求而无法停止。因此，推荐始终包含一个 `maxTokens` 参数以防止无限生成。

2. Schema 一致性只对完整、成功的生成有保证。如果生成被中断（因取消、达到 `maxTokens` 上限或其他原因），输出很可能违反 schema。使用 `zod` schema 输入时，这会抛出一个错误；使用 JSON schema 时，你会收到一个不满足 schema 的无效字符串。
```

<!-- ## Overview

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
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        import { z } from "zod";

        const Book = z.object({
          title: z.string(),
          author: z.string(),
          year: z.number().int()
        })

        const client = new LMStudioClient();
        const llm = await client.llm.model();

        const response = await llm.respond(
          "Tell me about The Hobbit.",
          { structured: Book },
        )

        console.log(response.content.title)
``` -->
