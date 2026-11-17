"""
意图解析器 - 把用户的自然语言翻译成 Agent 能理解的结构化指令
"""
import re


class IntentParser:
    """解析用户的中文自然语言指令"""

    def parse(self, text: str) -> dict:
        """
        主解析入口
        返回结构化的意图字典，包含 type（操作类型）和参数
        """
        text = text.strip()
        lower = text.lower()

        # 优先级 1: 改样式（字体、颜色、字号）
        if any(k in lower for k in ["标题", "字体", "颜色", "字号", "大小", "改成", "设置为"]):
            if any(k in lower for k in ["红", "蓝", "黑", "绿", "黄", "号", "pt", "大小"]):
                return self._parse_style(text)

        # 优先级 2: 替换文字
        if any(k in lower for k in ["替换", "改成", "改为", "把", "将"]):
            return self._parse_replace(text)

        # 优先级 3: 数据填充
        if any(k in lower for k in ["excel", "xlsx", "数据", "填充", "读取", "导入"]):
            return self._parse_data_fill(text)

        # 无法识别
        return {"type": "unknown", "raw": text, "msg": "暂不支持该指令，请尝试：改标题样式、替换文字、填充数据"}

    def _parse_style(self, text: str) -> dict:
        """解析改样式指令，例如：把所有标题改成红色 24 号字"""
        # 解析颜色
        color_map = {
            "红": "FF0000", "红色": "FF0000",
            "蓝": "0000FF", "蓝色": "0000FF",
            "黑": "000000", "黑色": "000000",
            "绿": "00AA00", "绿色": "00AA00",
            "黄": "FFCC00", "黄色": "FFCC00",
        }
        color = None
        for name, code in color_map.items():
            if name in text:
                color = code
                break

        # 解析字号（支持 "24号"、"24 号"、"24pt"）
        size = None
        match = re.search(r'(\d+)\s*[号号pt]', text)
        if match:
            size = int(match.group(1))

        # 解析目标范围
        target = "all"  # 默认全部页面
        page_match = re.search(r'第\s*(\d+)\s*页', text)
        if page_match:
            target = int(page_match.group(1))

        # 解析目标元素
        element = "title"  # 默认标题
        if "正文" in text or "内容" in text:
            element = "body"
        if "全部" in text or "所有文字" in text:
            element = "all_text"

        return {
            "type": "set_style",
            "target": target,      # "all" 或具体页码
            "element": element,    # "title" / "body" / "all_text"
            "color": color,        # 十六进制颜色码
            "size": size,          # 字号（Pt）
        }

    def _parse_replace(self, text: str) -> dict:
        """解析替换指令，例如：把 旧公司名 替换为 新公司名"""
        # 匹配多种中文表达
        patterns = [
            r'[把将]\s*(.+?)\s*替换[为成]\s*(.+)',
            r'[把将]\s*(.+?)\s*改[为成]\s*(.+)',
            r'[把将]\s*(.+?)\s*换[为成]\s*(.+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return {
                    "type": "replace_text",
                    "old_text": m.group(1).strip(),
                    "new_text": m.group(2).strip(),
                }

        # 兜底：如果包含"A换成B"的简单结构
        simple = text.split("换成")
        if len(simple) == 2:
            return {"type": "replace_text", "old_text": simple[0].strip(), "new_text": simple[1].strip()}

        return {"type": "replace_text", "old_text": "", "new_text": "", "msg": "未能解析替换内容"}

    def _parse_data_fill(self, text: str) -> dict:
        """解析数据填充指令，例如：从 data.xlsx 读取数据填充到第 2 页"""
        page = 1
        page_match = re.search(r'第\s*(\d+)\s*页', text)
        if page_match:
            page = int(page_match.group(1))

        # 尝试提取文件名
        file_match = re.search(r'[从用]\s*(\S+?\.xlsx?)', text)
        source = file_match.group(1) if file_match else "examples/data.xlsx"

        return {
            "type": "fill_data",
            "source": source,
            "page": page,
        }
