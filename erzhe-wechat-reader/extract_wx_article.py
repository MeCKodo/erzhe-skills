#!/usr/bin/env python3
"""提取微信公众号文章正文。

用法:
  python3 extract_wx_article.py <url_or_file>

支持:
  - 直接传 URL（自动 curl）
  - 传本地 HTML 文件路径
  - 从 stdin 读取 HTML（管道模式）
"""
import sys
import os
import re
import html
import subprocess

# 过滤规则：这些行不是文章正文
SKIP_PATTERNS = [
    r'^[{}()\[\];,\.]+$',                          # 纯标点符号
    r'^--[_a-z]',                                  # CSS 变量
    r'^function\b',                                # JS 函数
    r'^(var|const|let)\s+\w+\s*=\s*',              # JS 变量声明
    r'^(return|if|else|for|while|try|catch)\b',    # JS 关键字
    r'^(document|window)\.',                       # DOM 操作
    r'addEventListener',                           # 事件绑定
    r'^\s*$',                                      # 空白行
    r'^(\{|\})\s*$',                               # 纯花括号
    r'^\s*[0-9]+\s*$',                             # 纯数字
    r'^window\.',                                  # window 对象
    r'^weui-',                                     # weui 样式
    r'^\s*#',                                      # CSS 选择器
    r'^\s*\.',                                     # CSS class
    r'^取消$|^允许$|^知道了$|^收藏$|^分享$|^留言$|^听过$',  # UI 按钮文字
    r'^微信|^小程序|^视频|^视频号|^轻触',            # 微信 UI 元素
    r'^滑动|^点击|^摇一摇|^扫码',                   # 操作提示
    r'^赞赏$|^赞赏作者',                           # 赞赏按钮
]

SKIP_RE = [re.compile(p) for p in SKIP_PATTERNS]


def fetch_html(url):
    """用 curl 抓取微信公众号文章 HTML。"""
    result = subprocess.run(
        [
            "curl", "-sL",
            "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout


def extract_text(html_content):
    """从微信公众号 HTML 中提取纯文本正文。"""
    # 定位 js_content 区域（文章正文容器）
    idx = html_content.find('id="js_content"')
    if idx == -1:
        idx = html_content.find('id="js_article"')
    if idx == -1:
        print("ERROR: 找不到文章正文区域 (js_content / js_article)", file=sys.stderr)
        if "环境异常" in html_content or "captcha" in html_content.lower():
            print("检测到微信验证码页面，文章可能已被限制访问或需要浏览器环境", file=sys.stderr)
        sys.exit(1)

    # 截取正文区域（js_content 后面的 div 内容）
    snippet = html_content[idx:idx + 500000]

    # 找到 js_content div 的闭合位置（找 </div> 后面跟 <script> 或 </body> 的地方）
    # 微信公众号文章结构: <div id="js_content"> ...正文... </div> <script> ... </script>
    # 我们只需要 <div> 和 </div> 之间的内容
    inner_start = snippet.find('>')
    if inner_start != -1:
        inner_html = snippet[inner_start + 1:]
    else:
        inner_html = snippet

    # 找到 </div> 后面紧跟的非 div 内容的位置
    # 微信文章里 js_content 包含多层嵌套 div，需要找到匹配的闭合标签
    depth = 0
    pos = 0
    end_pos = len(inner_html)
    while pos < len(inner_html):
        # 找下一个标签
        tag_match = re.search(r'<(/?)(\w+)(\s|>|/>)', inner_html[pos:])
        if not tag_match:
            break
        tag_name = tag_match.group(2).lower()
        is_close = tag_match.group(1) == '/'

        if tag_name == 'div':
            if is_close:
                depth -= 1
                if depth <= 0:
                    end_pos = pos + tag_match.start()
                    break
            else:
                depth += 1
        pos += tag_match.end()

    article_html = inner_html[:end_pos]

    # 递归提取所有文本节点
    text = _extract_text_from_html(article_html)
    text = html.unescape(text)

    # 按段落分割（多个换行或多个空格分隔的段落）
    # 微信文章用 <br> 和 </p> 分隔段落
    paragraphs = re.split(r'\n{2,}|\r\n\r\n+', text)

    # 清理和过滤
    meaningful = []
    for para in paragraphs:
        cleaned = para.strip()
        if not cleaned:
            continue

        # 过滤掉包含大量空白字符但实际内容很少的段落
        text_only = re.sub(r'\s+', '', cleaned)
        if len(text_only) < 2:
            continue

        # 应用过滤规则
        should_skip = False
        for pattern in SKIP_RE:
            if pattern.search(cleaned):
                should_skip = True
                break
        if should_skip:
            continue

        # 合并多个连续空格/换行为单个空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        meaningful.append(cleaned)

    return '\n\n'.join(meaningful)


def _extract_text_from_html(html_str):
    """递归提取 HTML 中的纯文本。"""
    # 移除 script 和 style 标签及其内容
    html_str = re.sub(r'<script[^>]*>.*?</script>', '', html_str, flags=re.DOTALL)
    html_str = re.sub(r'<style[^>]*>.*?</style>', '', html_str, flags=re.DOTALL)

    # 移除注释
    html_str = re.sub(r'<!--.*?-->', '', html_str, flags=re.DOTALL)

    # 将 <br>, </p>, </div>, </section>, </li> 替换为换行符
    html_str = re.sub(r'<br\s*/?>', '\n', html_str)
    html_str = re.sub(r'</(?:p|div|section|li|h[1-6]|blockquote)>', '\n', html_str, flags=re.IGNORECASE)

    # 移除所有剩余 HTML 标签
    html_str = re.sub(r'<[^>]+>', ' ', html_str)

    # 合并多个连续空格为单个
    html_str = re.sub(r'[ \t]+', ' ', html_str)

    return html_str.strip()


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith(('http://', 'https://')):
            html_content = fetch_html(arg)
        elif os.path.isfile(arg):
            with open(arg, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
        else:
            print(f"ERROR: 参数不是 URL 也不是文件: {arg}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        html_content = sys.stdin.read()
    else:
        print(__doc__)
        sys.exit(1)

    if not html_content:
        print("ERROR: 未获取到任何 HTML 内容", file=sys.stderr)
        sys.exit(1)

    text = extract_text(html_content)
    print(text)


if __name__ == '__main__':
    main()
