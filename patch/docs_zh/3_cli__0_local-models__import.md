
使用 `lms import` 把一个已有的模型文件带入 LM Studio，而无需下载它。

### 标志

```lms_params
- name: "<file-path>"
  type: "string"
  optional: false
  description: "要导入的模型文件的路径"
- name: "--user-repo"
  type: "string"
  optional: true
  description: "将目标文件夹设为 <user>/<repo>。跳过分类提示。"
- name: "-y, --yes"
  type: "flag"
  optional: true
  description: "跳过确认，并尝试从文件名推断模型位置"
- name: "-c, --copy"
  type: "flag"
  optional: true
  description: "复制文件，而不是移动它"
- name: "-L, --hard-link"
  type: "flag"
  optional: true
  description: "创建硬链接，而不是移动或复制文件"
- name: "-l, --symbolic-link"
  type: "flag"
  optional: true
  description: "创建符号链接，而不是移动或复制文件"
- name: "--dry-run"
  type: "flag"
  optional: true
  description: "不执行导入，只展示将要进行的操作"
```

`--copy`、`--hard-link` 或 `--symbolic-link` 三者中一次只能使用一个。如果都未提供，`lms import` 默认移动文件。

### 导入一个模型文件

```shell
lms import ~/Downloads/model.gguf
```

### 保留原文件

```shell
lms import ~/Downloads/model.gguf --copy
```

### 自行选择目标文件夹

使用 `--user-repo` 跳过提示，把模型放入所选命名空间：

```shell
lms import ~/Downloads/model.gguf --user-repo my-user/custom-models
```

### 导入前先试运行

```shell
lms import ~/Downloads/model.gguf --dry-run
```
