import json

p = 'patch/zh_dict.json'
d = json.load(open(p, encoding='utf-8'))

new_entries = {
    "LM Link is a new feature in LM Studio. It allows you to connect together devices on which you have LM Studio (or [llmster](https://lmstudio.ai/blog/0.4.0#deploy-on-servers-deploy-in-ci-deploy-anywhere)) installed. It is end-to-end encrypted, and built on top of custom Tailscale mesh VPNs.":
        "LM Link 是 LM Studio 的全新功能。它可以将安装了 LM Studio（或 [llmster](https://lmstudio.ai/blog/0.4.0#deploy-on-servers-deploy-in-ci-deploy-anywhere)）的设备连接在一起。它采用端到端加密，基于自定义的 Tailscale 网格 VPN 构建。",

    "Once devices are together in a Link, you can load models on remote devices and use them as if they were local. Chats remain local and nothing gets uploaded to LM Studio's backend servers apart from your device list - in order to facilitate device discovery and connection.":
        "设备加入同一个 Link 后，您可以在远程设备上加载模型并像本地一样使用它们。聊天数据保留在本地，除了您的设备列表之外不会上传到 LM Studio 的后端服务器——设备列表仅用于设备发现与连接。",

    "**No!** All your devices in the LM Link network communicate with each other using a mesh VPN connection powered by Tailscale. They use end-to-end encrypted connections and communicate without opening any ports to the internet.":
        "**不会！** LM Link 网络中的所有设备都通过 Tailscale 支持的网格 VPN 连接相互通信。它们使用端到端加密连接，无需向互联网开放任何端口即可通信。",

    "Moreover, LM Link runs entirely in userspace and does **not change** anything globally on your device, such as networking settings or firewall settings.":
        "此外，LM Link 完全在用户态运行，**不会**修改您设备上的任何全局设置，例如网络设置或防火墙设置。",

    "Yes. Any model in your LM Link network can be used as if it is local. Any tool that already connects to your local LM Studio server will be able to use remote models as well, just by pointing to `localhost:1234` as usual.":
        "可以。LM Link 网络中的任何模型都可以像本地模型一样使用。任何已连接到您本地 LM Studio 服务器的工具都可以使用远程模型，只需照常指向 `localhost:1234` 即可。",

    "This means that if you use LM Studio together with tools like Codex, Claude Code, OpenCode, your remote models will show up automatically in those tools as well.":
        "这意味着如果您将 LM Studio 与 Codex、Claude Code、OpenCode 等工具搭配使用，您的远程模型也会自动出现在这些工具中。",

    "No. LM Link is an entirely separate and self-contained use of Tailscale VPN primitives. LM Link coexists with other uses of Tailscale on your machine or network, with no interference or interplay. LM Studio is introducing this feature in partnership and close technical collaboration with Tailscale.":
        "不会。LM Link 是 Tailscale VPN 原语的一种完全独立、自包含的使用方式。LM Link 可与您机器或网络上的其它 Tailscale 使用共存，不会相互干扰或相互作用。LM Studio 与 Tailscale 合作并在密切技术协作下推出此功能。",

    "LM Link is a network between your devices. An account is required in order to associate your LM Link with your user, and to facilitate device discovery.":
        "LM Link 是您设备之间的网络。需要一个账号才能将您的 LM Link 与您的用户关联起来，并便于设备发现。",

    "settings:jitTTL.subtitle":
        "JIT 加载的模型在空闲指定时长后将被自动卸载。",

    "settings:defaultContextLength.customSubtitle":
        "设置加载新模型时使用的默认上下文长度。如果模型支持的最大上下文长度更小，则使用模型自身的限制值。",

    "settings:defaultContextLength.maxSubtitle":
        "使用每个模型自身支持的最大上下文长度。",

    "JIT-loaded models will be automatically unloaded after being idle for the specified duration.":
        "JIT 加载的模型在空闲指定时长后将被自动卸载。",

    "Set the default context length for loading new models. If the model's supported maximum context length is lower, that value will be used.":
        "设置加载新模型时使用的默认上下文长度。如果模型支持的最大上下文长度更小，则使用模型自身的限制值。",

    "Use the maximum context length supported by each model.":
        "使用每个模型自身支持的最大上下文长度。",

    "Invalid context length value. Using {{value}}":
        "无效的上下文长度值，将使用 {{value}}。",

    "Invalid context length value. Should be in the range of 1 and 2^30. Using {{value}}":
        "无效的上下文长度值，合法范围为 1 到 2^30。将使用 {{value}}。",

    "The higher the context length, the more memory the model will take. If you are unsure, don't change the default":
        "上下文长度越高，模型占用的内存就越多。如果有疑问，请保持默认设置。",
}

added = 0
skipped = 0
for k, v in new_entries.items():
    if k in d:
        skipped += 1
        continue
    d[k] = v
    added += 1

# 用 json.dumps(indent=1) 写, 然后后处理: 每行末加 ", " (除了 "}" 行)
text = json.dumps(d, ensure_ascii=False, indent=1)
# indent=1 给的是 "key": value, 但原文件每行尾空格 ", "
# 我们一行行处理
out_lines = []
for line in text.split('\n'):
    if line == '{' or line == '}' or line == '':
        out_lines.append(line)
        continue
    # 行如:  "key": "value"
    # 转为:  "key": "value", 
    if line.endswith(','):
        # 倒数第二项, 已带逗号
        out_lines.append(line + ' ')
    else:
        # 末项 (没有逗号) - 不加 ", "
        out_lines.append(line)
text_with_trailing = '\n'.join(out_lines)
# 强制 CRLF
text_with_trailing = text_with_trailing.replace('\r\n', '\n').replace('\n', '\r\n')

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(text_with_trailing)

# 验证 JSON 合法性
d2 = json.load(open(p, encoding='utf-8'))
print(f'before: {len(d) - added}')
print(f'after:  {len(d2)}')
print(f'added: {added}, skipped: {skipped}')

# zh_dict.js 用紧凑格式
js = "window.__ZH_DICT__=" + json.dumps(d2, ensure_ascii=False, separators=(",", ":")) + ";\n"
with open('patch/zh_dict.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print(f'zh_dict.js: {len(js)} bytes')