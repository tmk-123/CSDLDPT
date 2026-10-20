# -*- coding: utf-8 -*-
"""
Dùng pywin32 để tự động tìm kiếm vị trí trang thực tế của từng đề mục trong file Word
với các cụm từ tìm kiếm duy nhất, đảm bảo không bị nhầm vào phần tóm tắt bố cục ở mục 1.4.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path
import win32com.client

BASE_DIR = Path(__file__).resolve().parent.parent
DOCX_PATH = str(BASE_DIR / "reports" / "Bao_cao_BTL_HCSDLDPT.docx")
JSON_PATH = BASE_DIR / "reports" / "page_mapping.json"

targets = [
    # Chương 1
    ("CHƯƠNG 1", "CHƯƠNG 1. GIỚI THIỆU"),
    ("1.1", "1.1 Đặt vấn đề"),
    ("1.2", "1.2 Mục tiêu và phạm vi"),
    ("1.3", "1.3 Định hướng giải pháp"),
    ("1.4", "1.4 Bố cục báo cáo"),
    # Chương 2
    ("CHƯƠNG 2", "CHƯƠNG 2. XÂY DỰNG"),
    ("2.1", "2.1 Nguồn dữ liệu"),
    ("2.2", "2.2 Quy cách âm thanh"),
    ("2.3", "2.3 Quy trình tiền xử lý"),
    ("2.4", "2.4 Tổ chức lưu trữ"),
    ("2.5", "2.5 Thống kê bộ dữ liệu"),
    ("2.6", "2.6 Đặc điểm giống và khác nhau"),
    ("2.6.1", "2.6.1 Đặc điểm giống nhau"),
    ("2.6.2", "2.6.2 Đặc điểm khác nhau"),
    ("2.6.3", "2.6.3 Biến thiên trong cùng nhạc cụ"),
    # Chương 3
    ("CHƯƠNG 3", "CHƯƠNG 3. BỘ ĐẶC TRƯNG"),
    ("3.1", "3.1 Tổng quan bộ đặc trưng"),
    ("3.2", "3.2 Nhóm đặc trưng thời gian"),
    ("3.3", "3.3 Nhóm đặc trưng phổ"),
    ("3.4", "3.4 Nhóm đặc trưng cao độ"),
    ("3.5", "3.5 Biểu diễn vectơ"),
    # Chương 4
    ("CHƯƠNG 4", "CHƯƠNG 4. ĐÁNH GIÁ"),
    ("4.1", "4.1 Phương pháp đánh giá"),
    ("4.1.1", "4.1.1 Đánh giá từng đặc trưng"),
    ("4.1.2", "4.1.2 Đánh giá theo nhóm"),
    ("4.2", "4.2 Khả năng phân biệt"),
    ("4.3", "4.3 Tương quan"),
    ("4.4", "4.4 Khoảng cách giữa các mẫu"),
    ("4.5", "4.5 Đóng góp của từng nhóm"),
    ("4.6", "4.6 Kết quả truy vấn minh họa"),
    # Chương 5
    ("CHƯƠNG 5", "CHƯƠNG 5. KẾT LUẬN"),
    ("5.1", "5.1 Kết quả đạt được"),
    ("5.2", "5.2 Hạn chế"),
    ("5.3", "5.3 Hướng phát triển"),
    # Tài liệu & Phụ lục
    ("TÀI LIỆU THAM KHẢO", "TÀI LIỆU THAM KHẢO"),
    ("PHỤ LỤC", "PHỤ LỤC"),
    ("A", "A. THỐNG KÊ CHI TIẾT"),
    ("A.1", "A.1. Số mẫu"),
    ("A.2", "A.2. Thống kê"),
    # Hình vẽ
    ("Hình 2.1", "Hình 2.1: Quy trình 3 bước"),
    ("Hình 2.2", "Hình 2.2: Số lượng tệp"),
    ("Hình 2.3", "Hình 2.3: Dạng sóng thời gian"),
    ("Hình 2.4", "Hình 2.4: Dải âm vực vật lý"),
    ("Hình 2.5", "Hình 2.5: So sánh phổ"),
    ("Hình 3.1", "Hình 3.1: Quy trình tổng thể"),
    ("Hình 3.2", "Hình 3.2: Chi tiết cơ chế"),
    ("Hình 4.1", "Hình 4.1: Fisher ratio"),
    ("Hình 4.2", "Hình 4.2: Phân bố theo nhạc cụ"),
    ("Hình 4.3", "Hình 4.3: Ma trận tương quan"),
    ("Hình 4.4", "Hình 4.4: Phân bố khoảng cách"),
    ("Hình 4.5", "Hình 4.5: Ba truy vấn minh họa"),
    # Bảng biểu
    ("Bảng 2.1", "Bảng 2.1: Đối chiếu yêu cầu"),
    ("Bảng 2.2", "Bảng 2.2: Cấu trúc tổ chức"),
    ("Bảng 2.3", "Bảng 2.3: So sánh đặc điểm"),
    ("Bảng 3.1", "Bảng 3.1: Tổng quan bộ 58"),
    ("Bảng 3.2", "Bảng 3.2: Công thức toán học"),
    ("Bảng 4.1", "Bảng 4.1: Xếp hạng 15"),
    ("Bảng 4.2", "Bảng 4.2: Các cặp đặc trưng"),
    ("Bảng 4.3", "Bảng 4.3: So sánh hiệu năng"),
    ("Bảng A.1", "Bảng A.1: Số mẫu và kết quả"),
    ("Bảng A.2", "Bảng A.2: Thống kê mô tả 58")
]

def main():
    print(">>> Đang khởi động Word qua win32com...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    
    try:
        print(f">>> Đang mở tài liệu: {DOCX_PATH}")
        doc = word.Documents.Open(DOCX_PATH)
        doc.Fields.Update()
        word.ActiveDocument.Repaginate()
        
        total_pages = doc.ComputeStatistics(2) # wdStatisticPages
        print(f">>> Tổng số trang Word thực tế: {total_pages} trang")
        
        start_pos = doc.GoTo(1, 1, 5).Start
        print(f">>> Bắt đầu tìm kiếm từ vị trí ký tự: {start_pos} (Trang 5)")
        
        page_mapping = {}
        curr_pos = start_pos
        for key, search_str in targets:
            # Đối với Tài liệu tham khảo và Phụ lục, bắt đầu tìm từ sau Chương 5 (trang 30 trở đi)
            if key in ["TÀI LIỆU THAM KHẢO", "PHỤ LỤC", "A", "A.1", "A.2"]:
                search_from = doc.GoTo(1, 1, 30).Start
            else:
                search_from = start_pos
                
            rng = doc.Range(search_from, doc.Content.End)
            find = rng.Find
            find.ClearFormatting()
            find.Text = search_str
            find.Forward = True
            find.Wrap = 0 # wdFindStop
            
            if find.Execute():
                pg = rng.Information(1)
                page_mapping[key] = str(pg)
                print(f"  [FOUND] {key:20s} -> Trang {pg}")
            else:
                print(f"  [NOT FOUND] {key:20s} ({search_str})")
                
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(page_mapping, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] Đã lưu bảng tra cứu số trang tại: {JSON_PATH}")
        
    finally:
        if 'doc' in locals():
            doc.Close(False)
        word.Quit()

if __name__ == "__main__":
    main()
