"""Yêu cầu 5: demo hệ thống tìm kiếm tiếng nhạc cụ bộ dây.

Cách chạy (từ thư mục gốc project):
    .venv\\Scripts\\streamlit.exe run src\\phan5_demo\\app.py
"""
import sys
from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "src" / "phan4_tim_kiem"))
import tim_kiem as tk  # noqa: E402

TAI_LEN = GOC / "data" / "truy_van" / "tai_len"
GIU_LAI = ["rms_mean", "rms_std", "zcr_mean", "zcr_std", "mfcc_5_std", "mfcc_7_std", "contrast_1_mean", "contrast_2_mean"]

st.set_page_config(page_title="Tìm kiếm tiếng nhạc cụ bộ dây", layout="wide")


@st.cache_resource
def thu_vien():
    return tk.ThuVien()


def ds_mau(tv):
    """Tệp mẫu: vài tệp của mỗi nhạc cụ trong CSDL + các tệp truy vấn ngoài."""
    mau = {}
    for nc, g in tv.bang.groupby("ten_hien_thi", sort=False):
        for p in g.duong_dan.iloc[[0, 50]]:
            mau[f"[CSDL · {nc}] {Path(p).name}"] = GOC / p
    for f in sorted((GOC / "data" / "truy_van" / "goc").rglob("*")):
        if f.suffix.lower() in (".ogg", ".wav", ".mp3", ".flac"):
            mau[f"[Ngoài CSDL · {f.parent.name}] {f.name}"] = f
    return mau


def ve_song_pho(duong_dan):
    y, sr = librosa.load(duong_dan, sr=tk.dt.SR, mono=True, duration=30)
    fig, ax = plt.subplots(2, 1, figsize=(9, 4.2), sharex=True)
    ax[0].plot(np.arange(len(y)) / sr, y, lw=0.4)
    ax[0].set_ylabel("Biên độ")
    S = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048, hop_length=512)), ref=np.max)
    librosa.display.specshow(S, sr=sr, hop_length=512, x_axis="time", y_axis="log", ax=ax[1], vmin=-70)
    ax[1].set_ylabel("Tần số (Hz)")
    ax[1].set_xlabel("Thời gian (s)" + ("  (hiển thị tối đa 30 s đầu)" if len(y) >= 30 * sr else ""))
    fig.tight_layout()
    return fig


def main():
    st.title("Tìm kiếm tiếng nhạc cụ bộ dây theo nội dung")
    tv = thu_vien()
    st.caption(f"CSDL MySQL: {len(tv.bang)} tệp, 6 nhạc cụ · so khớp {len(tv.chieu)} chiều "
               f"(MFCC 13 mean + Roll-off) · độ đo {tv.cau_hinh['do_do']} · trả về {tv.cau_hinh['so_ket_qua']} tệp")

    with st.sidebar:
        st.header("Tệp truy vấn")
        nguon = st.radio("Chọn cách nhập", ["Chọn tệp mẫu", "Tải tệp lên"])
        duong_dan = None
        if nguon == "Chọn tệp mẫu":
            mau = ds_mau(tv)
            duong_dan = mau[st.selectbox("Tệp mẫu", list(mau))]
        else:
            up = st.file_uploader("Tệp âm thanh", type=["wav", "ogg", "mp3", "flac"])
            if up:
                TAI_LEN.mkdir(parents=True, exist_ok=True)
                duong_dan = TAI_LEN / up.name
                duong_dan.write_bytes(up.getvalue())
        chay = st.button("Tìm 5 tệp giống nhất", type="primary", disabled=duong_dan is None)

    if duong_dan is None:
        st.info("Chọn hoặc tải lên một tệp âm thanh ở thanh bên trái.")
        return
    st.subheader("Tệp truy vấn")
    st.audio(str(duong_dan))
    if not chay:
        return

    with st.spinner("Đang tiền xử lý, trích đặc trưng và so khớp..."):
        r = tv.tim(duong_dan)

    st.subheader("Kết quả: 5 tệp giống nhất (độ tương đồng giảm dần)")
    for _, kq in r["ket_qua"].iterrows():
        c1, c2, c3 = st.columns([1, 3, 4])
        c1.metric(f"Hạng {kq.hang}", f"{kq.do_tuong_dong:.3f}")
        c2.markdown(f"**{kq.ten_tep}**  \n{kq.ten_hien_thi} · {kq.nhom}  \n<small>bản thu gốc: {kq.ban_thu_goc}</small>",
                    unsafe_allow_html=True)
        c3.audio(str(GOC / kq.duong_dan))
    tg = r["thoi_gian_ms"]
    st.caption(f"Tệp truy vấn dài {r['do_dai_s']:.1f} s, chia {r['so_doan']} đoạn · tiền xử lý + trích đặc trưng "
               f"{tg['tien_xu_ly_va_trich']:.0f} ms · so khớp 600 tệp {tg['so_khop']:.1f} ms")

    st.divider()
    st.subheader("Kết quả trung gian")
    t1, t2, t3, t4 = st.tabs(["Dạng sóng và phổ", "Vector truy vấn", "Độ tương đồng", "Đặc trưng giữ trong CSDL"])
    with t1:
        st.pyplot(ve_song_pho(duong_dan))
    with t2:
        bang = pd.DataFrame({"giá trị gốc": r["vector"][tv.chieu].round(3), "μ (CSDL)": tv.tk.loc[tv.chieu, "mu"].round(3),
                             "σ (CSDL)": tv.tk.loc[tv.chieu, "sigma"].round(3), "z-score": r["z"].round(3)})
        st.markdown("Mỗi chiều được chuẩn hóa: **z = (x − μ) / σ**, với μ, σ lấy từ bảng `thong_ke_chuan_hoa`.")
        st.dataframe(bang, width="stretch")
        st.markdown(f"Vector của từng đoạn ({r['so_doan']} đoạn) trước khi lấy trung bình:")
        st.dataframe(r["bang_doan"][["bat_dau_s", *tv.chieu]].round(3), width="stretch")
    with t3:
        st.markdown("Độ tương đồng cosine: **cos(q, g) = (q · g) / (‖q‖ ‖g‖)**. "
                    "Biểu đồ dưới cho biết mỗi chiều góp bao nhiêu vào độ tương đồng với tệp hạng 1.")
        dg = r["dong_gop_hang_1"]
        fig, ax = plt.subplots(figsize=(8, 3.6))
        ax.bar(dg.index, dg.values, color=["#4C72B0" if v >= 0 else "#C44E52" for v in dg.values])
        ax.set_ylabel("đóng góp vào cos")
        ax.tick_params(axis="x", rotation=60)
        fig.tight_layout()
        st.pyplot(fig)
        sim = np.sort(r["sim_tat_ca"])[::-1]
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(sim, lw=1)
        ax.scatter(range(5), sim[:5], color="red", zorder=3, label="Top 5")
        ax.set_xlabel("600 tệp trong CSDL, xếp theo độ tương đồng")
        ax.set_ylabel("cosine")
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig)
    with t4:
        st.markdown("Các chiều này **không dùng để so khớp** nhưng được lưu để giải thích kết quả: "
                    "RMS phân biệt kéo vĩ / gảy, ZCR và Spectral Contrast giúp nhận ra âm thanh không phải nhạc cụ dây.")
        tb_nhom = tv.bang.groupby("nhom")[GIU_LAI].mean().T
        bang = pd.DataFrame({"tệp truy vấn": r["vector"][GIU_LAI]}).join(tb_nhom.add_prefix("TB CSDL · "))
        st.dataframe(bang.round(4), width="stretch")


main()
