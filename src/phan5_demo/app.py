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


def giai_thich_tim_kiem(tv, r, duong_dan):
    st.subheader("Hệ thống tìm ra 5 tệp này như thế nào?")
    st.markdown(
        f"**1. Tiền xử lý:** đọc âm thanh thành mono, lấy mẫu lại ở **22.050 Hz**; "
        f"tệp truy vấn dài **{r['do_dai_s']:.2f} giây**, được xử lý thành **{r['so_doan']} đoạn**. "
        "Tệp ngắn tối đa 3,5 giây được giữ nguyên; tệp dài được cắt theo nốt "
        "(nếu không cắt được thì dùng khung 3 giây, bỏ đoạn gần im lặng), lấy tối đa 20 đoạn. "
        "Mỗi đoạn được chuẩn hóa đỉnh biên độ về 0,9 và làm mềm mép.\n\n"
        "**2. Trích đặc trưng:** phân tích các khung 2.048 mẫu, bước nhảy 512 mẫu. "
        "Tính 46 đặc trưng cho mỗi đoạn rồi lấy trung bình giữa các đoạn. "
        "Dùng **15 chiều để tìm kiếm: 13 MFCC trung bình (mô tả âm sắc) và Roll-off trung bình, "
        "độ lệch chuẩn (mô tả phân bố phổ và mức biến thiên theo thời gian)**.\n\n"
        "**3. Chuẩn hóa:** đưa từng chiều về cùng thang đo bằng trung bình μ và độ lệch chuẩn σ "
        "của thư viện; áp dụng cùng tham số cho truy vấn và các tệp trong CSDL."
    )
    st.latex(r"z_j = \frac{x_j-\mu_j}{\sigma_j}")
    st.markdown(
        f"**4. So sánh:** tính cosine giữa vector truy vấn và từng vector trong **{len(tv.bang)} tệp**. "
        "Mỗi đóng góp ở bảng chi tiết bên dưới là một số hạng trong tổng sau:"
    )
    st.latex(r"s(q,g)=\frac{\sum_{j=1}^{15}z_{q,j}z_{g,j}}{\|z_q\|_2\|z_g\|_2}"
             r"=\sum_{j=1}^{15}c_j,\qquad c_j=\frac{z_{q,j}z_{g,j}}{\|z_q\|_2\|z_g\|_2}")
    st.markdown(
        "**5. Xếp hạng:** sắp xếp toàn bộ điểm cosine giảm dần và lấy 5 tệp đầu. "
        "Tên nhạc cụ, tên tệp và nguồn thu chỉ dùng để hiển thị, không tham gia tính điểm. "
        "Cosine nằm trong khoảng −1 đến 1; càng gần 1 thì hướng vector đặc trưng càng giống nhau. "
        "Đây là điểm tương đồng, **không phải xác suất nhận diện hay phần trăm chính xác**."
    )
    if any((GOC / p).resolve() == duong_dan.resolve() for p in r["ket_qua"].duong_dan):
        st.info("Bạn đang truy vấn bằng một tệp có trong CSDL. Tệp đó vẫn được đưa vào xếp hạng, "
                "nên có thể đứng đầu với điểm gần 1. Hãy chọn mẫu Ngoài CSDL để thử âm thanh mới.")


def chi_tiet_top5(tv, r):
    kq = r["ket_qua"]
    meta = pd.read_csv(GOC / "data" / "metadata.csv").set_index("file_path")
    st.subheader("So sánh nhanh 5 kết quả")
    tong_hop = kq[["hang", "ten_tep", "ten_hien_thi", "nhom", "do_tuong_dong", "ban_thu_goc"]].copy()
    tong_hop["Độ dài (s)"] = [float(meta.loc[p, "duration_s"]) for p in kq.duong_dan]
    tong_hop = tong_hop.rename(columns={"hang": "Hạng", "ten_tep": "Tệp", "ten_hien_thi": "Nhạc cụ",
                                      "nhom": "Cách kích âm", "do_tuong_dong": "Cosine", "ban_thu_goc": "Bản thu gốc"})
    st.dataframe(tong_hop, hide_index=True, width="stretch")
    fig, ax = plt.subplots(figsize=(9, 3))
    diem = kq.do_tuong_dong.to_numpy()
    ax.barh([f"#{k.hang} · {k.ten_tep}" for k in kq.itertuples()], diem, color="#4C72B0")
    ax.invert_yaxis()
    ax.set_xlim(min(0, float(diem.min()) - 0.1), 1.15)
    for i, v in enumerate(diem):
        ax.text(v + 0.015, i, f"{v:.4f}", va="center")
    ax.set_xlabel("Điểm tương đồng cosine (càng lớn càng giống)")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Đối chiếu từng kết quả với âm thanh truy vấn")
    st.markdown(
        "**Cách đọc 5 cột:** màu xanh là **truy vấn**, màu cam là **tệp kết quả**. "
        "Hệ thống xếp hạng bằng **cosine của toàn bộ 15 chiều đã chuẩn hóa**. "
        "MFCC mô tả âm sắc; Roll-off mô tả phân bố phổ. Các biểu đồ dùng cùng thang đo để so sánh giữa các cột."
    )
    st.caption(
        "Tỉ lệ chiều gần nhau = số chiều có |z truy vấn − z kết quả| ≤ 1 chia cho 15 "
        "(chênh lệch không quá một độ lệch chuẩn CSDL). Đây là chỉ số minh họa, không dùng để xếp hạng. "
        "Điểm cosine và tỉ lệ này không phải xác suất nhận diện đúng."
    )
    q = r["z"].to_numpy(float)
    qn = q / np.linalg.norm(q)
    cac_z = [tv.chuan_hoa(tv.bang.loc[tv.bang.duong_dan == p].iloc[0][tv.chieu])[0]
             for p in kq.duong_dan]
    gioi_han = max(1.0, float(np.max(np.abs(np.array([q, *cac_z]))))) * 1.12
    mfcc = np.array([c.startswith("mfcc_") for c in tv.chieu])
    nhan = [c.replace("mfcc_", "M").replace("rolloff_", "RO ").replace("_mean", " TB")
            .replace("_std", " ĐLC") for c in tv.chieu]
    for cot, k, g in zip(st.columns(5), kq.itertuples(), cac_z):
        tep = tv.bang.loc[tv.bang.duong_dan == k.duong_dan].iloc[0]
        m = meta.loc[k.duong_dan]
        gn = g / np.linalg.norm(g)
        dong_gop = qn * gn
        chi_tiet = pd.DataFrame({"Đặc trưng": tv.chieu,
                                "Truy vấn (gốc)": r["vector"][tv.chieu].to_numpy(float),
                                "Tệp kết quả (gốc)": tep[tv.chieu].to_numpy(float),
                                "μ CSDL": tv.tk.loc[tv.chieu, "mu"].to_numpy(float),
                                "σ CSDL": tv.tk.loc[tv.chieu, "sigma"].to_numpy(float),
                                "z truy vấn": q, "z kết quả": g,
                                "Đóng góp cosine": dong_gop})
        with cot, st.container(border=True):
            st.markdown(f"### Hạng {k.hang}")
            st.markdown(f"**{k.ten_tep}**  \n{k.ten_hien_thi} · {k.nhom}")
            st.metric("Điểm cosine", f"{dong_gop.sum():.4f}", help="Điểm dùng để xếp hạng; càng gần 1 càng tương đồng về hướng vector.")
            gan = int(np.count_nonzero(np.abs(q - g) <= 1))
            st.metric("Tỉ lệ chiều gần nhau", f"{gan / len(q):.1%}", help="Chỉ số minh họa, không dùng để chọn Top 5.")
            st.caption(f"{gan}/{len(q)} chiều chênh lệch không quá 1σ của CSDL.")
            st.markdown("**Đối chiếu 15 đặc trưng**")
            fig, ax = plt.subplots(figsize=(3.6, 6.2))
            vi_tri = np.arange(len(q))
            ax.barh(vi_tri - .18, q, height=.35, color="#2878B5", label="Truy vấn")
            ax.barh(vi_tri + .18, g, height=.35, color="#F28E2B", label="Kết quả")
            ax.set_yticks(vi_tri, nhan, fontsize=9)
            ax.invert_yaxis()
            ax.set_xlim(-gioi_han, gioi_han)
            ax.axvline(0, color="gray", linewidth=.7)
            ax.set_xlabel("Giá trị z-score")
            ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=2, fontsize=8)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption("M0–M12: MFCC trung bình; RO TB/ĐLC: Roll-off trung bình/độ lệch chuẩn. "
                       "Hai thanh gần nhau biểu thị giá trị chuẩn hóa gần nhau.")
            st.markdown("**Điểm được tạo thành từ đâu?**")
            st.write(f"MFCC (13 chiều): **{dong_gop[mfcc].sum():+.4f}**")
            st.write(f"Roll-off (2 chiều): **{dong_gop[~mfcc].sum():+.4f}**")
            st.caption(f"Cộng hai phần = {dong_gop.sum():.4f}. Đây là đóng góp vào cùng một điểm cosine, không phải điểm tính riêng từng nhóm.")
            st.markdown("**Roll-off thực tế**")
            for chieu, ten in [("rolloff_mean", "Trung bình"), ("rolloff_std", "Độ lệch chuẩn")]:
                st.write(f"{ten}: {float(r['vector'][chieu]):.0f} → **{float(tep[chieu]):.0f} Hz**")
            st.caption("Thứ tự: truy vấn → kết quả. Roll-off là tần số chứa 85% tổng biên độ phổ.")
            st.markdown("**Thông tin âm thanh**")
            st.write(f"Truy vấn: **{r['do_dai_s']:.2f} s** · {r['so_doan']} đoạn")
            st.write(f"Kết quả: **{float(m.duration_s):.2f} s** · {int(m.sample_rate):,} Hz")
            st.write(f"Nguồn: **{m.source}**")
            st.caption(f"Bản thu: {k.ban_thu_goc} · cắt từ {float(m.start_s):.2f} s")
            with st.expander("Xem số liệu và phép tính"):
                st.write(f"‖z truy vấn‖ = {np.linalg.norm(q):.4f}; ‖z kết quả‖ = {np.linalg.norm(g):.4f}.")
                st.caption("Đóng góp dương làm tăng điểm, âm làm giảm điểm. Tổng 15 đóng góp bằng cosine.")
                st.dataframe(chi_tiet.round(6), hide_index=True, width="stretch")
                st.caption(f"Mã tệp: {int(tep.tep_id)} · Đường dẫn: {k.duong_dan}")
    st.caption("Các kết quả cùng bản thu gốc có thể là những đoạn cắt khác nhau của cùng một bản thu.")


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
                duong_dan = TAI_LEN / Path(up.name).name
                noi_dung = up.getvalue()
                if not duong_dan.exists() or duong_dan.read_bytes() != noi_dung:
                    duong_dan.write_bytes(noi_dung)
        chay = st.button("Tìm 5 tệp giống nhất", type="primary", disabled=duong_dan is None)

    if duong_dan is None:
        st.info("Chọn hoặc tải lên một tệp âm thanh ở thanh bên trái.")
        return
    st.subheader("Tệp truy vấn")
    st.audio(str(duong_dan))
    khoa = (str(duong_dan.resolve()), duong_dan.stat().st_mtime_ns)
    if chay:
        with st.spinner("Đang tiền xử lý, trích đặc trưng và so khớp..."):
            st.session_state["truy_van_da_chay"] = (khoa, tv.tim(duong_dan))
    da_chay = st.session_state.get("truy_van_da_chay")
    if da_chay is None or da_chay[0] != khoa:
        return
    r = da_chay[1]

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

    chi_tiet_top5(tv, r)
    giai_thich_tim_kiem(tv, r, duong_dan)

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
