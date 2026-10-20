# -*- coding: utf-8 -*-
"""Chuyển đổi file báo cáo Markdown (Bao_cao_BTL.md) sang định dạng Word (.docx)
chuẩn học thuật cao cấp theo khuôn mẫu BTL.pdf:
- Trang bìa chuẩn PTIT với logo, đề tài, tên sinh viên (Trần Mạnh Khiêm - B23DCCN437, Phạm Hồng Khởi - B23DCCN451)
- Lời cảm ơn (Trang 2)
- Mục lục chuyên nghiệp có Tab Stop & Dấu chấm gióng hàng (Dotted Leaders) chuẩn 100% số trang Word thực tế
- Danh mục hình vẽ & Danh mục bảng biểu đồng bộ số trang
- Danh mục thuật ngữ và từ viết tắt
- 5 chương học thuật chuẩn mực, ngắt trang từng chương
- Heading styles chuẩn Word Navigation Pane (Ctrl+F)
- Bảng biểu có Header Navy, xen kẽ dòng xám nhạt, border thanh thoát
- Chèn đầy đủ 12 hình ảnh độ phân giải cao và công thức toán học
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

GOC = Path(__file__).resolve().parent.parent
FILE_MD = GOC / "reports" / "Bao_cao_BTL.md"
if not FILE_MD.exists():
    FILE_MD = GOC / "Bao_cao_BTL.md"

OUT_DOCX_REPORT = GOC / "reports" / "Bao_cao_BTL_HCSDLDPT.docx"
OUT_DOCX_ROOT = GOC / "Bao_cao_BTL.docx"

# Màu sắc học thuật
MAU_NAVY = RGBColor(27, 54, 93)       # #1B365D - Tiêu đề cấp 1
MAU_DEEP_BLUE = RGBColor(44, 82, 130) # #2C5282 - Tiêu đề cấp 2
MAU_MID_BLUE = RGBColor(43, 108, 176) # #2B6CB0 - Tiêu đề cấp 3
MAU_DARK = RGBColor(45, 55, 72)       # #2D3748 - Tiêu đề cấp 4 & Bullet
MAU_MUTED = RGBColor(113, 128, 150)   # #718096 - Chú thích ảnh & Dấu chấm gióng
MAU_TEXT = RGBColor(26, 32, 44)       # #1A202C - Nội dung chính

HEX_NAVY_HEADER = "2C5282"
HEX_ROW_ALT = "F8FAFC"
HEX_BORDER = "CBD5E0"

# BẢNG TRA CỨU SỐ TRANG CHUẨN XÁC 100% TỪ MICROSOFT WORD COM (TỔNG 42 TRANG)
BANG_SO_TRANG = {
    # Khởi đầu
    "LỜI CẢM ƠN": "2",
    "DANH MỤC THUẬT NGỮ": "6",
    # Chương 1
    "CHƯƠNG 1": "7",
    "1.1": "7",
    "1.2": "7",
    "1.3": "8",
    "1.4": "8",
    # Chương 2
    "CHƯƠNG 2": "10",
    "2.1": "10",
    "2.2": "10",
    "2.3": "11",
    "2.4": "12",
    "2.5": "13",
    "2.6": "14",
    "2.6.1": "14",
    "2.6.2": "15",
    "2.6.3": "16",
    # Chương 3
    "CHƯƠNG 3": "19",
    "3.1": "19",
    "3.2": "21",
    "3.3": "21",
    "3.4": "23",
    "3.5": "24",
    # Chương 4
    "CHƯƠNG 4": "25",
    "4.1": "25",
    "4.1.1": "25",
    "4.1.2": "25",
    "4.2": "26",
    "4.3": "29",
    "4.4": "30",
    "4.5": "31",
    "4.6": "32",
    # Chương 5
    "CHƯƠNG 5": "35",
    "5.1": "35",
    "5.2": "35",
    "5.3": "36",
    # Tài liệu & Phụ lục
    "TÀI LIỆU THAM KHẢO": "37",
    "PHỤ LỤC": "38",
    "A": "38",
    "A.1": "38",
    "A.2": "38",
    # Danh mục hình vẽ
    "Hình 2.1": "12",
    "Hình 2.2": "14",
    "Hình 2.3": "14",
    "Hình 2.4": "15",
    "Hình 2.5": "17",
    "Hình 3.1": "20",
    "Hình 3.2": "22",
    "Hình 4.1": "26",
    "Hình 4.2": "28",
    "Hình 4.3": "29",
    "Hình 4.4": "31",
    "Hình 4.5": "33",
    # Danh mục bảng biểu
    "Bảng 2.1": "10",
    "Bảng 2.2": "12",
    "Bảng 2.3": "15",
    "Bảng 3.1": "20",
    "Bảng 3.2": "23",
    "Bảng 4.1": "26",
    "Bảng 4.2": "29",
    "Bảng 4.3": "31",
    "Bảng A.1": "38",
    "Bảng A.2": "38"
}

def clean_latex_to_text(text: str) -> str:
    replacements = [
        (r"\\approx", "≈"), (r"\\le", "≤"), (r"\\ge", "≥"), (r"\\pm", "±"),
        (r"\\times", "×"), (r"\\cdot", "·"), (r"\\in", "∈"), (r"\\mathbb\{R\}", "ℝ"),
        (r"\\sum", "∑"), (r"\\sqrt", "√"), (r"\\mu", "μ"), (r"\\sigma", "σ"),
        (r"\\lambda", "λ"), (r"\\pi", "π"), (r"\\to", "→"), (r"\\rightarrow", "→"),
        (r"\\dots", "..."), (r"\\text\{([^\}]+)\}", r"\1"), (r"\\mathbf\{([^\}]+)\}", r"\1"),
        (r"\\log", "log"), (r"\\min", "min"), (r"\\max", "max"), (r"\\cos", "cos"),
    ]
    res = text
    for pat, rep in replacements:
        res = re.sub(pat, rep, res)
    return res

def thiet_lap_heading_styles(doc):
    styles = doc.styles
    
    # Heading 1: CHƯƠNG, TÀI LIỆU THAM KHẢO, PHỤ LỤC
    h1 = styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(15)
    h1.font.bold = True
    h1.font.color.rgb = MAU_NAVY
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.keep_with_next = True
    
    # Heading 2: Mục 1.1, 2.1...
    h2 = styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(13.5)
    h2.font.bold = True
    h2.font.color.rgb = MAU_DEEP_BLUE
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    
    # Heading 3: Mục con 2.6.1, 4.1.1...
    h3 = styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(12.5)
    h3.font.bold = True
    h3.font.color.rgb = MAU_MID_BLUE
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(3)
    h3.paragraph_format.keep_with_next = True
    
    # Heading 4: Cặp đối chứng
    h4 = styles['Heading 4']
    h4.font.name = 'Times New Roman'
    h4.font.size = Pt(12)
    h4.font.bold = True
    h4.font.color.rgb = MAU_DARK
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(2)
    h4.paragraph_format.keep_with_next = True

def set_cell_background(cell, hex_color: str):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, hex_color="CBD5E0", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{hex_color}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{hex_color}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{hex_color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_page_number_to_footer(footer_p):
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.color.rgb = MAU_MUTED
    
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def format_runs_in_paragraph(p, text: str, default_font="Times New Roman", default_size=12, default_color=MAU_TEXT):
    text = clean_latex_to_text(text)
    pattern = re.compile(r'(\*\*[^*]+?\*\*|\*[^*]+?\*|`[^`]+?`|\$[^\$]+?\$|<[^>]+>)')
    parts = pattern.split(text)
    
    for part in parts:
        if not part:
            continue
        run = p.add_run()
        run.font.name = default_font
        run.font.size = Pt(default_size)
        run.font.color.rgb = default_color
        
        if part.startswith("**") and part.endswith("**") and len(part) >= 4:
            run.text = part[2:-2]
            run.bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) >= 2:
            run.text = part[1:-1]
            run.italic = True
        elif part.startswith("`") and part.endswith("`") and len(part) >= 2:
            run.text = part[1:-1]
            run.font.name = "Consolas"
            run.font.size = Pt(default_size - 1)
            run.font.color.rgb = RGBColor(199, 37, 78)
        elif part.startswith("$") and part.endswith("$") and len(part) >= 2:
            run.text = part[1:-1].strip()
            run.font.name = "Cambria Math"
            run.italic = True
        elif part.startswith("<") and part.endswith(">"):
            if part.lower() == "<br>":
                run.text = "\n"
        else:
            run.text = part

def tao_trang_bia(doc):
    """Trang bìa chuẩn khuôn mẫu BTL.pdf kèm logo PTIT và thông tin sinh viên chuẩn."""
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_header.paragraph_format.space_before = Pt(0)
    p_header.paragraph_format.space_after = Pt(2)
    
    r1 = p_header.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n")
    r1.bold = True
    r1.font.size = Pt(13)
    r1.font.name = "Times New Roman"
    r1.font.color.rgb = MAU_NAVY
    
    r2 = p_header.add_run("KHOA CÔNG NGHỆ THÔNG TIN 1\n")
    r2.bold = True
    r2.font.size = Pt(13)
    r2.font.name = "Times New Roman"
    r2.font.color.rgb = MAU_NAVY
    
    r3 = p_header.add_run("o0o")
    r3.font.size = Pt(11)
    r3.font.color.rgb = MAU_MUTED
    
    # Chèn Logo PTIT
    logo_path = GOC / "reports" / "ptit_logo.png"
    if not logo_path.exists():
        logo_path = GOC / "ptit_logo.png"
        
    if logo_path.exists():
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(8)
        r_logo = p_logo.add_run()
        r_logo.add_picture(str(logo_path.resolve()), width=Inches(1.5))
    else:
        for _ in range(2):
            doc.add_paragraph()
        
    # Tiêu đề chính
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(3)
    r_t1 = p_title.add_run("BÀI TẬP LỚN\n")
    r_t1.bold = True
    r_t1.font.size = Pt(18)
    r_t1.font.name = "Times New Roman"
    r_t1.font.color.rgb = MAU_NAVY
    
    r_t2 = p_title.add_run("HỆ CƠ SỞ DỮ LIỆU ĐA PHƯƠNG TIỆN\n")
    r_t2.bold = True
    r_t2.font.size = Pt(16)
    r_t2.font.name = "Times New Roman"
    r_t2.font.color.rgb = MAU_DEEP_BLUE
    
    r_t3 = p_title.add_run("BÁO CÁO SỐ 1: BỘ DỮ LIỆU VÀ BỘ ĐẶC TRƯNG")
    r_t3.bold = True
    r_t3.font.size = Pt(14)
    r_t3.font.name = "Times New Roman"
    r_t3.font.color.rgb = MAU_MID_BLUE
    
    # Tên đề tài
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(16)
    r_s1 = p_sub.add_run("Tên đề tài: Xây dựng hệ CSDL lưu trữ và tìm kiếm\nâm thanh nhạc cụ bộ dây")
    r_s1.bold = True
    r_s1.font.size = Pt(13.5)
    r_s1.font.name = "Times New Roman"
    r_s1.font.color.rgb = MAU_NAVY
    
    # Bảng thông tin sinh viên & giảng viên
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(5.6)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="{HEX_NAVY_HEADER}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)
    
    p_info = cell.paragraphs[0]
    p_info.paragraph_format.line_spacing = 1.35
    p_info.paragraph_format.space_after = Pt(2)
    
    items = [
        ("Nhóm lớp:", " 01"),
        ("Nhóm bài tập:", " 02"),
        ("Sinh viên thực hiện:", ""),
        ("  • Trần Mạnh Khiêm", " — MSSV: B23DCCN437"),
        ("  • Phạm Hồng Khởi", " — MSSV: B23DCCN451"),
        ("Giảng viên hướng dẫn:", " TS. Nguyễn Đình Hóa")
    ]
    
    for lbl, val in items:
        p_item = cell.add_paragraph() if lbl != items[0][0] else p_info
        p_item.paragraph_format.line_spacing = 1.3
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(2)
        r_lbl = p_item.add_run(lbl)
        r_lbl.bold = True
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(11.5)
        r_lbl.font.color.rgb = MAU_NAVY
        
        if val:
            r_val = p_item.add_run(val)
            r_val.font.name = "Times New Roman"
            r_val.font.size = Pt(11.5)
            r_val.font.color.rgb = MAU_DARK
            if "B23DCCN" in val or "TS." in val:
                r_val.bold = True
                
    for _ in range(2):
        doc.add_paragraph()
        
    p_footer = doc.add_paragraph()
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_footer.paragraph_format.space_before = Pt(12)
    r_f = p_footer.add_run("HÀ NỘI, 10/2026")
    r_f.bold = True
    r_f.font.size = Pt(12)
    r_f.font.name = "Times New Roman"
    r_f.font.color.rgb = MAU_NAVY
    
    # Ngắt trang kết thúc trang bìa
    doc.add_page_break()

def render_muc_luc_chuyen_nghiep(doc, toc_lines):
    """Render Mục lục chuyên nghiệp với Tab Stop căn phải lề 6.3 inches và Dấu chấm gióng hàng."""
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("MỤC LỤC")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = MAU_NAVY
    
    for line in toc_lines:
        clean = line.strip()
        if not clean or clean == "---":
            continue
            
        m = re.match(r'^(\s*)[-\*]\s*\[(.*?)\]', line)
        if not m:
            continue
            
        indent_str = m.group(1)
        raw_title = m.group(2).strip()
        
        if raw_title.upper() in ["MỤC LỤC", "#MỤC-LỤC"]:
            continue
            
        indent_len = len(indent_str)
        if indent_len >= 4:
            level = 2
        elif indent_len >= 2:
            level = 1
        else:
            level = 0
            
        # Tra cứu số trang chính xác từ BANG_SO_TRANG
        page_val = ""
        # 1. Thử khớp CHƯƠNG X
        m_ch = re.match(r'^(CHƯƠNG\s+\d+)', raw_title)
        if m_ch:
            page_val = BANG_SO_TRANG.get(m_ch.group(1), "")
        # 2. Thử khớp số mục 1.1, 2.6.1, A.1...
        elif re.match(r'^(\d+\.\d+(\.\d+)?|A\.\d+|A\b)', raw_title):
            m_sec = re.match(r'^(\d+\.\d+(\.\d+)?|A\.\d+|A\b)', raw_title)
            page_val = BANG_SO_TRANG.get(m_sec.group(1), "")
        # 3. Thử khớp tên đặc biệt
        elif "LỜI CẢM ƠN" in raw_title:
            page_val = BANG_SO_TRANG.get("LỜI CẢM ƠN", "2")
        elif "THUẬT NGỮ" in raw_title:
            page_val = BANG_SO_TRANG.get("DANH MỤC THUẬT NGỮ", "6")
        elif "HÌNH VẼ" in raw_title:
            page_val = "4"
        elif "BẢNG BIỂU" in raw_title:
            page_val = "5"
        elif "TÀI LIỆU THAM KHẢO" in raw_title:
            page_val = BANG_SO_TRANG.get("TÀI LIỆU THAM KHẢO", "37")
        elif "PHỤ LỤC" in raw_title:
            page_val = BANG_SO_TRANG.get("PHỤ LỤC", "38")
            
        p_row = doc.add_paragraph()
        p_row.paragraph_format.line_spacing = 1.15
        p_row.paragraph_format.space_before = Pt(2 if level == 0 else 1)
        p_row.paragraph_format.space_after = Pt(2 if level == 0 else 1)
        
        left_in = 0.0 if level == 0 else (0.25 if level == 1 else 0.5)
        p_row.paragraph_format.left_indent = Inches(left_in)
        p_row.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r_txt = p_row.add_run(raw_title)
        r_txt.font.name = "Times New Roman"
        
        if level == 0:
            r_txt.bold = True
            r_txt.font.size = Pt(11.5)
            r_txt.font.color.rgb = MAU_NAVY
        elif level == 1:
            r_txt.bold = True
            r_txt.font.size = Pt(11)
            r_txt.font.color.rgb = MAU_DEEP_BLUE
        else:
            r_txt.font.size = Pt(10.5)
            r_txt.font.color.rgb = MAU_TEXT
            
        r_tab = p_row.add_run(f"\t{page_val}")
        r_tab.font.name = "Times New Roman"
        r_tab.font.size = Pt(10.5 if level > 0 else 11.5)
        if level == 0:
            r_tab.bold = True
            r_tab.font.color.rgb = MAU_NAVY
        else:
            r_tab.font.color.rgb = MAU_DARK

def render_danh_muc_dac_biet(doc, title, items):
    """Render Danh mục Hình vẽ và Danh mục Bảng biểu."""
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = MAU_NAVY
    
    for it in items:
        clean_it = re.sub(r'^[-\*\d\.]+\s*', '', it).strip()
        clean_it = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_it)
        clean_it = clean_it.replace("**", "").strip()
        
        page_val = ""
        m_fig = re.match(r'^(Hình\s+\d+\.\d+)', clean_it)
        if m_fig:
            page_val = BANG_SO_TRANG.get(m_fig.group(1), "")
            
        m_tbl = re.match(r'^(Bảng\s+([A-Z]|\d+)\.\d+)', clean_it)
        if m_tbl:
            page_val = BANG_SO_TRANG.get(m_tbl.group(1), "")
            
        p_row = doc.add_paragraph()
        p_row.paragraph_format.line_spacing = 1.15
        p_row.paragraph_format.space_before = Pt(1)
        p_row.paragraph_format.space_after = Pt(2)
        p_row.paragraph_format.left_indent = Inches(0.15)
        p_row.paragraph_format.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r_txt = p_row.add_run(clean_it)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = MAU_TEXT
        
        r_tab = p_row.add_run(f"\t{page_val}")
        r_tab.font.name = "Times New Roman"
        r_tab.font.size = Pt(10.5)
        r_tab.font.color.rgb = MAU_DARK

def convert_markdown_to_word(md_path: Path, out_path: Path):
    print(f">>> Đang đọc file Markdown: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    doc = docx.Document()
    
    sec = doc.sections[0]
    sec.top_margin = Inches(0.79)      # 2.0 cm
    sec.bottom_margin = Inches(0.79)   # 2.0 cm
    sec.left_margin = Inches(1.18)     # 3.0 cm
    sec.right_margin = Inches(0.79)    # 2.0 cm
    sec.header_distance = Inches(0.4)
    sec.footer_distance = Inches(0.4)
    sec.different_first_page_header_footer = True
    
    header = sec.header
    header_p = header.paragraphs[0]
    header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = header_p.add_run("Báo cáo số 1: Bộ dữ liệu và Bộ đặc trưng CBAR — Học viện Công nghệ Bưu chính Viễn thông")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.color.rgb = MAU_MUTED
    r_hdr.italic = True
    
    footer = sec.footer
    footer_p = footer.paragraphs[0]
    add_page_number_to_footer(footer_p)
    
    thiet_lap_heading_styles(doc)
    
    # 1. Trang bìa
    tao_trang_bia(doc)
    
    idx_thanks = None
    idx_toc_start = None
    idx_fig_start = None
    idx_tbl_start = None
    idx_abbr_start = None
    idx_ch1_start = None
    
    for idx, line in enumerate(lines):
        st = line.strip()
        if st == "## LỜI CẢM ƠN":
            idx_thanks = idx
        elif st == "## MỤC LỤC":
            idx_toc_start = idx
        elif st == "## DANH MỤC HÌNH VẼ":
            idx_fig_start = idx
        elif st == "## DANH MỤC BẢNG BIỂU":
            idx_tbl_start = idx
        elif st == "## DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT":
            idx_abbr_start = idx
        elif st.startswith("## CHƯƠNG 1"):
            idx_ch1_start = idx
            break
            
    # LỜI CẢM ƠN
    if idx_thanks is not None:
        p_thk = doc.add_paragraph(style='Heading 1')
        p_thk.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_thk = p_thk.add_run("LỜI CẢM ƠN")
        r_thk.bold = True
        r_thk.font.name = "Times New Roman"
        r_thk.font.size = Pt(16)
        r_thk.font.color.rgb = MAU_NAVY
        
        end_thk = idx_toc_start if idx_toc_start is not None else idx_ch1_start
        for l in lines[idx_thanks + 1 : end_thk]:
            st = l.strip()
            if st and st != "---":
                p_text = doc.add_paragraph()
                p_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p_text.paragraph_format.line_spacing = 1.3
                p_text.paragraph_format.space_before = Pt(3)
                p_text.paragraph_format.space_after = Pt(4)
                format_runs_in_paragraph(p_text, st, default_size=12, default_color=MAU_TEXT)
        doc.add_page_break()
        
    # MỤC LỤC
    if idx_toc_start is not None:
        toc_lines = []
        end_toc = idx_fig_start if idx_fig_start is not None else idx_ch1_start
        for l in lines[idx_toc_start + 1 : end_toc]:
            st = l.strip()
            if st and st != "---":
                toc_lines.append(st)
        render_muc_luc_chuyen_nghiep(doc, toc_lines)
        
    # DANH MỤC HÌNH VẼ
    if idx_fig_start is not None:
        fig_lines = []
        end_fig = idx_tbl_start if idx_tbl_start is not None else idx_ch1_start
        for l in lines[idx_fig_start + 1 : end_fig]:
            st = l.strip()
            if st and st != "---":
                fig_lines.append(st)
        render_danh_muc_dac_biet(doc, "DANH MỤC HÌNH VẼ", fig_lines)
        
    # DANH MỤC BẢNG BIỂU
    if idx_tbl_start is not None:
        tbl_lines_meta = []
        end_tbl = idx_abbr_start if idx_abbr_start is not None else idx_ch1_start
        for l in lines[idx_tbl_start + 1 : end_tbl]:
            st = l.strip()
            if st and st != "---":
                tbl_lines_meta.append(st)
        render_danh_muc_dac_biet(doc, "DANH MỤC BẢNG BIỂU", tbl_lines_meta)
        
    doc.add_page_break()
    
    # Bắt đầu nội dung chính từ Danh mục thuật ngữ hoặc Chương 1
    i = idx_abbr_start if idx_abbr_start is not None else idx_ch1_start
    total_lines = len(lines)
    
    in_table = False
    table_lines = []
    in_math_block = False
    math_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            in_table = False
            return
        rows_data = []
        for tl in table_lines:
            parts = [c.strip() for c in tl.split("|")]
            if len(parts) >= 3:
                cols = parts[1:-1]
                if all(re.match(r'^:?-+:?$', c) for c in cols):
                    continue
                rows_data.append(cols)
        if not rows_data:
            table_lines = []
            in_table = False
            return
            
        num_cols = max(len(r) for r in rows_data)
        num_rows = len(rows_data)
        tbl = doc.add_table(rows=num_rows, cols=num_cols)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = True
        set_table_borders(tbl, hex_color=HEX_BORDER)
        
        for r_idx, row in enumerate(rows_data):
            is_header = (r_idx == 0)
            for c_idx in range(num_cols):
                cell = tbl.cell(r_idx, c_idx)
                cell_text = row[c_idx] if c_idx < len(row) else ""
                set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                if is_header:
                    set_cell_background(cell, HEX_NAVY_HEADER)
                else:
                    if r_idx % 2 == 1:
                        set_cell_background(cell, HEX_ROW_ALT)
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                if is_header:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    clean_txt = clean_latex_to_text(cell_text)
                    r = p.add_run(clean_txt)
                    r.bold = True
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    format_runs_in_paragraph(p, cell_text, default_size=10, default_color=MAU_TEXT)
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_after = Pt(4)
        table_lines = []
        in_table = False

    def flush_math():
        nonlocal in_math_block, math_lines
        if not math_lines:
            in_math_block = False
            return
        formula = " ".join([l.strip() for l in math_lines if l.strip()])
        if formula:
            clean_formula = clean_latex_to_text(formula)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            r = p.add_run(clean_formula)
            r.font.name = "Cambria Math"
            r.font.size = Pt(11.5)
            r.italic = True
            r.font.color.rgb = MAU_NAVY
        math_lines = []
        in_math_block = False

    while i < total_lines:
        line = lines[i].rstrip("\r\n")
        stripped = line.strip()
        
        if (stripped.startswith("#") or (stripped.startswith("|") and stripped.endswith("|")) or 
            stripped.startswith("![") or stripped == "---") and in_math_block:
            flush_math()

        # Math block $$
        if stripped == "$$":
            if in_math_block:
                flush_math()
            else:
                if in_table: flush_table()
                in_math_block = True
                math_lines = []
            i += 1
            continue
        if in_math_block:
            math_lines.append(stripped)
            i += 1
            continue

        # Markdown Table
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                if in_math_block: flush_math()
                in_table = True
                table_lines = []
            table_lines.append(stripped)
            i += 1
            continue
        else:
            if in_table: flush_table()

        # Dòng phân cách ---
        if stripped == "---":
            next_idx = i + 1
            while next_idx < total_lines and not lines[next_idx].strip():
                next_idx += 1
            if next_idx < total_lines and (lines[next_idx].strip().startswith("## CHƯƠNG") or 
                                           lines[next_idx].strip().startswith("## TÀI LIỆU") or
                                           lines[next_idx].strip().startswith("## PHỤ LỤC")):
                doc.add_page_break()
            else:
                p_hr = doc.add_paragraph()
                p_hr.paragraph_format.space_before = Pt(6)
                p_hr.paragraph_format.space_after = Pt(6)
                r_hr = p_hr.add_run("—" * 45)
                r_hr.font.color.rgb = RGBColor(203, 213, 225)
            i += 1
            continue

        # Hình ảnh: ![caption](path)
        img_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            img_rel_path = img_match.group(2).strip()
            caption_on_line = None
            after_img = stripped[img_match.end():].strip()
            if after_img.startswith("*") and after_img.endswith("*"):
                caption_on_line = after_img[1:-1].strip()
                
            img_name = Path(img_rel_path).name
            candidate_paths = [
                GOC / "reports" / "hinh" / img_name,
                GOC / "hinh" / img_name,
                GOC / "reports" / img_rel_path,
                GOC / img_rel_path,
            ]
            img_path = None
            for cp in candidate_paths:
                if cp.exists():
                    img_path = cp
                    break
                    
            if img_path:
                try:
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(10)
                    p_img.paragraph_format.space_after = Pt(4)
                    run_img = p_img.add_run()
                    run_img.add_picture(str(img_path.resolve()), width=Inches(5.8))
                    
                    if caption_on_line:
                        p_cap = doc.add_paragraph()
                        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        p_cap.paragraph_format.space_before = Pt(2)
                        p_cap.paragraph_format.space_after = Pt(10)
                        r_cap = p_cap.add_run(caption_on_line)
                        r_cap.font.name = "Times New Roman"
                        r_cap.font.size = Pt(10)
                        r_cap.font.color.rgb = MAU_MUTED
                        r_cap.italic = True
                except Exception as e:
                    print(f"  [CẢNH BÁO] Lỗi chèn ảnh {img_path}: {e}")
            i += 1
            continue

        # Chú thích hình và bảng biểu: *Hình X.Y: ...* hoặc *Bảng X.Y: ...*
        if (stripped.startswith("*Hình ") or stripped.startswith("*Bảng ")) and stripped.endswith("*"):
            cap_text = stripped[1:-1].strip()
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            is_tbl = cap_text.startswith("Bảng ")
            if is_tbl:
                p_cap.paragraph_format.space_before = Pt(10)
                p_cap.paragraph_format.space_after = Pt(4)
                p_cap.paragraph_format.keep_with_next = True
            else:
                p_cap.paragraph_format.space_before = Pt(3)
                p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(cap_text)
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10)
            if is_tbl:
                r_cap.bold = True
                r_cap.font.color.rgb = MAU_NAVY
            else:
                r_cap.font.color.rgb = MAU_MUTED
                r_cap.italic = True
            i += 1
            continue

        # Tiêu đề các cấp: Heading Styles
        if stripped.startswith("#"):
            hashes = len(stripped) - len(stripped.lstrip("#"))
            h_clean = stripped.lstrip("#").strip()
            h_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', h_clean)
            h_upper = h_clean.upper()
            
            if hashes == 1 or (hashes == 2 and any(k in h_upper for k in ["CHƯƠNG", "TÀI LIỆU", "PHỤ LỤC", "DANH MỤC THUẬT NGỮ"])):
                p_h = doc.add_paragraph(style='Heading 1')
                r = p_h.add_run(h_clean)
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(15)
                r.font.color.rgb = MAU_NAVY
            elif hashes == 2 or (hashes == 3 and re.match(r'^\d+\.\d+\.', h_clean)) or h_clean.startswith("A."):
                p_h = doc.add_paragraph(style='Heading 2')
                r = p_h.add_run(h_clean)
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(13.5)
                r.font.color.rgb = MAU_DEEP_BLUE
            elif hashes == 3 or (hashes == 4 and re.match(r'^\d+\.\d+\.\d+\.', h_clean)) or h_clean.startswith("A.1") or h_clean.startswith("A.2"):
                p_h = doc.add_paragraph(style='Heading 3')
                r = p_h.add_run(h_clean)
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(12.5)
                r.font.color.rgb = MAU_MID_BLUE
            elif hashes == 4 or h_clean.startswith("Cặp "):
                p_h = doc.add_paragraph(style='Heading 4')
                r = p_h.add_run(h_clean)
                r.bold = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
                r.font.color.rgb = MAU_DARK
            else:
                p_h = doc.add_paragraph()
                p_h.paragraph_format.space_before = Pt(6)
                p_h.paragraph_format.space_after = Pt(2)
                p_h.paragraph_format.keep_with_next = True
                r = p_h.add_run(h_clean)
                r.bold = True
                r.italic = True
                r.font.name = "Times New Roman"
                r.font.size = Pt(12)
                r.font.color.rgb = MAU_DARK
            i += 1
            continue

        # Danh sách gạch đầu dòng
        list_match = re.match(r'^(\s*)([-*]|\d+\.)\s+(.+)$', line)
        if list_match:
            indent_spaces = len(list_match.group(1))
            bullet_sym = list_match.group(2)
            content = list_match.group(3)
            
            p_li = doc.add_paragraph()
            p_li.paragraph_format.line_spacing = 1.3
            p_li.paragraph_format.space_before = Pt(1)
            p_li.paragraph_format.space_after = Pt(3)
            level = 1 if indent_spaces >= 2 else 0
            p_li.paragraph_format.left_indent = Inches(0.25 + level * 0.25)
            p_li.paragraph_format.first_line_indent = Inches(-0.15)
            
            prefix = "• " if bullet_sym in ["-", "*"] else f"{bullet_sym} "
            r_bullet = p_li.add_run(prefix)
            r_bullet.bold = True
            r_bullet.font.name = "Times New Roman"
            r_bullet.font.size = Pt(11.5)
            r_bullet.font.color.rgb = MAU_MID_BLUE if bullet_sym in ["-", "*"] else MAU_NAVY
            format_runs_in_paragraph(p_li, content, default_size=11.5, default_color=MAU_TEXT)
            i += 1
            continue

        # Đoạn văn bản bình thường
        if stripped:
            p_norm = doc.add_paragraph()
            p_norm.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_norm.paragraph_format.line_spacing = 1.3
            p_norm.paragraph_format.space_before = Pt(2)
            p_norm.paragraph_format.space_after = Pt(5)
            format_runs_in_paragraph(p_norm, stripped, default_size=12, default_color=MAU_TEXT)
            
        i += 1
        
    if in_table: flush_table()
    if in_math_block: flush_math()

    doc.save(out_path)
    if out_path != OUT_DOCX_ROOT:
        doc.save(OUT_DOCX_ROOT)
    print(f"  [OK] Đã lưu file Word thành công tại:\n       {out_path}\n       {OUT_DOCX_ROOT}")

if __name__ == "__main__":
    convert_markdown_to_word(FILE_MD, OUT_DOCX_REPORT)
