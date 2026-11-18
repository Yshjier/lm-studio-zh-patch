
## macOS

- 芯片：Apple Silicon（M1/M2/M3/M4）。
- 需要 macOS 14.0 或更高版本。
- 建议 16GB 及以上内存。
  - 在 8GB 内存的 Mac 上你仍可能使用 LM Studio，但请坚持使用较小的模型和适中的上下文长度。
- 目前不支持 Intel 芯片的 Mac。如果你对此感兴趣，请在[此处](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/9)留言。

## Windows

LM Studio 同时支持基于 x64 和 ARM（Snapdragon X Elite）的系统。

- CPU：需要支持 AVX2 指令集（针对 x64）
- 内存：LLM 可能消耗大量内存。建议至少 16GB 内存。
- GPU：建议至少 4GB 专用显存。

## Linux

LM Studio 同时支持基于 x64 和 ARM64（aarch64）的系统。

- Linux 版 LM Studio 以 AppImage 形式分发。
- 需要 Ubuntu 20.04 或更高版本
- 比 22 更新的 Ubuntu 版本未经充分测试。如果你遇到问题，请在[此处](https://github.com/lmstudio-ai/lmstudio-bug-tracker)提交 bug 告知我们。
- CPU：
  - 在 x64 上，LM Studio 默认带 AVX2 支持
