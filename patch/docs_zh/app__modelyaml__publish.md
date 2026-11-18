
通过把 [`model.yaml`](./) 上传到你在 LM Studio Hub 上的页面，即可分享可移植模型。

当你把 model.yaml 发布到 LM Studio Hub 后，其他用户就可以用 `lms get` 下载它。

###### 注意：`model.yaml` 仅涉及元数据。这意味着它不包含实际的模型权重。

# 快速上手

最简单的上手方式是克隆一个现有模型、修改它，然后运行 `lms push`。

例如，你可以克隆 Qwen 3 8B 模型：

```shell
lms clone qwen/qwen3-8b
```

这会在本地生成一份 `model.yaml`、`README` 及其他元数据文件的副本。重要的是，这**不会**下载模型权重。

```lms_terminal
$ ls
README.md     manifest.json    model.yaml    thumbnail.png
```

## 将发布者改为你的用户

`model:` 字段的第一部分应为发布者的用户名。把它改为你拥有写入权限的用户或组织的用户名。

```diff
- model: qwen/qwen3-8b
+ model: your-user-here/qwen3-8b
base:
  - key: lmstudio-community/qwen3-8b-gguf
    sources:
# ... the rest of the file
```

## 登录

在命令行中向 Hub 进行身份验证：

```shell
lms login
```

CLI 会打印一个身份验证 URL。在你批准访问后，会话令牌会保存在本地，之后你就可以发布模型了。

## 发布你的模型

在包含 `model.yaml` 的目录中运行 push 命令：

```shell
lms push
```

该命令会打包该文件、上传它，并为新版本打印一个修订号。

### 在发布时覆盖元数据

使用 `--overrides` 可以在不编辑文件的情况下调整字段：

```shell
lms push --overrides '{"description": "Qwen 3 8B model"}'
```

## 下载模型并在 LM Studio 中使用

发布后，该模型会出现在你在 LM Studio Hub 上的用户或组织主页下。

随后可用以下命令下载：

```shell
lms get my-user/my-model
```
