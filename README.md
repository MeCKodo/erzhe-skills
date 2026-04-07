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

将 skill 目录复制到 `~/.claude/skills/` 或通过 settings.json 配置 skill 搜索路径。

**settings.json 方式：**

```json
{
  "skills": ["<repo-path>/erzhe-eat", "<repo-path>/erzhe-wechat-reader"]
}
```

将 `<repo-path>` 替换为你克隆此仓库的实际路径。

## 更新

```bash
git pull origin main
```
