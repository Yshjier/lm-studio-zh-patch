
使用 `lms login` 让 CLI 通过 LM Studio Hub 进行身份验证。

### 使用浏览器登录

```shell
lms login
```

CLI 会打开一个浏览器窗口进行身份验证。如果无法自动打开浏览器，请把打印出的 URL 复制到浏览器中。

### 使用预认证密钥进行"CI 风格"登录

```bash
lms login --with-pre-authenticated-keys \
  --key-id <KEY_ID> \
  --public-key <PUBLIC_KEY> \
  --private-key <PRIVATE_KEY>
```

### 高级标志

```lms_params
- name: "--with-pre-authenticated-keys"
  type: "flag"
  optional: true
  description: "使用预生成的密钥进行身份验证（CI/CD）。需要 --key-id、--public-key 和 --private-key。"
- name: "--key-id"
  type: "string"
  optional: true
  description: "与 --with-pre-authenticated-keys 配合使用的 key ID"
- name: "--public-key"
  type: "string"
  optional: true
  description: "与 --with-pre-authenticated-keys 配合使用的公钥"
- name: "--private-key"
  type: "string"
  optional: true
  description: "与 --with-pre-authenticated-keys 配合使用的私钥"
```
