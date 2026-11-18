[← 首页](/README.md)

# LM Studio 文档

本仓库内容发布于 [lmstudio.ai/docs](/docs)。

## 解析规则

* docs/ 下的文件夹视为章节
* 章节文件夹下的文件视为文章
* 可以嵌套文件夹以创建子章节
* `0_root` 是一个特殊文件夹，用于存放根层级文章
* `index.md` 是特殊文件，作为章节的落地页（发布于 `/docs/<section>/`）
* 可以通过数字前缀命名来控制章节顺序（例如 `1_api`、`2_guides` 等）
* 可以通过 frontmatter 中的 `index` 字段控制文章顺序
  * `index: -1` 表示“将该文章排在列表末尾”
* 以 `_` 开头的文件和文件夹会被忽略

## 如何添加新的文档文章

1. 在对应文件夹中新建一个 markdown 文件

2. 在文件中填入如下 frontmatter：

```yaml
---
title: Keyboard Shortcuts
description: Learn about the keyboard shortcuts in LM Studio
index: 2
---
```

##### 可选地设置 `sidebar_title:` 以覆盖侧边栏中的标题

## 自定义 markdown 组件

### 示例见 `_template_dont_edit.md`

### 多语言代码片段

可在模型页面查看实际效果：[https://lmstudio.ai/model/deepseek-r1-qwen-7b](/model/deepseek-r1-qwen-7b)

效果较好的配置：

1. 标题 + 1 个变体
2. 无标题 + 2 个及以上变体

````
```typescript tab="TypeScript"
// Multi-line TypeScript code
function hello() {
  console.log("hey")
  return "world"
}
```

```python tab="Python"
# Multi-line Python code
def hello():
    print("hey")
    return "world"
```
````

````
```python title="generator.py"
# Multi-line Python code
def hello():
    print("hey")
    return "world"
```
````

### 横向堆叠（HStack）

用于把文本块放在代码块旁边（例如代码讲解或分步指南）

````
```lms_hstack

# 第一列

~~~js
console.log("Hello from the code block");
~~~

:::split:::

# 第二列
此处为第二列的 markdown 内容

```
````

### 参数（Params）

格式化参数列表

````
### Flags
```lms_params
- name: "[path]"
  type: "string"
  optional: true
  description: "要加载的模型路径。若未提供，将提示你选择一个模型"
- name: "--ttl"
  type: "number"
  optional: true
  description: "若提供，则模型在该秒数内未被使用时将被卸载"
- name: "--gpu"
  type: "string"
  optional: true
  description: "卸载到 GPU 的比例。取值：0-1、off、max"
- name: "--context-length"
  type: "number"
  optional: true
  description: "生成文本时作为上下文考虑的词元数量"
- name: "--identifier"
  type: "string"
  optional: true
  description: "为已加载模型分配的标识符，供 API 引用"
```
````
