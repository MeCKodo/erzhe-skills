# erzhe-skills

个人 Claude Code skills 集合

## 目录

### eat

从外部内容（文章、博客、论文、对话）中提炼知识，按三层架构持久化存储：

- **技能层（Skill）**：可复用的方法论、工作流程、操作步骤 — 优先抽象成 skill
- **纪律层（CLAUDE.md）**：可执行的行为规则，每次启动都应遵守
- **记忆层（Memory）**：用户偏好、项目背景、工具经验

**触发方式**：用户提供内容并说 "/eat"、"学习这个"、"记住这个"

### wechat-reader

提取微信公众号文章全文。当用户提供微信公众号文章链接时使用。

**特点**：自动用 curl 带 UA 抓取，过滤 JS/CSS/UI 噪音，支持 URL/本地文件/stdin 三种输入

## 安装

将此仓库克隆到本地，然后在 `~/.claude/settings.json` 中配置 skills 路径：

```json
{
  "skills": [
    "/Users/bytedance/workspaces/erzhe-skills/erzhe-eat",
    "/Users/bytedance/workspaces/erzhe-skills/erzhe-wechat-reader"
  ]
}
```

或者直接将 skill 复制到 `~/.claude/skills/` 目录。

## 更新

```bash
git pull origin main
```
