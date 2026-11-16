"""Yêu cầu 4: tìm 5 tệp âm thanh giống nhất với một tệp truy vấn mới.

Sơ đồ khối (mỗi khối là một hàm, dữ liệu vào -> ra):
  K1 tien_xu_ly       tệp âm thanh bất kỳ (wav/ogg/mp3...) -> các đoạn ~3 s, mono, 22 050 Hz, chuẩn hóa đỉnh, fade
  K2 trich_vector     các đoạn -> vector 46 chiều của tệp truy vấn (trung bình vector các đoạn)
  K3 ThuVien          CSDL MySQL -> 600 vector (15 chiều truy vấn) + metadata + tham số chuẩn hóa
  K4 chuan_hoa        vector -> z-score theo bảng thong_ke_chuan_hoa (cùng thang với thư viện)
  K5 do_tuong_dong    độ tương đồng cosine giữa truy vấn và từng tệp trong thư viện
  K6 xep_hang         sắp xếp giảm dần, lấy 5 tệp đầu

Cách chạy (từ thư mục gốc project):
    .venv\\Scripts\\python.exe src\\phan4_tim_kiem\\tim_kiem.py <tệp truy vấn>
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "src" / "phan1_du_lieu"))
sys.path.insert(0, str(GOC / "src" / "phan3_dac_trung_csdl"))
import dac_trung as dt  # noqa: E402
import nap_csdl  # noqa: E402
import tao_bo_du_lieu as tb  # noqa: E402

DO_DAI = 3.0          # độ dài một đoạn (giây), giống CSDL
TOI_DA_DOAN = 20      # tệp dài: lấy tối đa 20 đoạn rải đều


# ---------- K1. Tiền xử lý ----------
def tien_xu_ly(duong_dan):
    """Tệp truy vấn -> danh sách (giây bắt đầu, tín hiệu đoạn) theo đúng quy trình của CSDL.

    Tệp ngắn (<= 3,5 s) dùng nguyên tệp. Tệp dài cắt theo ranh giới nốt như CSDL; nếu không cắt được
    (ví dụ tiếng gõ tắt nhanh nên hiếm khi có 90% khung có tiếng) thì cắt khung 3 s cố định, bỏ khung gần im lặng.
    """
    y = dt.doc_tin_hieu(duong_dan)
    if len(y) <= 3.5 * dt.SR:
        doan = [(0.0, y)]
    else:
        doan = [(t, g) for t, g, _ in tb.cat_doan(y, Path(duong_dan).name)]
        if not doan:
            n = int(DO_DAI * dt.SR)
            muc = np.sqrt(np.mean(y ** 2)) + 1e-12
            doan = [(a / dt.SR, y[a:a + n]) for a in range(0, len(y) - n + 1, n)
                    if np.sqrt(np.mean(y[a:a + n] ** 2)) / muc > 10 ** (-40 / 20)]
    if len(doan) > TOI_DA_DOAN:
        doan = [doan[i] for i in np.linspace(0, len(doan) - 1, TOI_DA_DOAN).astype(int)]
    return [(t, tb.lam_mem_mep(0.9 * g / (np.max(np.abs(g)) + 1e-9))) for t, g in doan], len(y) / dt.SR


# ---------- K2. Trích vector ----------
def trich_vector(doan):
    """Mỗi đoạn -> vector 46 chiều; vector của cả tệp = trung bình các vector đoạn."""
    bang = pd.DataFrame([dt.trich_dac_trung(g) for _, g in doan])
    bang.insert(0, "bat_dau_s", [round(t, 2) for t, _ in doan])
    return bang[dt.TEN_CHIEU].mean(), bang


# ---------- K3. Thư viện (CSDL) ----------
class ThuVien:
    """Đọc một lần từ CSDL: metadata + vector 600 tệp, tham số chuẩn hóa, danh sách chiều truy vấn."""

    def __init__(self):
        with nap_csdl.ket_noi() as cn:
            cur = cn.cursor()
            cur.execute("SELECT ten_chieu, trung_binh, do_lech_chuan, dung_truy_van FROM thong_ke_chuan_hoa ORDER BY thu_tu")
            tk = pd.DataFrame(cur.fetchall(), columns=["ten_chieu", "mu", "sigma", "dung_truy_van"]).set_index("ten_chieu")
            cur.execute("SELECT khoa, gia_tri FROM cau_hinh_truy_van")
            self.cau_hinh = dict(cur.fetchall())
            cot = ["tep_id", "ten_tep", "duong_dan", "nhac_cu", "ten_hien_thi", "nhom", "ban_thu_goc", *dt.TEN_CHIEU]
            cur.execute(f"SELECT {', '.join(cot)} FROM v_tep_dac_trung ORDER BY tep_id")
            self.bang = pd.DataFrame(cur.fetchall(), columns=cot)
        self.bang[dt.TEN_CHIEU] = self.bang[dt.TEN_CHIEU].astype(float)
        self.tk = tk.astype(float)
        self.chieu = list(tk.index[tk.dung_truy_van == 1])                      # 15 chiều truy vấn
        self.Z = self.chuan_hoa(self.bang[self.chieu])                          # 600 x 15
        self.Zn = self.Z / np.linalg.norm(self.Z, axis=1, keepdims=True)

    # ---------- K4. Chuẩn hóa ----------
    def chuan_hoa(self, x):
        """z = (x - mu) / sigma với mu, sigma lấy từ thong_ke_chuan_hoa (thang của thư viện)."""
        x = pd.DataFrame(x) if isinstance(x, pd.DataFrame) else pd.DataFrame([x])
        return ((x[self.chieu] - self.tk.loc[self.chieu, "mu"]) / self.tk.loc[self.chieu, "sigma"]).to_numpy(float)

    # ---------- K5 + K6. Độ tương đồng và xếp hạng ----------
    def tim(self, duong_dan, k=5):
        t0 = time.perf_counter()
        doan, do_dai = tien_xu_ly(duong_dan)
        vec, bang_doan = trich_vector(doan)
        t1 = time.perf_counter()
        z = self.chuan_hoa(vec)[0]
        zn = z / np.linalg.norm(z)
        sim = self.Zn @ zn                                  # cos(q, g) = (q . g) / (|q| |g|)
        top = np.argsort(-sim)[:k]
        t2 = time.perf_counter()
        kq = self.bang.iloc[top][["ten_tep", "ten_hien_thi", "nhom", "ban_thu_goc", "duong_dan"]].copy()
        kq.insert(0, "hang", range(1, k + 1))
        kq.insert(3, "do_tuong_dong", sim[top].round(4))
        # đóng góp của từng chiều vào cosine với tệp hạng 1: z_q,j * z_g,j / (|z_q| |z_g|)
        dong_gop = pd.Series(zn * self.Zn[top[0]], index=self.chieu).sort_values(ascending=False)
        return {"do_dai_s": do_dai, "so_doan": len(doan), "bang_doan": bang_doan, "vector": vec,
                "z": pd.Series(z, index=self.chieu), "ket_qua": kq.reset_index(drop=True),
                "dong_gop_hang_1": dong_gop, "sim_tat_ca": sim,
                "thoi_gian_ms": {"tien_xu_ly_va_trich": (t1 - t0) * 1000, "so_khop": (t2 - t1) * 1000}}


def in_ket_qua(r):
    print(f"Tệp truy vấn dài {r['do_dai_s']:.1f} s -> {r['so_doan']} đoạn")
    print("Vector truy vấn (15 chiều dùng để so khớp, giá trị gốc -> z-score):")
    for c in r["z"].index:
        print(f"  {c:14s} {r['vector'][c]:10.3f} -> {r['z'][c]:7.3f}")
    print("\nTop 5 tệp giống nhất (độ tương đồng cosine, giảm dần):")
    print(r["ket_qua"].drop(columns=["duong_dan"]).to_string(index=False))
    print(f"\nThời gian: tiền xử lý + trích đặc trưng {r['thoi_gian_ms']['tien_xu_ly_va_trich']:.0f} ms, "
          f"so khớp 600 tệp {r['thoi_gian_ms']['so_khop']:.2f} ms")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Cách dùng: tim_kiem.py <tệp âm thanh truy vấn>")
    in_ket_qua(ThuVien().tim(sys.argv[1]))
