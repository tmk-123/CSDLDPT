"""Kiểm tra lợi ích "phân biệt bộ dây với nhạc cụ khác" của từng loại đặc trưng.

1. Cắt các tệp truy vấn ngoài (data/truy_van/goc) thành đoạn ~3 giây bằng đúng quy trình của CSDL
   (theo ranh giới nốt, bỏ đoạn im lặng, chuẩn hóa đỉnh 0,9, fade 50 ms) -> data/truy_van/doan/.
2. Trích 72 chiều ứng viên cho đoạn ngoài (600 tệp CSDL đọc từ ket_qua/ung_vien_dac_trung_600_tep.csv).
3. Với từng chiều, tính AUC tách "nhạc cụ dây" (600 tệp CSDL + đoạn dây chưa có trong CSDL)
   với "không phải dây" (sáo, trống). AUC = 0,5: không tách được; AUC = 1: tách hoàn toàn.

Cách chạy: .venv\\Scripts\\python.exe src\\phan4_tim_kiem\\kiem_tra_ngoai_bo_day.py
Đầu ra   : data/truy_van/doan/, ket_qua/chon_dac_trung/e9_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.metrics import roc_auc_score

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "src" / "phan1_du_lieu"))
sys.path.insert(0, str(GOC / "src" / "phan3_dac_trung_csdl"))
import dac_trung as dt  # noqa: E402
import tao_bo_du_lieu as tb  # noqa: E402

GOC_TV = GOC / "data" / "truy_van" / "goc"
DOAN = GOC / "data" / "truy_van" / "doan"
RA = GOC / "ket_qua" / "chon_dac_trung"
TOI_DA_MOI_TEP = 15          # tối đa 15 đoạn mỗi tệp gốc, để không tệp nào áp đảo


def cat_tep_ngoai():
    """Cắt từng tệp gốc thành đoạn theo đúng quy trình CSDL; trả về bảng đặc trưng của các đoạn."""
    dong = []
    for f in sorted(GOC_TV.rglob("*")):
        if f.suffix.lower() not in (".ogg", ".wav", ".mp3", ".flac"):
            continue
        nhom = f.parent.name                     # day_keo_vi / day_gay / khong_phai_day
        ten = f.stem
        y = tb.doc_mono(f)
        ds = tb.cat_doan(y, f.name)[:TOI_DA_MOI_TEP]
        if len(ds) < 3:
            # Tiếng gõ tắt rất nhanh nên hiếm khi đạt "90% khung có tiếng" -> cắt khung 3 s cố định,
            # chỉ bỏ khung gần như im lặng (RMS trung bình nhỏ hơn đỉnh của tệp quá 40 dB).
            n = int(3.0 * tb.SR)
            dinh = np.sqrt(np.mean(y ** 2)) if len(y) else 1.0
            ds = [(a / tb.SR, y[a:a + n], f.name) for a in range(0, len(y) - n + 1, n)
                  if 20 * np.log10(np.sqrt(np.mean(y[a:a + n] ** 2)) / (dinh + 1e-12) + 1e-12) > -40][:TOI_DA_MOI_TEP]
        (DOAN / nhom).mkdir(parents=True, exist_ok=True)
        for i, (t, g, _) in enumerate(ds, 1):
            g = tb.lam_mem_mep(0.9 * g / (np.max(np.abs(g)) + 1e-9))
            out = DOAN / nhom / f"{ten}_{i:02d}.wav"
            sf.write(out, g, tb.SR, subtype="PCM_16")
            dong.append({"tep": out.relative_to(GOC).as_posix(), "tep_goc": f.name, "nhom": nhom,
                         "bo_day": nhom != "khong_phai_day", **dt.trich_ung_vien(g)})
        print(f"  {nhom:15s} {f.name:40s} {len(y) / tb.SR:6.1f} s -> {len(ds)} đoạn")
    return pd.DataFrame(dong)


def main():
    print("1. Cắt tệp truy vấn ngoài thành đoạn:")
    ngoai = cat_tep_ngoai()
    ngoai.to_csv(GOC / "data" / "truy_van" / "dac_trung_doan_ngoai.csv", index=False, encoding="utf-8-sig")

    csdl = pd.read_csv(GOC / "ket_qua" / "ung_vien_dac_trung_600_tep.csv")
    csdl["bo_day"] = True
    cot = dt.TEN_CHIEU_UNG_VIEN
    tat_ca = pd.concat([csdl[cot + ["bo_day"]], ngoai[cot + ["bo_day"]]], ignore_index=True)
    nhan = (~tat_ca.bo_day).astype(int)          # 1 = không phải nhạc cụ dây
    loai_cua = dt.LOAI_CUA_CHIEU
    auc = []
    for c in cot:
        a = roc_auc_score(nhan, tat_ca[c])
        auc.append({"chieu": c, "loai": loai_cua[c], "AUC": max(a, 1 - a),
                    "huong": "không-dây cao hơn" if a >= 0.5 else "không-dây thấp hơn"})
    auc = pd.DataFrame(auc).sort_values("AUC", ascending=False)
    auc.to_csv(RA / "e9_auc_day_vs_khong_day_theo_chieu.csv", index=False, encoding="utf-8-sig")
    theo_loai = auc.groupby("loai").agg(AUC_lon_nhat=("AUC", "max"), chieu_tot_nhat=("chieu", "first"),
                                        AUC_trung_binh=("AUC", "mean")).sort_values("AUC_lon_nhat", ascending=False)
    theo_loai.to_csv(RA / "e9_auc_day_vs_khong_day_theo_loai.csv", encoding="utf-8-sig")

    so = ngoai.groupby("nhom").size()
    print(f"\nSố đoạn: dây trong CSDL 600, dây ngoài {int(so.get('day_keo_vi', 0) + so.get('day_gay', 0))}, "
          f"không phải dây {int(so.get('khong_phai_day', 0))}")
    print("\n=== E9. Tách 'nhạc cụ dây' với 'không phải dây' (AUC, theo loại) ===")
    print(theo_loai.round(3).to_string())
    print("\n10 chiều tách tốt nhất:")
    print(auc.head(10).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
