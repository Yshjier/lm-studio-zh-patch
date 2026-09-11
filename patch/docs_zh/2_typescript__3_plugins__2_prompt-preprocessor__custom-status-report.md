
视任务而定，提示词预处理器可能需要一些时间才能完成，例如它可能需要从互联网获取数据或执行较重的计算。这种情况下，你可以用 `ctl.setStatus` 上报预处理的状态。

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        const status = ctl.createStatus({
          status: "loading",
          text: "Preprocessing.",
        });
```

你可以随时调用 `status.setState` 更新状态。

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        status.setState({
          status: "done",
          text: "Preprocessing done.",
        })
```

你甚至可以为状态添加子状态：

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        const subStatus = status.addSubStatus({
          status: "loading",
          text: "I am a sub status."
        });
```
