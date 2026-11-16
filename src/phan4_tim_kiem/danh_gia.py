"""Yêu cầu 4c: đánh giá kết quả tìm kiếm Top 5 với cấu hình đã chốt (15 chiều, cosine).

Hệ thống chỉ trả về 5 tệp giống nhất; nhãn nhạc cụ được dùng SAU khi xếp hạng, làm "đáp án" để chấm:
một kết quả được coi là phù hợp nếu cùng nhạc cụ với tệp truy vấn.

1. Nhạc cụ đã có: chia 5 phần theo nhóm bản thu (truy vấn luôn là bản thu thư viện chưa có), lặp 5 lần.
   -> P@1, P@5, MAP@5 tổng và theo từng nhạc cụ; 5 tệp trả về thuộc những nhạc cụ nào (ma trận).
2. Nhạc cụ dây chưa có (data/truy_van/goc/day_*): không có tệp cùng nhạc cụ để đối chiếu, nên xét tính hợp lý:
   5 tệp trả về thuộc nhạc cụ nào, có cùng nhóm kéo vĩ / gảy không, độ tương đồng ra sao.
3. Thời gian một truy vấn qua toàn bộ hệ thống.

Cách chạy: .venv\\Scripts\\python.exe src\\phan4_tim_kiem\\danh_gia.py
Đầu ra   : ket_qua/danh_gia/
"""
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

matplotlib.use("Agg")
GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import tim_kiem as tk  # noqa: E402

RA = GOC / "ket_qua" / "danh_gia"
THU_TU = ["violin", "viola", "cello", "double_bass", "guitar_acoustic", "guitar_electric"]
TEN = {"violin": "Violin", "viola": "Viola", "cello": "Cello", "double_bass": "Double Bass",
       "guitar_acoustic": "Guitar Acoustic", "guitar_electric": "Guitar Electric"}
NHOM_NGOAI = {"day_keo_vi": "kéo vĩ", "day_gay": "gảy"}


def danh_gia_trong_csdl(tv, so_lan=5, k=5):
    """Đánh giá trên 600 tệp, chia theo nhóm bản thu. Trả về bảng từng truy vấn (gộp 5 lần lặp)."""
    with tk.nap_csdl.ket_noi() as cn:
        cur = cn.cursor()
        cur.execute("SELECT tep_id, nhom_ban_thu FROM tep_am_thanh ORDER BY tep_id")
        nhom_bt = dict(cur.fetchall())
    b = tv.bang
    X = b[tv.chieu].to_numpy(float)
    y, ho, g = b.nhac_cu.to_numpy(), b.nhom.to_numpy(), b.tep_id.map(nhom_bt).to_numpy()
    dong = []
    for hat in range(so_lan):
        for tv_idx, tq_idx in StratifiedGroupKFold(5, shuffle=True, random_state=hat).split(X, y, g):
            mu, sd = X[tv_idx].mean(0), X[tv_idx].std(0)
            G, Q = (X[tv_idx] - mu) / sd, (X[tq_idx] - mu) / sd
            G /= np.linalg.norm(G, axis=1, keepdims=True)
            Q /= np.linalg.norm(Q, axis=1, keepdims=True)
            S = Q @ G.T
            top = np.argsort(-S, axis=1)[:, :k]
            for i, q in enumerate(tq_idx):
                nhan = y[tv_idx][top[i]]
                rel = nhan == y[q]
                pk = np.cumsum(rel) / np.arange(1, k + 1)
                dong.append({"lan": hat, "truy_van": y[q], "nhom": ho[q], "P@1": rel[0], "P@5": rel.mean(),
                             "AP@5": (pk * rel).sum() / k, "cung_nhom_keo_vi_gay": (ho[tv_idx][top[i]] == ho[q]).mean(),
                             "sim_hang_1": S[i, top[i][0]], "sim_hang_5": S[i, top[i][-1]],
                             **{f"tra_ve_{n}": int((nhan == n).sum()) for n in THU_TU}})
    return pd.DataFrame(dong)


def bang_tong_hop(q):
    theo_lan = q.groupby("lan")[["P@1", "P@5", "AP@5", "cung_nhom_keo_vi_gay"]].mean()
    tong = pd.DataFrame({"trung_binh_%": theo_lan.mean() * 100, "do_lech_chuan_%": theo_lan.std(ddof=1) * 100}).round(2)
    tong.index = ["P@1", "P@5", "MAP@5", "P@5 cùng nhóm kéo vĩ/gảy"]
    theo_nc = (q.groupby("truy_van")[["P@1", "P@5", "AP@5", "cung_nhom_keo_vi_gay", "sim_hang_1"]].mean()
               .loc[THU_TU] * [100, 100, 100, 100, 1]).round(3)
    theo_nc.columns = ["P@1_%", "P@5_%", "MAP@5_%", "cung_nhom_%", "sim_hang_1_tb"]
    ma_tran = q.groupby("truy_van")[[f"tra_ve_{n}" for n in THU_TU]].sum().loc[THU_TU]
    ma_tran = (ma_tran.div(ma_tran.sum(1), axis=0) * 100).round(1)
    ma_tran.columns = [TEN[n] for n in THU_TU]
    ma_tran.index = [TEN[n] for n in THU_TU]
    return tong, theo_nc, ma_tran


def danh_gia_ngoai(tv):
    """Nhạc cụ dây chưa có trong CSDL: truy vấn từng tệp gốc, ghi 5 tệp trả về."""
    dong, chi_tiet = [], []
    for thu_muc, nhom in NHOM_NGOAI.items():
        for f in sorted((GOC / "data" / "truy_van" / "goc" / thu_muc).glob("*")):
            r = tv.tim(f)
            kq = r["ket_qua"]
            dong.append({"tep": f.name, "nhom_that": nhom, "so_doan": r["so_doan"],
                         "top5_nhac_cu": ", ".join(kq.ten_hien_thi), "so_cung_nhom": int((kq.nhom == nhom).sum()),
                         "sim_hang_1": kq.do_tuong_dong.iloc[0], "sim_hang_5": kq.do_tuong_dong.iloc[-1]})
            chi_tiet.append(kq.assign(tep_truy_van=f.name, nhom_that=nhom))
    return pd.DataFrame(dong), pd.concat(chi_tiet)


def do_thoi_gian(tv, so=12):
    """Thời gian chạy toàn bộ hệ thống cho một số tệp WAV của CSDL (đoạn ~3 s)."""
    t = [tv.tim(tk.GOC / p)["thoi_gian_ms"] for p in tv.bang.duong_dan.iloc[::len(tv.bang) // so][:so]]
    t = pd.DataFrame(t)
    return t.mean().round(2), t


def ve(ma_tran, theo_nc):
    fig, ax = plt.subplots(figsize=(7.5, 6))
    im = ax.imshow(ma_tran.to_numpy(), cmap="Blues", vmin=0, vmax=100)
    ax.set_xticks(range(6), ma_tran.columns, rotation=30, ha="right")
    ax.set_yticks(range(6), ma_tran.index)
    for i in range(6):
        for j in range(6):
            v = ma_tran.iat[i, j]
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", color="white" if v > 55 else "black", fontsize=9)
    ax.set_xlabel("Nhạc cụ của tệp được trả về")
    ax.set_ylabel("Nhạc cụ của tệp truy vấn")
    ax.set_title("Tỉ lệ (%) nhạc cụ trong 5 tệp trả về")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(RA / "h1_ma_tran_tra_ve.png", dpi=130)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.bar([TEN[n] for n in THU_TU], theo_nc["P@5_%"], color="#4C72B0")
    for i, v in enumerate(theo_nc["P@5_%"]):
        ax.text(i, v + 1, f"{v:.1f}", ha="center", fontsize=9)
    ax.set_ylim(0, 105)
    ax.set_ylabel("P@5 (%)")
    ax.set_title("Tỉ lệ tệp cùng nhạc cụ trong 5 kết quả, theo nhạc cụ truy vấn")
    fig.tight_layout()
    fig.savefig(RA / "h2_p5_theo_nhac_cu.png", dpi=130)
    plt.close(fig)


def main():
    RA.mkdir(parents=True, exist_ok=True)
    tv = tk.ThuVien()
    print(f"Thư viện: {len(tv.bang)} tệp; chiều truy vấn ({len(tv.chieu)}): {', '.join(tv.chieu)}; "
          f"độ đo: {tv.cau_hinh['do_do']}")

    q = danh_gia_trong_csdl(tv)
    tong, theo_nc, ma_tran = bang_tong_hop(q)
    q.to_csv(RA / "tung_truy_van.csv", index=False, encoding="utf-8-sig")
    tong.to_csv(RA / "tong_hop.csv", encoding="utf-8-sig")
    theo_nc.to_csv(RA / "theo_nhac_cu.csv", encoding="utf-8-sig")
    ma_tran.to_csv(RA / "ma_tran_tra_ve.csv", encoding="utf-8-sig")
    ve(ma_tran, theo_nc)
    print("\n=== 1. Nhạc cụ đã có (5 phần theo bản thu x 5 lần lặp = 3 000 lượt truy vấn) ===")
    print(tong.to_string())
    print("\nTheo nhạc cụ truy vấn:")
    print(theo_nc.to_string())
    print("\n5 tệp trả về thuộc nhạc cụ nào (% theo hàng):")
    print(ma_tran.to_string())

    ngoai, ngoai_ct = danh_gia_ngoai(tv)
    ngoai.to_csv(RA / "nhac_cu_chua_co.csv", index=False, encoding="utf-8-sig")
    ngoai_ct.to_csv(RA / "nhac_cu_chua_co_top5.csv", index=False, encoding="utf-8-sig")
    print("\n=== 2. Nhạc cụ dây chưa có trong CSDL ===")
    print(ngoai.to_string(index=False))
    print(f"\nĐộ tương đồng hạng 1: nhạc cụ đã có trung bình {q.sim_hang_1.mean():.3f}; "
          f"nhạc cụ chưa có trung bình {ngoai.sim_hang_1.mean():.3f}")

    tg, _ = do_thoi_gian(tv)
    tg.to_csv(RA / "thoi_gian_ms.csv", encoding="utf-8-sig")
    print("\n=== 3. Thời gian một truy vấn (tệp ~3 s, trung bình 12 lượt) ===")
    print(tg.to_string())
    print(f"\nĐã lưu vào {RA.relative_to(GOC)}")


if __name__ == "__main__":
    main()
