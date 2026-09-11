
在插件项目中运行 `lms dev`，可启动一个在文件变化时重新构建并重载的本地开发服务器。

此功能是 LM Studio [插件](/docs/typescript/plugins)的一部分，目前处于私密 beta 阶段。

### 运行开发插件服务器

```shell
lms dev
```

这会校验 `manifest.json`，在需要时安装依赖，并启动一个在变化时重新构建插件的监视器。支持的运行器：Node/ECMAScript 和 Deno。

### 安装插件而非运行开发服务器

```shell
lms dev --install
```

### 标志

```lms_params
- name: "-i, --install"
  type: "flag"
  optional: true
  description: "将插件安装到 LM Studio，而不是运行开发服务器"
- name: "--no-notify"
  type: "flag"
  optional: true
  description: "不在 LM Studio 中显示 \"Plugin started\" 通知"
```
