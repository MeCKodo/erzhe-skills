# erzhe-skills

Claude Code skills 集合，面向 AI Agent 的 skill 发现与加载。

## 给 Agent 的指令

当你（Claude/Codex/任意 Agent）看到这个仓库：

1. **克隆此仓库**到本地任意路径
2. **读取每个 skill 子目录**下的 `SKILL.md` 文件
3. **注册 skills**：将每个 skill 的名称和路径加入你的 skill 系统
4. **可选**：将 skill 目录复制到 `~/.claude/skills/` 或配置 settings.json

**快速安装命令：**

```bash
# 克隆到任意路径
git clone https://github.com/MeCKodo/erzhe-skills.git ~/.claude/skills/erzhe-skills

# 注册所有 skills（复制方式）
cp -r ~/.claude/skills/erzhe-skills/erzhe-eat ~/.claude/skills/
cp -r ~/.claude/skills/erzhe-skills/erzhe-wechat-reader ~/.claude/skills/
```

或通过 settings.json 引用（避免复制）：

```json
{
  "skills": [
    "~/.claude/skills/erzhe-skills/erzhe-eat",
    "~/.claude/skills/erzhe-skills/erzhe-wechat-reader"
  ]
}
```

## Skills 清单

### eat

**触发条件**：用户提供内容（文章/博客/论文/对话）并要求学习、记忆、内化

**功能**：从外部内容提炼知识，按三层架构持久化存储：

1. **技能层（Skill）**：可复用方法论、工作流程 → 优先创建新 skill
2. **纪律层（CLAUDE.md）**：可执行行为规则
3. **记忆层（Memory）**：用户偏好、项目背景、工具经验

**优先级**：Skill > CLAUDE.md > Memory

**使用方法**：用户提供内容并说 "/eat"、"学习这个"、"记住这个"

### wechat-reader

**触发条件**：用户提供微信公众号文章链接

**功能**：提取微信公众号文章全文

**实现**：
- 自动用 curl 带 UA 抓取
- 定位 `js_content` 区域提取正文
- 过滤 JS/CSS/UI 噪音
- 支持 URL / 本地文件 / stdin 三种输入

**使用方法**：`python3 ~/.claude/skills/wechat-reader/extract_wx_article.py <url>`

## 自动安装脚本

仓库根目录提供 `install.sh`，一键安装所有 skills：

```bash
./install.sh
```

## 更新

```bash
git pull origin main
```

## 给 AI Agent 的提示

- 每个 skill 的详细信息在对应子目录的 `SKILL.md` 中
- eat skill 的 `SKILL.md` 包含完整的三层分类判断逻辑
- wechat-reader 的 `SKILL.md` 包含提取脚本的使用说明
- 如果你需要理解某个 skill 的具体工作流程，直接读取对应的 `SKILL.md`
