# 🤖 PPT Agent - 自然语言驱动的 PPT 自动化工具

> 本项目使用 AI 编程工具（Cursor + Claude / Codex）辅助开发，展示如何借助 AI 完成从 0 到 1 的 Agent 原型搭建。

## 解决的问题

手动修改 PPT 格式繁琐且容易出错：
- 字体不统一，反复调整浪费时间
- 数据从 Excel 贴到 PPT，容易贴错行、小数位不对
- 批量替换公司名称或数据，需要一页页手动改
- 多人协作时风格难以保持一致

**PPT Agent 让用户用自然语言描述需求，自动完成格式统一、文本替换和数据填充**，减少重复劳动，保证结果可复现。

## 核心能力（Agent 架构）

| 模块 | 作用 | 对应 JD 关键词 |
|------|------|---------------|
| **意图解析器** | 把"把所有标题改成红色 24 号字"翻译成结构化指令 | 任务规划 |
| **PPT 执行器** | 调用 `python-pptx` 完成具体修改 | 工具调用 |
| **上下文管理器** | 记录当前文件、操作历史、页码状态 | 上下文管理 |
| **主控流程** | 接收输入 → 解析 → 执行 → 反馈 | Agent Harness / 任务执行 |

## 安装与运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python main.py
```

首次运行会自动生成 `examples/sample.pptx` 和 `examples/data.xlsx`。

### 3. 输入指令示例
```
📝 请输入指令: 把所有标题改成红色 24 号字
📝 请输入指令: 把 旧公司名 替换为 新公司名
📝 请输入指令: 从 data.xlsx 读取数据填充到第 2 页
```

## 项目结构

```
ppt-agent/
├── main.py                  # 程序入口
├── agent/
│   ├── intent_parser.py     # 自然语言 → 结构化意图
│   ├── ppt_executor.py      # 意图 → python-pptx 工具调用
│   └── context_manager.py   # 状态与上下文管理
├── tools/
│   └── ppt_tools.py         # 示例文件生成工具
├── examples/
│   ├── sample.pptx          # 示例 PPT
│   └── data.xlsx            # 示例 Excel
└── requirements.txt         # 依赖清单
```

## 使用 AI 编程工具的开发过程

1. **需求描述**：向 Cursor Composer / Codex 描述"做一个自然语言改 PPT 的 Agent"
2. **架构设计**：AI 建议拆分为 Parser、Executor、Context 三个模块
3. **代码生成**：逐模块生成代码，我负责审阅逻辑和边界情况
4. **调试迭代**：针对"颜色解析失败"、"表格定位错误"等问题，用 AI 辅助修复
5. **验收验证**：用示例文件跑通完整流程，确认结果可复现

## 待优化方向

- [ ] 接入大模型（GPT-4 / Claude）做更精准的意图理解
- [ ] 增加"撤销/重做"和"操作回放"功能
- [ ] 支持更多 PPT 元素：图表、SmartArt、动画
- [ ] 建立自动化评测集，量化各指令的成功率

## 技术栈

- **python-pptx**: 操作 PowerPoint 文件（无需安装 Office）
- **openpyxl**: 读取 Excel 数据
- **正则表达式**: 中文自然语言规则解析
