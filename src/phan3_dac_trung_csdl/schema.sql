-- CSDL đặc trưng âm thanh nhạc cụ bộ dây (yêu cầu 3).
-- Tệp này được sinh tự động bởi nap_csdl.py từ danh sách đặc trưng trong dac_trung.py; không sửa tay.
-- Tên CSDL lấy từ biến MYSQL_DATABASE trong .env.

CREATE TABLE nhac_cu (
  nhac_cu_id   TINYINT UNSIGNED NOT NULL PRIMARY KEY,
  ma           VARCHAR(30) NOT NULL UNIQUE,      -- mã dùng trong data/wav, ví dụ double_bass
  ten_hien_thi VARCHAR(50) NOT NULL,             -- ví dụ Double Bass
  nhom         VARCHAR(20) NOT NULL              -- nhóm theo cách kích âm: kéo vĩ / gảy
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE tep_am_thanh (
  tep_id      INT UNSIGNED NOT NULL PRIMARY KEY, -- = file_id trong data/metadata.csv
  ten_tep     VARCHAR(100) NOT NULL UNIQUE,
  duong_dan   VARCHAR(255) NOT NULL UNIQUE,      -- đường dẫn tương đối từ gốc project
  nhac_cu_id  TINYINT UNSIGNED NOT NULL,
  nguon       VARCHAR(50) NOT NULL,              -- bộ dữ liệu gốc: URMP, PHENICX-Anechoic, ...
  ban_thu_goc VARCHAR(255) NOT NULL,             -- tệp gốc mà đoạn được cắt ra
  nhom_ban_thu VARCHAR(255) NOT NULL,            -- lần ghi âm: các đoạn cùng nhóm có cùng người chơi, cùng bản nhạc
  bat_dau_s   DECIMAL(8,2) NOT NULL,             -- vị trí bắt đầu cắt trong tệp gốc (giây)
  do_dai_s    DECIMAL(6,2) NOT NULL,             -- độ dài đoạn (giây)
  tan_so_mau  INT NOT NULL,
  CONSTRAINT fk_tep_nhac_cu FOREIGN KEY (nhac_cu_id) REFERENCES nhac_cu (nhac_cu_id),
  INDEX idx_tep_nhac_cu (nhac_cu_id),
  INDEX idx_tep_nhom_ban_thu (nhom_ban_thu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dac_trung (
  tep_id           INT UNSIGNED NOT NULL PRIMARY KEY,
  rms_mean         DOUBLE NOT NULL,
  rms_std          DOUBLE NOT NULL,
  zcr_mean         DOUBLE NOT NULL,
  zcr_std          DOUBLE NOT NULL,
  rolloff_mean     DOUBLE NOT NULL,
  rolloff_std      DOUBLE NOT NULL,
  mfcc_0_mean      DOUBLE NOT NULL,
  mfcc_0_std       DOUBLE NOT NULL,
  mfcc_1_mean      DOUBLE NOT NULL,
  mfcc_1_std       DOUBLE NOT NULL,
  mfcc_2_mean      DOUBLE NOT NULL,
  mfcc_2_std       DOUBLE NOT NULL,
  mfcc_3_mean      DOUBLE NOT NULL,
  mfcc_3_std       DOUBLE NOT NULL,
  mfcc_4_mean      DOUBLE NOT NULL,
  mfcc_4_std       DOUBLE NOT NULL,
  mfcc_5_mean      DOUBLE NOT NULL,
  mfcc_5_std       DOUBLE NOT NULL,
  mfcc_6_mean      DOUBLE NOT NULL,
  mfcc_6_std       DOUBLE NOT NULL,
  mfcc_7_mean      DOUBLE NOT NULL,
  mfcc_7_std       DOUBLE NOT NULL,
  mfcc_8_mean      DOUBLE NOT NULL,
  mfcc_8_std       DOUBLE NOT NULL,
  mfcc_9_mean      DOUBLE NOT NULL,
  mfcc_9_std       DOUBLE NOT NULL,
  mfcc_10_mean     DOUBLE NOT NULL,
  mfcc_10_std      DOUBLE NOT NULL,
  mfcc_11_mean     DOUBLE NOT NULL,
  mfcc_11_std      DOUBLE NOT NULL,
  mfcc_12_mean     DOUBLE NOT NULL,
  mfcc_12_std      DOUBLE NOT NULL,
  contrast_0_mean  DOUBLE NOT NULL,
  contrast_0_std   DOUBLE NOT NULL,
  contrast_1_mean  DOUBLE NOT NULL,
  contrast_1_std   DOUBLE NOT NULL,
  contrast_2_mean  DOUBLE NOT NULL,
  contrast_2_std   DOUBLE NOT NULL,
  contrast_3_mean  DOUBLE NOT NULL,
  contrast_3_std   DOUBLE NOT NULL,
  contrast_4_mean  DOUBLE NOT NULL,
  contrast_4_std   DOUBLE NOT NULL,
  contrast_5_mean  DOUBLE NOT NULL,
  contrast_5_std   DOUBLE NOT NULL,
  contrast_6_mean  DOUBLE NOT NULL,
  contrast_6_std   DOUBLE NOT NULL,
  phien_ban        VARCHAR(200) NOT NULL,        -- tham số trích đặc trưng đã dùng
  CONSTRAINT fk_dac_trung_tep FOREIGN KEY (tep_id) REFERENCES tep_am_thanh (tep_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE thong_ke_chuan_hoa (
  ten_chieu     VARCHAR(40) NOT NULL PRIMARY KEY, -- tên một cột của bảng dac_trung
  thu_tu        TINYINT UNSIGNED NOT NULL UNIQUE, -- vị trí trong vector (1..46)
  loai          VARCHAR(20) NOT NULL,             -- MFCC, Roll-off, RMS, ZCR, Spectral Contrast
  trung_binh    DOUBLE NOT NULL,                  -- trung bình của chiều này trên toàn bộ tệp
  do_lech_chuan DOUBLE NOT NULL,                  -- độ lệch chuẩn của chiều này trên toàn bộ tệp
  dung_truy_van TINYINT(1) NOT NULL               -- 1: dùng để tính độ tương đồng khi truy vấn; 0: chỉ lưu để giải thích
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE cau_hinh_truy_van (
  khoa    VARCHAR(40) NOT NULL PRIMARY KEY,       -- tên tham số
  gia_tri VARCHAR(200) NOT NULL                   -- giá trị
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE VIEW v_tep_dac_trung AS
SELECT t.tep_id, t.ten_tep, t.duong_dan, n.ma AS nhac_cu, n.ten_hien_thi, n.nhom, t.ban_thu_goc, t.nhom_ban_thu, d.rms_mean, d.rms_std, d.zcr_mean, d.zcr_std, d.rolloff_mean, d.rolloff_std, d.mfcc_0_mean, d.mfcc_0_std, d.mfcc_1_mean, d.mfcc_1_std, d.mfcc_2_mean, d.mfcc_2_std, d.mfcc_3_mean, d.mfcc_3_std, d.mfcc_4_mean, d.mfcc_4_std, d.mfcc_5_mean, d.mfcc_5_std, d.mfcc_6_mean, d.mfcc_6_std, d.mfcc_7_mean, d.mfcc_7_std, d.mfcc_8_mean, d.mfcc_8_std, d.mfcc_9_mean, d.mfcc_9_std, d.mfcc_10_mean, d.mfcc_10_std, d.mfcc_11_mean, d.mfcc_11_std, d.mfcc_12_mean, d.mfcc_12_std, d.contrast_0_mean, d.contrast_0_std, d.contrast_1_mean, d.contrast_1_std, d.contrast_2_mean, d.contrast_2_std, d.contrast_3_mean, d.contrast_3_std, d.contrast_4_mean, d.contrast_4_std, d.contrast_5_mean, d.contrast_5_std, d.contrast_6_mean, d.contrast_6_std
FROM tep_am_thanh t
JOIN nhac_cu n ON n.nhac_cu_id = t.nhac_cu_id
JOIN dac_trung d ON d.tep_id = t.tep_id;
