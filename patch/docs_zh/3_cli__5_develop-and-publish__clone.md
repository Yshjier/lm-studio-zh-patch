
使用 `lms clone` 把 LM Studio Hub 上的一个制品复制到你的机器上。

### 标志

```lms_params
- name: "<artifact>"
  type: "string"
  optional: false
  description: "形如 owner/name 的制品标识符"
- name: "[path]"
  type: "string"
  optional: true
  description: "目标文件夹。默认为以制品命名的、新创建的文件夹。"
```

如果未提供路径，`lms clone owner/name` 会在当前目录下创建一个名为 `name` 的文件夹。如果目标路径已存在，命令会退出。

### 克隆最新修订版

```shell
lms clone alice/sample-plugin
```

### 克隆到指定目录

```shell
lms clone alice/sample-plugin ./my-folder
```
