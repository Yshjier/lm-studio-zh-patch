技能（Skill）让你可以为 Bionic 提供针对某项能力、某类知识或可重复任务的可复用指令。技能采用标准的 [Agent Skills](https://agentskills.io/specification) 格式：一个包含指令和可选配套文件的 `SKILL.md` 文件。

Bionic 可以使用你安装的技能、与你共同创建的技能，以及你在 Codex、Claude Code 等其他应用中已使用的兼容技能。

<figure>

![Bionic 聊天输入框中的使用技能选项](https://lmstudio.ai/assets/marketing/blog/skills/skills-hero.png)

<figcaption>

技能为 Bionic 处理专项任务提供可复用的指引。

</figcaption>

</figure>

## 使用技能

当 Bionic 判断某个技能有帮助时，会在相关任务中自动使用。要显式触发某个技能，在聊天输入框中输入 `@`。这会打开引用面板，你可以在其中选择文件或技能。

<figure>

![Bionic 聊天输入框中的技能引用面板](https://lmstudio.ai/assets/marketing/blog/skills/at-ref.png)

<figcaption>

输入 `@` 调出技能选择器。

</figcaption>

</figure>

无论 Bionic 是自动选择技能还是你显式引用某个技能，它都会检视技能文件，并决定如何把其中的指令应用到你的任务上。

## 创建技能

Bionic 可以为你创建技能。当你完成一项效果良好的任务、想把工作流程留存以备下次使用时，这很有用。

<figure>

![让 Bionic 基于已完成的工作创建技能](https://lmstudio.ai/assets/marketing/blog/skills/create-skill-3.png)

<figcaption>

让 Bionic 基于一次成功的工作流创建技能。

</figcaption>

</figure>

例如，在完成一项可重复任务后，可以问：

> 基于我们刚才做的内容创建一个技能。

Bionic 可能会先提出澄清问题，然后起草技能，方便你在以后的会话中复用。

你也可以从零开始与 Bionic 打磨一个新技能。描述工作流程、输入、输出，以及希望智能体遵循的标准。

## 安装技能

你可以让 Bionic 从 URL 安装技能，例如 GitHub 仓库地址或技能的直链。

<figure>

![让 Bionic 从 GitHub 安装技能](https://lmstudio.ai/assets/marketing/blog/skills/install-ask.png)

<figcaption>

给 Bionic 一个 URL，并让它安装该技能。

</figcaption>

</figure>

你也可以在希望 Bionic 帮忙添加技能时调用 `@Install Skill`。

如果你已有 `SKILL.md` 文件，在**设置 → 技能**中添加，即可让 Bionic 使用它。

## 使用其他应用中的技能

Bionic 可以使用来自其他应用的兼容技能，包括 Codex 和 Claude Code。

要管理这些技能，进入**设置 → 技能 → 使用在其他应用中找到的技能**。在那里选择哪些技能对 Bionic 可见。你可以在 `•••` 菜单中禁用单个技能。

## 技能的适用场景

技能最适合具有可重复步骤、统一输出格式或专项指令的工作流。例如：

* 按清单审阅文档。
* 创建演示文稿、报告、表格或其他交付物。
* 应用团队风格指南或写作规范。
* 遵循固定的研究或分析工作流。
* 处理特定文件格式、工具或集成。

## 提示

* 明确知道希望 Bionic 应用哪个技能时，使用 `@`。
* 在完成一项预计会重复的成功任务后，让 Bionic 创建技能。
* 创建技能时包含示例、所需输出和约束条件。
* 在把新创建或安装的技能用于重要工作之前，先审阅它们。
