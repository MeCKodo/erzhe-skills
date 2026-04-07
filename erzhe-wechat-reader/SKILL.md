---
name: wechat-reader
description: 提取微信公众号文章全文。当用户提供微信公众号文章链接时使用。
---

# 微信公众号文章读取

## 使用方法

遇到微信公众号文章链接时，使用本地脚本提取全文内容：

```bash
python3 ~/.claude/skills/wechat-reader/extract_wx_article.py <url>
```

## 为什么不用其他工具

| 工具 | 问题 |
|------|------|
| WebFetch | 公司网络策略拦截，返回验证码页 |
| curl 直接解析 | 需要正确处理 HTML 结构，过滤 JS/CSS 噪音 |
| CDP 浏览器 | 过重，且需要 proxy 连接 |
| Jina Reader | 对微信公众号经常超时 |

## 脚本特性

- 自动用 curl 带 UA 抓取
- 定位 `js_content` 区域提取正文
- 过滤 JS、CSS、UI 按钮等噪音
- 支持 URL / 本地文件 / stdin 三种输入方式

## 注意事项

- 如果返回验证码页面（检测到"环境异常"），脚本会报错提示
- 部分被微信限制访问的文章可能无法获取，此时需要通过搜索引擎查找镜像源
