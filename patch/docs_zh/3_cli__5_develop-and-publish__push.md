
在[插件](/docs/typescript/plugins)、[预设](/docs/app/presets)或 [`model.yaml`](/docs/app/modelyaml) 项目中运行 `lms push`，即可发布一个新的修订版。如果存在 `model.yaml`，CLI 会在推送前为你生成一个 `manifest.json`。

对于插件，除非你传入 `-y`，否则 CLI 会请求确认。

### 发布当前文件夹

```shell
lms push
```

### 标志

```lms_params
- name: "--description"
  type: "string"
  optional: true
  description: "覆盖本次推送的制品描述"
- name: "--overrides"
  type: "string"
  optional: true
  description: "用于覆盖 manifest 字段的 JSON 字符串（用 JSON.parse 解析）"
- name: "-y, --yes"
  type: "flag"
  optional: true
  description: "抑制确认和警告"
- name: "--private"
  type: "flag"
  optional: true
  description: "首次发布时把制品标记为私有"
- name: "--write-revision"
  type: "flag"
  optional: true
  description: "把返回的修订号写入 manifest.json"
```

### 高级

#### 静默发布并把修订号保留在 manifest.json 中

```shell
lms push -y --write-revision
```

#### 覆盖本次上传的元数据

```shell
lms push --description "New beta build" --overrides '{"tags": ["beta"]}'
```
