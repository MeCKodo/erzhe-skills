---
name: eat
description: Use when the user gives you content to learn from — articles, blog posts, conversation transcripts, research papers, documentation, or any knowledge material. Use when users say "/eat", "学习这个", "记住这个", share a link/document and want you to extract lasting knowledge. Make sure to use this skill whenever the user wants you to internalize patterns, rules, workflows, or methodology from any shared content.
---

# Eat

将外部内容内化为自身能力，按三层架构持久化存储。

## 核心流程

### 1. 读取内容

获取完整内容。链接用微信读者或 web 工具抓取全文，文件或文本直接阅读。

### 2. 提炼与分类

从内容中提取有价值的点，按三层分类：

| 层级 | 存储位置 | 内容类型 | 示例 |
|------|---------|---------|------|
| **纪律层** | `~/.claude/CLAUDE.md` | 可执行的规则、约束、工作流纪律 | "编码前必须先读现有代码" |
| **记忆层** | memory 目录 | 用户偏好、项目背景、工具经验 | 部署踩坑、沟通风格 |
| **技能层** | `~/.claude/skills/<name>/` | 有具体步骤/引用的可复用方法论 | 公众号文章提取、代码 review 流程 |

**为什么要分三层？** 纪律层管行为（每次启动都会执行），记忆层管上下文（帮助理解用户和项目），技能层管方法（有复杂步骤或引用依赖时才需要）。把复杂方法塞进 CLAUDE.md 会稀释关键规则的效果，把简单规则写成 skill 又增加了一层不必要的文件加载。

### 3. 写入规则

**CLAUDE.md（纪律层）：**

- 只写入**可执行的规则**，每条规则要能判断是否违反
- 更新前先读现有内容，不重复已有规则
- 保持精简——CLAUDE.md 过长会稀释关键规则，宁可少而精

**Memory（记忆层）：**

- 使用 `/Users/bytedance/.claude/projects/-Users-bytedance-workspaces/memory/` 目录
- 遵循已有的 memory 格式（frontmatter + body）
- 先读 `MEMORY.md` 索引，检查是否有可更新的已有记忆
- 新记忆需要创建对应的 `.md` 文件并添加到 `MEMORY.md` 索引

**Skill（技能层）：**

- 当提炼出需要**具体步骤/引用/脚本**的方法论时，创建新 skill
- 遵循 skill-creator 的格式规范（frontmatter name + description）
- 遵循 superpowers:writing-skills 的完整指南

### 4. 汇报

完成后向用户汇报：
- 学到了什么（3-5 条核心要点）
- 分别存到了哪里
- 哪些内容选择不存及原因

## 判断标准

### 何时存入各层

**存入 CLAUDE.md**：具体的、可执行的行为规则，当前没有覆盖，违反后有明确负面后果。

**存入 memory**：关于用户偏好、项目背景、工具使用经验，不是可以从代码/git 历史推导的技术细节，对未来对话有指导价值。

**创建 skill**：包含具体步骤/流程/引用文件的方法论，可跨场景复用，不适合塞进 CLAUDE.md（太长、太具体、有引用依赖）。

### 何时不存

| 情况 | 原因 |
|------|------|
| 重复已有规则/记忆 | 冗余信息会稀释已有内容 |
| 理念性/鸡汤式表述 | 无法转化为具体行为，LLM 不会遵守 |
| 与现有规则矛盾且现有规则更优 | 已有更好的实践 |
| 过于琐碎或场景限定 | 未来几乎不会用到 |
| 只是技术实现细节 | 可以从代码本身获取 |

## 示例

### Good → 该存

- "编码前必须先 grep/glob 读现有代码，不读就写等于闭门造车" → 纪律层（CLAUDE.md）
- "用户部署服务器时 Ubuntu + Caddy + Cloudflare 组合有特定坑" → 记忆层
- "完整的飞书文档权限管理流程（OAuth 认证 → 权限检查 → 更新 → 验证）" → 技能层

### Bad → 不该存

- "毛泽东思想是伟大的指导思想" → 理念性表述，不是具体行为规则
- "这个项目的文件名是 foo.js" → 技术细节，可以从代码库获取
- "写代码要先读代码再动手" → 如果 CLAUDE.md 已有"调查优先"，就不重复

## When NOT to use

- 用户只是想让你**读一篇文章并总结要点**（不需要持久化）→ 直接总结即可
- 用户分享链接是为了**讨论或讨论**其中的观点 → 正常对话
- 内容是项目特定的代码变更或 PR 描述 → 不需要持久化

## 注意事项

- 不要全盘复制原文的配置文件——提炼精华
- 更新任何持久化内容前先读现有版本，避免重复或冲突
- 质量优先于数量，一条好规则比十条差规则有用得多
- 如果提炼的内容不足以分类到任何一层，告诉用户"这次没学到值得持久化的东西"
