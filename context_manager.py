"""
上下文管理器 - Agent 的"记忆系统"
记录：当前在处理哪个 PPT、已经做了什么、做到哪一步了
"""


class ContextManager:
    """管理 Agent 的执行上下文（状态与记忆）"""

    def __init__(self):
        self.ppt_path = None          # 当前打开的 PPT 文件路径
        self.history = []             # 操作历史记录
        self.current_slide = 0        # 当前聚焦的页码
        self.total_slides = 0         # PPT 总页数

    def set_ppt(self, path: str):
        """设置当前 PPT 文件"""
        self.ppt_path = path
        self.history.append(f"📂 加载 PPT: {path}")
        print(f"📂 已加载: {path}")

    def log_action(self, intent: dict):
        """记录一次操作"""
        self.history.append(intent)

    def get_summary(self) -> str:
        """获取操作摘要"""
        return f"已执行 {len(self.history)} 步操作"

    def last_action(self) -> dict:
        """获取上一步操作（用于回滚或重试）"""
        if self.history:
            return self.history[-1]
        return {}
