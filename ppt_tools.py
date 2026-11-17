"""
底层工具 - 生成示例文件，方便零基础用户直接体验
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import openpyxl
import os


def create_sample_files():
    """自动生成示例 PPT 和 Excel，用户无需准备文件即可运行"""
    os.makedirs("examples", exist_ok=True)

    # 1. 创建示例 PPT
    prs = Presentation()

    # 第 1 页：标题页
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])  # 标题页布局
    slide1.shapes.title.text = "旧公司名 - 季度汇报"
    slide1.placeholders[1].text = "2026 Q3 财务与业务总结"

    # 第 2 页：带表格的数据页
    slide2 = prs.slides.add_slide(prs.slide_layouts[5])  # 空白布局
    slide2.shapes.title.text = "销售数据概览"

    # 插入表格
    rows, cols = 4, 3
    left = Inches(1)
    top = Inches(2)
    width = Inches(6)
    height = Inches(2)
    table = slide2.shapes.add_table(rows, cols, left, top, width, height).table

    # 表头
    table.cell(0, 0).text = "产品"
    table.cell(0, 1).text = "Q2 销售额（万元）"
    table.cell(0, 2).text = "Q3 销售额（万元）"
    # 数据行（占位）
    table.cell(1, 0).text = "产品 A"
    table.cell(1, 1).text = "待填充"
    table.cell(1, 2).text = "待填充"
    table.cell(2, 0).text = "产品 B"
    table.cell(2, 1).text = "待填充"
    table.cell(2, 2).text = "待填充"
    table.cell(3, 0).text = "产品 C"
    table.cell(3, 1).text = "待填充"
    table.cell(3, 2).text = "待填充"

    # 第 3 页：正文页
    slide3 = prs.slides.add_slide(prs.slide_layouts[1])
    slide3.shapes.title.text = "下季度规划"
    slide3.placeholders[1].text = "旧公司名将继续推进数字化转型..."

    prs.save("examples/sample.pptx")

    # 2. 创建示例 Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "销售数据"
    ws.append(["产品", "Q2 销售额（万元）", "Q3 销售额（万元）"])
    ws.append(["产品 A", 120, 150])
    ws.append(["产品 B", 85, 92])
    ws.append(["产品 C", 200, 180])
    wb.save("examples/data.xlsx")

    print("✅ 示例文件生成完毕")
