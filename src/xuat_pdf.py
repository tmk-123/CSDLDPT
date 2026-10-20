# -*- coding: utf-8 -*-
"""
Xuất file Word sang PDF chuẩn xác qua win32com
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import win32com.client

BASE_DIR = Path(__file__).resolve().parent.parent
DOCX_REPORT = str(BASE_DIR / "reports" / "Bao_cao_BTL_HCSDLDPT.docx")
DOCX_ROOT   = str(BASE_DIR / "Bao_cao_BTL.docx")
PDF_REPORT  = str(BASE_DIR / "reports" / "Bao_cao_BTL_HCSDLDPT.pdf")
PDF_ROOT    = str(BASE_DIR / "Bao_cao_BTL.pdf")

def main():
    print(">>> Đang khởi động Word qua win32com để xuất PDF...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    
    try:
        print(f">>> Đang mở tài liệu: {DOCX_REPORT}")
        doc = word.Documents.Open(DOCX_REPORT)
        doc.Fields.Update()
        word.ActiveDocument.Repaginate()
        
        total_pages = doc.ComputeStatistics(2) # wdStatisticPages
        print(f">>> Tổng số trang Word: {total_pages} trang")
        
        # Lưu file docx đã cập nhật
        doc.Save()
        doc.SaveAs(DOCX_ROOT, 12) # wdFormatXMLDocument
        print("  [OK] Đã lưu file DOCX đồng bộ ở reports/ và thư mục gốc.")
        
        # Xuất PDF (17 = wdExportFormatPDF)
        print(">>> Đang xuất file PDF...")
        doc.SaveAs(PDF_REPORT, 17)
        doc.SaveAs(PDF_ROOT, 17)
        print(f"  [OK] Đã xuất PDF thành công tại:\n       {PDF_REPORT}\n       {PDF_ROOT}")
        
    finally:
        if 'doc' in locals():
            doc.Close(False)
        word.Quit()

if __name__ == "__main__":
    main()
