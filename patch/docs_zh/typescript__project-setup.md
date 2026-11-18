
`@lmstudio/sdk` 是发布在 npm 上的一个库，让你可以在自己的项目中使用 `lmstudio-js`。它是开源的，在 GitHub 上开发。你可以在[此处](https://github.com/lmstudio-ai/lmstudio-js)找到源码。

## 创建一个新的 `node` 项目

使用以下命令启动一个交互式的项目初始化：

```lms_code_snippet
  variants:
    "TypeScript（推荐）":
      language: bash
      code: |
        lms create node-typescript
    Javascript:
      language: bash
      code: |
        lms create node-javascript
```

## 把 `lmstudio-js` 添加到一个已有项目

如果你已经创建了一个项目，并希望在其中使用 `lmstudio-js`，你可以用 npm、yarn 或 pnpm 安装它。

```lms_code_snippet
  variants:
    npm:
      language: bash
      code: |
        npm install @lmstudio/sdk --save
    yarn:
      language: bash
      code: |
        yarn add @lmstudio/sdk
    pnpm:
      language: bash
      code: |
        pnpm add @lmstudio/sdk
```
