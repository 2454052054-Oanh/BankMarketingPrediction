import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# CẤU HÌNH HỆ THỐNG VÀ GIAO DIỆN ENTERPRISE BUSINESS INTELLIGENCE DASHBOARD
# ==============================================================================
st.set_page_config(
    page_title="Hệ thống phân tích dữ liệu và dự đoán quyết định gửi tiền tiết kiệm ngân hàng",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hệ thống thiết kế chuẩn phần mềm phân tích dữ liệu chuyên nghiệp (Enterprise BI):
# Tối giản, thanh lịch, tập trung hoàn toàn vào dữ liệu thực tế từ dataset gốc,
# không sử dụng emoji, không bịa đặt số liệu hoặc nghiệp vụ ngoài phạm vi nghiên cứu.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0F172A;
        font-size: 14px;
        line-height: 1.5;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    /* Định dạng thanh điều hướng bên trái (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: none;
        padding-top: 1.5rem;
    }

    .sidebar-title {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.35;
        margin-bottom: 4px;
    }
    .sidebar-subtitle {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.4;
        margin-bottom: 24px;
    }

    .sidebar-section-header {
        font-size: 11px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    /* Style menu điều hướng trong sidebar */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #CBD5E1 !important;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.15s ease;
        border: none;
        cursor: pointer;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.06);
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] .stRadio input[type="radio"] {
        display: none;
    }

    /* Khung thông tin hệ thống chân sidebar */
    .sidebar-info-box {
        background-color: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 12px 14px;
        margin-top: 24px;
        font-size: 12px;
        color: #94A3B8;
        line-height: 1.5;
    }

    /* Tiêu đề trang nội dung */
    .page-header-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 18px 24px;
        margin-bottom: 20px;
    }
    .page-main-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        line-height: 1.3;
    }
    .page-main-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-top: 4px;
        margin-bottom: 0;
    }

    /* Thẻ chỉ số tổng quan (KPI Metric Card) */
    .metric-panel {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 16px 18px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .metric-desc {
        font-size: 12px;
        color: #475569;
        margin-top: 6px;
        line-height: 1.4;
    }

    /* Khối nội dung chuẩn (Content Card) */
    .card-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .card-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 16px;
        line-height: 1.4;
    }

    /* Sơ đồ pipeline quy trình */
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 16px;
    }
    .pipeline-step {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-top: 3px solid #1E3A8A;
        border-radius: 4px;
        padding: 12px;
    }
    .pipeline-step-num {
        font-size: 11px;
        font-weight: 700;
        color: #1E3A8A;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .pipeline-step-title {
        font-size: 13px;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .pipeline-step-desc {
        font-size: 11.5px;
        color: #475569;
        line-height: 1.4;
    }

    /* Hộp ghi chú nghiệp vụ và cảnh báo */
    .callout-info {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid #1E3A8A;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        color: #334155;
        line-height: 1.5;
    }
    .callout-warning {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 3px solid #D97706;
        border-radius: 4px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        color: #92400E;
        line-height: 1.5;
    }

    /* Nhãn trạng thái */
    .status-badge-positive {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .status-badge-negative {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }

    /* Nút bấm chuẩn mực */
    .stButton>button {
        background-color: #1E3A8A;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 14px;
        border-radius: 4px;
        padding: 8px 16px;
        border: none;
        width: 100%;
        transition: background-color 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# NẠP DỮ LIỆU GỐC VÀ CÁC MÔ HÌNH HỌC MÁY ĐÃ KIỂM ĐỊNH (CACHED)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "dataset", "cleaned", "bank_cleaned.csv")
MODEL_DIR = os.path.join(BASE_DIR, "dataset", "model")
PROCESSED_DIR = os.path.join(BASE_DIR, "dataset", "processed")

# Đảm bảo đường dẫn figures trỏ đúng thư mục chứa 12 biểu đồ chuẩn
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
if not os.path.exists(FIGURES_DIR) or not os.path.exists(os.path.join(FIGURES_DIR, "kmeans_customer_clusters.png")):
    FIGURES_DIR = os.path.join(os.path.dirname(BASE_DIR), "figures")

METRICS_PATH = os.path.join(os.path.dirname(BASE_DIR), "reports", "advanced_model_metrics.json")
if not os.path.exists(METRICS_PATH):
    METRICS_PATH = os.path.join(BASE_DIR, "reports", "advanced_model_metrics.json")

@st.cache_data
def load_dataset():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return None

@st.cache_resource
def load_models_and_resources():
    models = {
        "XGBoost Classifier": joblib.load(os.path.join(MODEL_DIR, "xgboost_model.pkl")),
        "LightGBM Classifier": joblib.load(os.path.join(MODEL_DIR, "lightgbm_model.pkl")),
        "Random Forest Classifier": joblib.load(os.path.join(MODEL_DIR, "rf_model.pkl")),
        "Logistic Regression": joblib.load(os.path.join(MODEL_DIR, "lr_model.pkl"))
    }
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    kmeans = joblib.load(os.path.join(MODEL_DIR, "kmeans_model.pkl"))
    scaler_km = joblib.load(os.path.join(MODEL_DIR, "scaler_kmeans.pkl"))
    
    with open(os.path.join(PROCESSED_DIR, "feature_columns.json"), "r", encoding="utf-8") as f:
        feature_cols = json.load(f)
        
    metrics_data = None
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)
            
    return models, scaler, kmeans, scaler_km, feature_cols, metrics_data

df = load_dataset()
models_dict, scaler, kmeans_model, scaler_km, feature_cols, metrics_data = load_models_and_resources()

# ==============================================================================
# SIDEBAR ĐIỀU HƯỚNG PHÂN HỆ CHỨC NĂNG
# ==============================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">Phân tích Dữ liệu Tiếp thị Ngân hàng</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Hệ thống phân tích khách hàng và dự đoán quyết định gửi tiền tiết kiệm</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section-header">Phân hệ chức năng</div>', unsafe_allow_html=True)
    selected_page = st.radio(
        label="Chọn phân hệ làm việc:",
        options=[
            "Tổng quan dữ liệu & Khám phá EDA",
            "Phân tích hành vi & Phân cụm K-Means",
            "Đánh giá mô hình & Diễn giải SHAP",
            "Chấm điểm & Dự đoán gửi tiết kiệm"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="sidebar-section-header">Thuật toán phân loại</div>', unsafe_allow_html=True)
    selected_model_name = st.selectbox(
        label="Thuật toán sử dụng:",
        options=list(models_dict.keys()),
        index=0,
        label_visibility="collapsed",
        help="Lựa chọn thuật toán học máy được áp dụng cho phân hệ đánh giá và dự đoán."
    )
    active_model = models_dict[selected_model_name]
    
    st.markdown("""
    <div class="sidebar-info-box">
        <strong>Thông số dataset gốc:</strong><br>
        • Nguồn: UCI Bank Marketing<br>
        • Tổng số mẫu: 45.211 bản ghi<br>
        • Số thuộc tính: 17 biến độc lập<br>
        • Biến mục tiêu: deposit (no / yes)<br>
        • Tỷ lệ lớp Yes: 11,70% (5.289 mẫu)<br>
        • Tỷ lệ mất cân bằng: 7,55 : 1
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# PHÂN HỆ 1: TỔNG QUAN DỮ LIỆU & KHÁM PHÁ EDA
# ==============================================================================
if selected_page == "Tổng quan dữ liệu & Khám phá EDA":
    st.markdown("""
    <div class="page-header-box">
        <div class="page-main-title">Tổng quan dữ liệu và phân tích đặc điểm khách hàng</div>
        <div class="page-main-subtitle">Khảo sát toàn bộ 45.211 hồ sơ từ dataset gốc, phân tích quy trình phương pháp luận và trực quan hóa phân bố các thuộc tính.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Bốn thẻ KPI tính toán trực tiếp từ dữ liệu gốc
    if df is not None:
        total_records = len(df)
        yes_records = int((df['target'] == 1).sum())
        no_records = int((df['target'] == 0).sum())
        yes_pct = (yes_records / total_records) * 100
        imbalance_val = no_records / yes_records if yes_records > 0 else 0
        housing_records = int((df['housing'] == 'yes').sum())
        housing_pct = (housing_records / total_records) * 100
        
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="metric-panel">
                <div class="metric-label">Tổng số bản ghi khách hàng</div>
                <div class="metric-value">{total_records:,}</div>
                <div class="metric-desc">Dữ liệu thực tế từ ngân hàng bán lẻ Bồ Đào Nha, 100% đầy đủ không khuyết thiếu.</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="metric-panel">
                <div class="metric-label">Khách hàng đồng ý mở sổ (Yes)</div>
                <div class="metric-value">{yes_records:,}</div>
                <div class="metric-desc">Tỷ lệ chuyển đổi tự nhiên của chiến dịch tiếp thị đạt {yes_pct:.2f}%.</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="metric-panel">
                <div class="metric-label">Khách hàng từ chối mở sổ (No)</div>
                <div class="metric-value">{no_records:,}</div>
                <div class="metric-desc">Chiếm 88,30% tổng số cuộc gọi, tạo ra độ mất cân bằng {imbalance_val:.2f} : 1.</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="metric-panel">
                <div class="metric-label">Khách hàng có nợ vay mua nhà</div>
                <div class="metric-value">{housing_records:,}</div>
                <div class="metric-desc">Chiếm {housing_pct:.2f}% khách hàng, là nghĩa vụ tài chính ảnh hưởng lớn đến quyết định gửi tiền.</div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Quy trình tiền xử lý dữ liệu chuẩn hóa và ngăn ngừa rò rỉ phân phối
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Quy trình tiền xử lý dữ liệu chuẩn hóa và ngăn ngừa rò rỉ phân phối</div>
        <div class="card-subtitle">Quy trình 5 bước kỹ thuật được thiết kế nghiêm ngặt nhằm tránh rò rỉ thông tin phân phối từ tập kiểm tra vào tập huấn luyện.</div>
        <div class="pipeline-grid">
            <div class="pipeline-step">
                <div class="pipeline-step-num">Bước 1</div>
                <div class="pipeline-step-title">Phân chia phân tầng</div>
                <div class="pipeline-step-desc">Tách 80% Train (36.168 mẫu) và 20% Test (9.043 mẫu) bằng Stratified Sampling để cố định chính xác tỷ lệ nhãn 11,70% trên cả 2 tập.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-step-num">Bước 2</div>
                <div class="pipeline-step-title">IQR Capping độc lập</div>
                <div class="pipeline-step-desc">Tính ngưỡng ngoại lai [Q1 - 1.5*IQR, Q3 + 1.5*IQR] độc lập trên Train, kéo biên cho balance, duration, campaign để bảo toàn khách VIP.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-step-num">Bước 3</div>
                <div class="pipeline-step-title">Rời rạc hóa (Binning)</div>
                <div class="pipeline-step-desc">Nhóm độ tuổi (&lt;25, 25-34, 35-44, 45-54, 55-64, ≥65) và thời lượng gọi để phát hiện quy luật phi tuyến tính hình chữ U.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-step-num">Bước 4</div>
                <div class="pipeline-step-title">One-Hot Encoding</div>
                <div class="pipeline-step-desc">Mã hóa 9 biến định danh sang ma trận 42 chiều với <code>drop_first=True</code> nhằm triệt tiêu hoàn toàn bẫy đa cộng tuyến dummy variable trap.</div>
            </div>
            <div class="pipeline-step">
                <div class="pipeline-step-num">Bước 5</div>
                <div class="pipeline-step-title">Chuẩn hóa StandardScaler</div>
                <div class="pipeline-step-desc">Chỉ khớp (fit) bộ chuẩn hóa trên tập Train và chuyển đổi (transform) trên tập Test, chống rò rỉ phân phối dữ liệu tuyệt đối.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Phân tích chuyển đổi theo đặc tính nhân khẩu học
    demo_img_path = os.path.join(FIGURES_DIR, "demographics_conversion.png")
    if os.path.exists(demo_img_path):
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Phân tích tỷ lệ chuyển đổi khách hàng theo đặc tính nhân khẩu học</div>
            <div class="card-subtitle">Khảo sát tỷ lệ gửi tiền tiết kiệm (%) theo 3 khía cạnh: Nhóm tuổi, 12 Nhóm nghề nghiệp và Trình độ học vấn.</div>
        """, unsafe_allow_html=True)
        st.image(demo_img_path, caption="Phân tích tỷ lệ mở sổ tiết kiệm (%) theo nhóm tuổi, 12 nhóm nghề nghiệp và trình độ học vấn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Hai biểu đồ bổ trợ: Tương quan Pearson và Tác động tài chính
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        corr_img_path = os.path.join(FIGURES_DIR, "correlation_heatmap.png")
        if os.path.exists(corr_img_path):
            st.markdown("""
            <div class="card-container">
                <div class="card-title">Ma trận tương quan Pearson giữa các thuộc tính định lượng</div>
                <div class="card-subtitle">Khảo sát mối quan hệ tuyến tính giữa các biến số độc lập và biến mục tiêu target.</div>
            """, unsafe_allow_html=True)
            st.image(corr_img_path, caption="Hệ số tương quan Pearson giữa các thuộc tính định lượng và Biến mục tiêu", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        fin_img_path = os.path.join(FIGURES_DIR, "financial_impact.png")
        if os.path.exists(fin_img_path):
            st.markdown("""
            <div class="card-container">
                <div class="card-title">Tác động của các yếu tố tài chính đến quyết định gửi tiền</div>
                <div class="card-subtitle">Phân phối số dư tài khoản và sự suy giảm tỷ lệ mở sổ do áp lực nợ vay nhà/tiêu dùng.</div>
            """, unsafe_allow_html=True)
            st.image(fin_img_path, caption="Phân phối số dư và tác động của khoản nợ vay mua nhà (housing), vay tiêu dùng (loan)", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 5. Ảnh hưởng của bối cảnh tiếp thị (Thời lượng và số lần gọi)
    camp_img_path = os.path.join(FIGURES_DIR, "campaign_duration_effect.png")
    if os.path.exists(camp_img_path):
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Ảnh hưởng của bối cảnh tiếp thị (Thời lượng cuộc gọi và Tần suất liên hệ)</div>
            <div class="card-subtitle">Mối liên hệ giữa độ dài cuộc đàm thoại và số lần gọi điện trong chiến dịch với tỷ lệ gửi tiền thành công.</div>
        """, unsafe_allow_html=True)
        st.image(camp_img_path, caption="Tỷ lệ chốt thành công theo thời lượng cuộc gọi và đường suy giảm hiệu quả sau 3 lần gọi", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 6. Bảng trích xuất dữ liệu gốc
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Dữ liệu thực tế từ tập dữ liệu gốc (10 bản ghi đầu tiên)</div>
        <div class="card-subtitle">Đối chiếu trực tiếp 16 thuộc tính độc lập và biến mục tiêu deposit từ dataset đã nạp.</div>
    """, unsafe_allow_html=True)
    if df is not None:
        st.dataframe(df.head(10), use_container_width=True, hide_index=False)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PHÂN HỆ 2: PHÂN TÍCH HÀNH VI & PHÂN CỤM K-MEANS
# ==============================================================================
elif selected_page == "Phân tích hành vi & Phân cụm K-Means":
    st.markdown("""
    <div class="page-header-box">
        <div class="page-main-title">Phân tích hành vi khách hàng và phân khúc tự động bằng K-Means</div>
        <div class="page-main-subtitle">Phát hiện quy luật độ tuổi hình chữ U, tác động của nghĩa vụ tài chính và phân khúc tự động khách hàng bằng K-Means (K = 3).</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Đồ thị phương pháp Elbow và phân cụm K-Means
    km_img_path = os.path.join(FIGURES_DIR, "kmeans_customer_clusters.png")
    if os.path.exists(km_img_path):
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Phân khúc khách hàng tự động và tối ưu hóa số cụm bằng phương pháp Elbow</div>
            <div class="card-subtitle">Đồ thị bên trái biểu diễn điểm gãy khuỷu tay (Elbow Point) tại K = 3; đồ thị bên phải minh họa 3 phân khúc khách hàng cùng trọng tâm cụm (Centroids chữ X đỏ).</div>
        """, unsafe_allow_html=True)
        st.image(km_img_path, caption="Phương pháp Elbow xác định số cụm tối ưu (K = 3) và không gian phân cụm khách hàng K-Means kèm các trọng tâm cụm (Centroids)", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Bảng thông số chi tiết 3 phân cụm K-Means tính toán động từ dữ liệu
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Bảng thống kê đặc trưng và tỷ lệ mở sổ tiết kiệm của 3 phân cụm K-Means</div>
        <div class="card-subtitle">Dữ liệu được tính toán động trực tiếp từ 45.211 bản ghi sau khi phân cụm.</div>
    """, unsafe_allow_html=True)
    if df is not None:
        df_km = df.copy()
        X_scaled_km = scaler_km.transform(df_km[['age', 'balance']])
        df_km['cluster_id'] = kmeans_model.predict(X_scaled_km)
        
        cluster_labels = {
            0: "Cụm 0: Đại chúng trẻ tích lũy cơ bản",
            1: "Cụm 1: Khách hàng lớn tuổi / Hưu trí",
            2: "Cụm 2: Khách hàng tích lũy cao (VIP)"
        }
        df_km['ten_cum'] = df_km['cluster_id'].map(cluster_labels)
        
        km_summary = df_km.groupby('cluster_id').agg(
            so_luong=('age', 'count'),
            tuoi_tb=('age', lambda x: round(x.mean(), 1)),
            so_du_tb=('balance', lambda x: round(x.mean(), 1)),
            ty_le_gui=('target', lambda x: round(x.mean() * 100, 2))
        ).reset_index()
        km_summary['ty_le_mau'] = km_summary['so_luong'].apply(lambda x: f"{round(x/len(df)*100, 2)}% ({x:,})")
        km_summary['ten_cum'] = km_summary['cluster_id'].map(cluster_labels)
        
        dinh_huong = {
            0: "Gói tích lũy số định kỳ tự động qua Mobile Banking, số tiền gửi ban đầu nhỏ.",
            1: "Gói tiết kiệm dưỡng già an nhàn, nhận lãi định kỳ hàng tháng, ưu tiên tiếp cận tại quầy.",
            2: "Chuyên viên quản lý tài sản riêng (RM), kỳ hạn dài 12 - 24 tháng kèm chính sách lãi suất bậc thang."
        }
        km_summary['dinh_huong'] = km_summary['cluster_id'].map(dinh_huong)
        
        df_km_show = km_summary[['ten_cum', 'ty_le_mau', 'tuoi_tb', 'so_du_tb', 'ty_le_gui', 'dinh_huong']]
        df_km_show.columns = ['Phân cụm khách hàng', 'Quy mô mẫu', 'Tuổi trung bình', 'Số dư TB (EUR)', 'Tỷ lệ gửi tiền (%)', 'Định hướng tiếp cận tiếp thị']
        st.dataframe(df_km_show, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Phân tích hành vi tương tác: Độ tuổi hình chữ U & Rào cản nợ vay
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Tỷ lệ đồng ý gửi tiền theo nhóm tuổi (Quy luật hình chữ U)</div>
            <div class="card-subtitle">Tỷ lệ phần trăm khách hàng gửi tiền trong từng khoảng độ tuổi.</div>
        """, unsafe_allow_html=True)
        if df is not None:
            df['age_group'] = pd.cut(df['age'], bins=[17, 25, 35, 45, 55, 65, 100], labels=['< 25', '25 - 34', '35 - 44', '45 - 54', '55 - 64', '≥ 65'])
            age_agg = df.groupby('age_group', observed=False).agg(
                so_khach=('target', 'count'),
                ty_le_gui=('target', lambda x: round(x.mean() * 100, 2))
            ).reset_index()
            
            fig_age = go.Figure()
            fig_age.add_trace(go.Bar(
                x=age_agg['age_group'],
                y=age_agg['so_khach'],
                name='Số lượng khách hàng',
                marker_color='#CBD5E1',
                yaxis='y'
            ))
            fig_age.add_trace(go.Scatter(
                x=age_agg['age_group'],
                y=age_agg['ty_le_gui'],
                name='Tỷ lệ gửi tiền (%)',
                marker=dict(color='#1E3A8A', size=8),
                line=dict(color='#1E3A8A', width=2.5),
                yaxis='y2'
            ))
            fig_age.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(title='Số lượng khách', showgrid=False),
                yaxis2=dict(title='Tỷ lệ gửi (%)', overlaying='y', side='right', range=[0, 50], showgrid=True, gridcolor='#F1F5F9'),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified'
            )
            st.plotly_chart(fig_age, use_container_width=True)
            st.caption("Nhận xét: Tỷ lệ mở sổ đạt đỉnh ở nhóm dưới 25 tuổi (23,95%) và nhóm trên 65 tuổi (42,61%), trong khi độ tuổi lao động chính (35-54) có tỷ lệ thấp hơn (< 10%).")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_b2:
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Tác động của nghĩa vụ nợ vay lên quyết định gửi tiền</div>
            <div class="card-subtitle">So sánh trực tiếp tỷ lệ gửi tiền giữa nhóm có nợ và không có nợ.</div>
        """, unsafe_allow_html=True)
        if df is not None:
            h_no = df[df['housing'] == 'no']['target'].mean() * 100
            h_yes = df[df['housing'] == 'yes']['target'].mean() * 100
            l_no = df[df['loan'] == 'no']['target'].mean() * 100
            l_yes = df[df['loan'] == 'yes']['target'].mean() * 100
            
            debt_table = [
                {"Nghĩa vụ nợ": "Không nợ nhà (housing=no)", "Tỷ lệ gửi tiền (%)": round(h_no, 2)},
                {"Nghĩa vụ nợ": "Có nợ nhà (housing=yes)", "Tỷ lệ gửi tiền (%)": round(h_yes, 2)},
                {"Nghĩa vụ nợ": "Không nợ tiêu dùng (loan=no)", "Tỷ lệ gửi tiền (%)": round(l_no, 2)},
                {"Nghĩa vụ nợ": "Có nợ tiêu dùng (loan=yes)", "Tỷ lệ gửi tiền (%)": round(l_yes, 2)}
            ]
            fig_debt = px.bar(
                pd.DataFrame(debt_table),
                x='Nghĩa vụ nợ',
                y='Tỷ lệ gửi tiền (%)',
                text='Tỷ lệ gửi tiền (%)',
                color_discrete_sequence=['#475569']
            )
            fig_debt.update_traces(texttemplate='%{text}%', textposition='outside')
            fig_debt.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(range=[0, 22], title='Tỷ lệ gửi tiền (%)', showgrid=True, gridcolor='#F1F5F9'),
                xaxis=dict(title='')
            )
            st.plotly_chart(fig_debt, use_container_width=True)
            st.caption("Nhận xét: Nợ vay mua nhà làm tỷ lệ gửi tiền giảm hơn 2,17 lần (từ 16,70% xuống 7,70%). Nợ tiêu dùng làm giảm 1,90 lần (từ 12,66% xuống 6,68%).")
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PHÂN HỆ 3: ĐÁNH GIÁ MÔ HÌNH & DIỄN GIẢI SHAP
# ==============================================================================
elif selected_page == "Đánh giá mô hình & Diễn giải SHAP":
    st.markdown("""
    <div class="page-header-box">
        <div class="page-main-title">Đánh giá hiệu năng mô hình học máy và diễn giải bằng SHAP</div>
        <div class="page-main-subtitle">Khảo sát toàn diện hiệu năng phân loại trên 9.043 mẫu kiểm tra độc lập, kiểm soát rủi ro Data Leakage và minh bạch hóa cơ chế dự báo bằng SHAP.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Bảng tổng hợp hiệu năng các mô hình phân loại trên tập kiểm tra độc lập
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Bảng tổng hợp hiệu năng các mô hình học máy trên tập kiểm tra độc lập (9.043 mẫu)</div>
        <div class="card-subtitle">Đánh giá đa chiều qua 7 chỉ số kiểm định độc lập và kiểm định chéo 5-Fold Stratified Cross-Validation.</div>
    """, unsafe_allow_html=True)
    
    if metrics_data:
        rows = []
        for k, v in metrics_data.items():
            acc = v['Accuracy']
            prec = v['Precision']
            rec = v['Recall']
            f1 = v['F1-Score']
            roc = v['ROC-AUC']
            pr = v['PR-AUC']
            cv_m = v['CV_Mean_AUC']
            cv_s = v['CV_Std_AUC']
            
            rows.append({
                "Thuật toán": k,
                "Accuracy": f"{acc*100:.2f}%",
                "Precision": f"{prec*100:.2f}%",
                "Recall (Độ nhạy)": f"{rec*100:.2f}%",
                "F1-Score": f"{f1:.4f}",
                "PR-AUC": f"{pr:.4f}",
                "ROC-AUC": f"{roc:.4f}",
                "5-Fold CV AUC": f"{cv_m:.4f} (±{cv_s:.3f})"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Biểu đồ so sánh trực quan hiệu năng các mô hình học máy
    comp_img_path = os.path.join(FIGURES_DIR, "model_comparison_metrics.png")
    if os.path.exists(comp_img_path):
        st.markdown("""
        <div class="card-container">
            <div class="card-title">So sánh trực quan 5 chỉ số hiệu năng của các thuật toán phân loại</div>
            <div class="card-subtitle">So sánh trực quan giữa Logistic Regression, Random Forest, XGBoost và LightGBM trên toàn bộ các thước đo đánh giá.</div>
        """, unsafe_allow_html=True)
        st.image(comp_img_path, caption="So sánh đa chiều các chỉ số Accuracy, Recall, F1-Score, ROC-AUC và PR-AUC trên 9.043 mẫu kiểm tra độc lập", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Đánh giá phân loại đa chiều: ROC, PR Curve và Ma trận nhầm lẫn
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Đánh giá phân loại đa chiều: Đường cong ROC, Precision-Recall và Ma trận nhầm lẫn</div>
        <div class="card-subtitle">Kiểm định khả năng phân tách nhãn trong điều kiện mất cân bằng dữ liệu 7,55 : 1.</div>
    """, unsafe_allow_html=True)
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        roc_img_path = os.path.join(FIGURES_DIR, "roc_curves_advanced.png")
        if os.path.exists(roc_img_path):
            st.image(roc_img_path, caption="Đường cong ROC và diện tích dưới đường cong (ROC-AUC đạt 0,9309)", use_container_width=True)
    with col_r2:
        pr_img_path = os.path.join(FIGURES_DIR, "pr_curves_advanced.png")
        if os.path.exists(pr_img_path):
            st.image(pr_img_path, caption="Đường cong Precision-Recall và diện tích PR-AUC (PR-AUC đạt 0,6227)", use_container_width=True)
    with col_r3:
        cm_img_path = os.path.join(FIGURES_DIR, "confusion_matrices_advanced.png")
        if os.path.exists(cm_img_path):
            st.image(cm_img_path, caption="Ma trận nhầm lẫn (Confusion Matrix) tổng hợp của 4 mô hình phân loại", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. Phân tích đối chứng định lượng rủi ro rò rỉ dữ liệu (Look-ahead Bias)
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Phân tích đối chứng định lượng rủi ro rò rỉ dữ liệu (Look-ahead Bias)</div>
        <div class="card-subtitle">So sánh định lượng giữa Kịch bản thực tế trước cuộc gọi (Pre-call) và Kịch bản đối chứng sau cuộc gọi (Post-call).</div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1.1, 1])
    with col_l1:
        leak_img_path = os.path.join(FIGURES_DIR, "pre_vs_post_call_leakage.png")
        if os.path.exists(leak_img_path):
            st.image(leak_img_path, caption="Đối chứng hiệu năng mô hình giữa Kịch bản trước cuộc gọi (Pre-call) và Kịch bản sau cuộc gọi (Post-call)", use_container_width=True)
    with col_l2:
        st.markdown("""
        <div class="callout-warning">
            <strong>Bản chất Look-ahead bias:</strong> Trước khi tổng đài viên bấm máy, cuộc gọi chưa diễn ra nên <code>duration</code> thực tế bằng 0. Nếu sử dụng duration để chấm điểm danh sách khách hàng cần gọi, mô hình đã vô tình lấy thông tin của tương lai mà thực tế không thể có.
        </div>
        """, unsafe_allow_html=True)
        leak_data = [
            {"Kịch bản": "Kịch bản A (Trước cuộc gọi - Pre-call)", "Số biến": 41, "ROC-AUC": "0,8036", "PR-AUC": "0,4725", "Vận hành thực tế": "Xếp hạng danh sách khách hàng trước khi bấm máy"},
            {"Kịch bản": "Kịch bản B (Sau cuộc gọi - Post-call)", "Số biến": 42, "ROC-AUC": "0,9309", "PR-AUC": "0,6227", "Mục đích đối chứng": "Đánh giá chất lượng cuộc gọi sau đàm thoại"}
        ]
        st.dataframe(pd.DataFrame(leak_data), use_container_width=True, hide_index=True)
        st.caption("Nhận định học thuật: Khoảng cách chênh lệch ROC-AUC là 0,1273 (từ 0,8036 lên 0,9309) chính là thước đo định lượng cho mức độ rò rỉ dữ liệu của thuộc tính thời lượng cuộc gọi.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 5. Diễn giải mô hình và xếp hạng tầm quan trọng bằng SHAP
    st.markdown("""
    <div class="card-container">
        <div class="card-title">Giải thích cơ chế ra quyết định của mô hình và tầm quan trọng thuộc tính bằng SHAP</div>
        <div class="card-subtitle">Ứng dụng lý thuyết trò chơi hợp tác của giải Nobel Kinh tế Lloyd Shapley để xóa bỏ định kiến 'hộp đen' và minh bạch hóa cơ chế ra quyết định.</div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        shap_b_path = os.path.join(FIGURES_DIR, "shap_summary_beeswarm.png")
        if os.path.exists(shap_b_path):
            st.image(shap_b_path, caption="Biểu đồ SHAP Summary Beeswarm: Chiều hướng và mức độ tác động của từng đặc trưng đến kết quả dự đoán", use_container_width=True)
    with col_s2:
        shap_i_path = os.path.join(FIGURES_DIR, "shap_importance_bar.png")
        if os.path.exists(shap_i_path):
            st.image(shap_i_path, caption="Biểu đồ SHAP Global Feature Importance (|mean SHAP value|): Xếp hạng mức độ đóng góp toàn cục", use_container_width=True)
            
    st.markdown("""
    <div class="callout-info">
        <strong>4 bài học nghiệp vụ ngân hàng rút ra từ phân tích SHAP:</strong><br>
        1. <strong>Biến thời lượng (duration):</strong> Chi phối áp đảo điểm số dự báo ở kịch bản sau cuộc gọi (cuộc gọi trên 5 phút nâng tỷ lệ chốt lên gần 50%).<br>
        2. <strong>Khách hàng tái tục (poutcome_success):</strong> Điểm đỏ có SHAP dương rất cao; khách hàng từng gửi tiền thành công trong quá khứ có xác suất gửi tiền cao gấp 5,4 lần khách hàng mới.<br>
        3. <strong>Nghĩa vụ tài chính nợ vay (housing_yes & loan_yes):</strong> Mang giá trị SHAP âm rõ rệt, là rào cản thanh khoản lớn nhất làm thâm hụt dòng tiền nhàn rỗi của khách hàng.<br>
        4. <strong>Kỷ luật tần suất gọi (campaign):</strong> Giá trị SHAP chuyển sang âm khi số lần gọi vượt quá 3 lần; chứng minh thực nghiệm ngân hàng không nên gọi quá 3 lần để tránh phản ứng tiêu cực.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PHÂN HỆ 4: CHẤM ĐIỂM & DỰ ĐOÁN GỬI TIẾT KIỆM
# ==============================================================================
elif selected_page == "Chấm điểm & Dự đoán gửi tiết kiệm":
    st.markdown(f"""
    <div class="page-header-box">
        <div class="page-main-title">Chấm điểm tiềm năng và dự đoán quyết định gửi tiền tiết kiệm</div>
        <div class="page-main-subtitle">Hệ thống hỗ trợ ra quyết định thời gian thực, điều chỉnh ngưỡng phân loại và tính toán xác suất mở sổ với mô hình <strong>{selected_model_name}</strong>.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_form, col_pred = st.columns([1.15, 1])
    
    with col_form:
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Biểu mẫu nhập thông tin khách hàng</div>
            <div class="card-subtitle">Các trường nhập liệu tương ứng chính xác với 16 thuộc tính độc lập của dataset.</div>
        """, unsafe_allow_html=True)
        
        # Chọn mẫu hồ sơ
        preset_choice = st.selectbox(
            label="Chọn mẫu hồ sơ đánh giá nhanh:",
            options=[
                "Tự nhập dữ liệu tùy chỉnh",
                "Khách hàng lớn tuổi có số dư cao, từng gửi tiền thành công",
                "Khách hàng trẻ tuổi, không có nghĩa vụ nợ",
                "Khách hàng đang chịu áp lực nợ vay mua nhà và tiêu dùng"
            ]
        )
        
        # Thiết lập giá trị mặc định theo mẫu hồ sơ
        if preset_choice == "Khách hàng lớn tuổi có số dư cao, từng gửi tiền thành công":
            d_age, d_job, d_mar, d_edu = 62, "retired", "married", "tertiary"
            d_bal, d_def, d_hou, d_loa = 4500, "no", "no", "no"
            d_con, d_day, d_mon, d_dur = "cellular", 15, "oct", 360
            d_cam, d_pda, d_pre, d_pout = 1, 90, 2, "success"
        elif preset_choice == "Khách hàng trẻ tuổi, không có nghĩa vụ nợ":
            d_age, d_job, d_mar, d_edu = 23, "student", "single", "secondary"
            d_bal, d_def, d_hou, d_loa = 650, "no", "no", "no"
            d_con, d_day, d_mon, d_dur = "cellular", 10, "apr", 240
            d_cam, d_pda, d_pre, d_pout = 1, -1, 0, "unknown"
        elif preset_choice == "Khách hàng đang chịu áp lực nợ vay mua nhà và tiêu dùng":
            d_age, d_job, d_mar, d_edu = 38, "blue-collar", "married", "secondary"
            d_bal, d_def, d_hou, d_loa = 120, "no", "yes", "yes"
            d_con, d_day, d_mon, d_dur = "cellular", 18, "may", 90
            d_cam, d_pda, d_pre, d_pout = 4, -1, 0, "unknown"
        else:
            d_age, d_job, d_mar, d_edu = 40, "management", "married", "tertiary"
            d_bal, d_def, d_hou, d_loa = 1500, "no", "yes", "no"
            d_con, d_day, d_mon, d_dur = "cellular", 15, "may", 180
            d_cam, d_pda, d_pre, d_pout = 2, -1, 0, "unknown"
            
        st.markdown("**1. Thông tin nhân khẩu học:**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            inp_age = st.number_input("Tuổi (age):", min_value=18, max_value=95, value=d_age, step=1)
        with c2:
            job_opts = ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed', 'services', 'student', 'technician', 'unemployed', 'unknown']
            inp_job = st.selectbox("Nghề nghiệp (job):", job_opts, index=job_opts.index(d_job))
        with c3:
            mar_opts = ['married', 'single', 'divorced']
            inp_mar = st.selectbox("Hôn nhân (marital):", mar_opts, index=mar_opts.index(d_mar))
        with c4:
            edu_opts = ['primary', 'secondary', 'tertiary', 'unknown']
            inp_edu = st.selectbox("Học vấn (education):", edu_opts, index=edu_opts.index(d_edu))
            
        st.markdown("**2. Năng lực tài chính & Nợ vay:**")
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            inp_bal = st.number_input("Số dư (balance EUR):", min_value=-8000, max_value=105000, value=d_bal, step=100)
        with c6:
            inp_def = st.selectbox("Nợ xấu (default):", ['no', 'yes'], index=0 if d_def=='no' else 1)
        with c7:
            inp_hou = st.selectbox("Vay mua nhà (housing):", ['no', 'yes'], index=0 if d_hou=='no' else 1)
        with c8:
            inp_loa = st.selectbox("Vay tiêu dùng (loan):", ['no', 'yes'], index=0 if d_loa=='no' else 1)
            
        st.markdown("**3. Bối cảnh cuộc gọi & Lịch sử tiếp thị:**")
        c9, c10, c11, c12 = st.columns(4)
        with c9:
            con_opts = ['cellular', 'telephone', 'unknown']
            inp_con = st.selectbox("Kênh liên hệ (contact):", con_opts, index=con_opts.index(d_con))
        with c10:
            inp_day = st.number_input("Ngày trong tháng (day):", min_value=1, max_value=31, value=d_day, step=1)
        with c11:
            mon_opts = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            inp_mon = st.selectbox("Tháng liên hệ (month):", mon_opts, index=mon_opts.index(d_mon))
        with c12:
            inp_cam = st.number_input("Số lần gọi (campaign):", min_value=1, max_value=50, value=d_cam, step=1)
            
        c13, c14, c15, c16 = st.columns(4)
        with c13:
            inp_pda = st.number_input("Số ngày từ lần trước (pdays):", min_value=-1, max_value=900, value=d_pda, step=1)
        with c14:
            inp_pre = st.number_input("Số lần liên hệ trước (previous):", min_value=0, max_value=100, value=d_pre, step=1)
        with c15:
            pout_opts = ['unknown', 'failure', 'other', 'success']
            inp_pout = st.selectbox("Kết quả trước (poutcome):", pout_opts, index=pout_opts.index(d_pout))
        with c16:
            inp_dur = st.number_input("Thời lượng (duration giây):", min_value=0, max_value=5000, value=d_dur, step=10)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tùy chọn kịch bản và ngưỡng quyết định
        st.markdown("**4. Thiết lập vận hành và Kịch bản dự báo:**")
        col_scen, col_thresh = st.columns(2)
        with col_scen:
            eval_mode = st.radio(
                label="Kịch bản vận hành:",
                options=[
                    "Trước cuộc gọi (Pre-call - Loại bỏ duration)",
                    "Sau cuộc gọi (Post-call - Có duration)"
                ],
                index=0,
                help="Kịch bản Pre-call không sử dụng biến thời lượng cuộc gọi để chống rò rỉ dữ liệu (Look-ahead bias) khi chấm điểm khách hàng trước khi bấm máy."
            )
        with col_thresh:
            threshold = st.slider(
                label="Ngưỡng phân loại (Decision Threshold):",
                min_value=0.20,
                max_value=0.80,
                value=0.50,
                step=0.05,
                help="Điều chỉnh ngưỡng quyết định: Ngưỡng thấp (0.3 - 0.4) ưu tiên bắt trọn khách hàng (Recall cao); Ngưỡng cao (0.6 - 0.7) ưu tiên độ chính xác cuộc gọi (Precision cao)."
            )
            
        predict_btn = st.button("Dự đoán quyết định gửi tiền")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_pred:
        st.markdown("""
        <div class="card-container">
            <div class="card-title">Kết quả chấm điểm và Phân tích chuyên sâu</div>
            <div class="card-subtitle">Xác suất tính toán thời gian thực kết hợp phân loại cụm K-Means và kịch bản hành động.</div>
        """, unsafe_allow_html=True)
        
        # Tiền xử lý dữ liệu đầu vào cho dự đoán
        input_dict = {
            'age': inp_age,
            'job': inp_job,
            'marital': inp_mar,
            'education': inp_edu,
            'default': inp_def,
            'balance': inp_bal,
            'housing': inp_hou,
            'loan': inp_loa,
            'contact': inp_con,
            'day': inp_day,
            'month': inp_mon,
            'duration': inp_dur if "Post-call" in eval_mode else 0,
            'campaign': inp_cam,
            'pdays': inp_pda,
            'previous': inp_pre,
            'poutcome': inp_pout
        }
        
        input_df = pd.DataFrame([input_dict])
        input_encoded = pd.get_dummies(input_df, drop_first=True, dtype=int)
        
        # Căn chỉnh đầy đủ các cột thuộc tính One-Hot
        for col in feature_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[feature_cols]
        
        # Chuẩn hóa dữ liệu
        input_scaled = pd.DataFrame(scaler.transform(input_encoded), columns=feature_cols)
        
        # Tính toán xác suất dự đoán
        prob = active_model.predict_proba(input_scaled)[0][1]
        
        # Phân cụm K-Means cho hồ sơ đầu vào
        km_input_scaled = scaler_km.transform([[inp_age, inp_bal]])
        user_cluster_id = int(kmeans_model.predict(km_input_scaled)[0])
        cluster_names = {
            0: "Cụm 0 (Đại chúng trẻ tích lũy cơ bản)",
            1: "Cụm 1 (Khách hàng lớn tuổi / Hưu trí)",
            2: "Cụm 2 (Khách hàng tích lũy cao - VIP)"
        }
        user_cluster_name = cluster_names.get(user_cluster_id, "Cụm 0")
        
        # Biểu đồ Gauge hiển thị xác suất
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            number={'suffix': "%", 'font': {'size': 32, 'family': 'Inter', 'color': '#0F172A'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                'bar': {'color': "#1E3A8A" if prob >= threshold else "#64748B"},
                'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 30], 'color': '#F1F5F9'},
                    {'range': [30, 60], 'color': '#E2E8F0'},
                    {'range': [60, 100], 'color': '#DBEAFE'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.8,
                    'value': threshold * 100
                }
            }
        ))
        fig_g.update_layout(height=200, margin=dict(t=10, b=10, l=20, r=20), paper_bgcolor='white')
        st.plotly_chart(fig_g, use_container_width=True)
        
        # Kết luận phân loại
        is_yes = prob >= threshold
        if is_yes:
            st.markdown(f"""
            <div style="background-color: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 6px; padding: 14px; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #065F46; font-size: 15px;">DỰ ĐOÁN: ĐỒNG Ý GỬI TIỀN (Xác suất: {prob*100:.1f}%)</div>
                <div style="color: #047857; font-size: 13px; margin-top: 4px;">Khách hàng vượt ngưỡng quyết định ({threshold*100:.0f}%). Thuộc diện <strong>tiềm năng cao</strong> cần ưu tiên tiếp cận ngay.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 14px; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #475569; font-size: 15px;">DỰ ĐOÁN: TỪ CHỐI GỬI TIỀN (Xác suất: {prob*100:.1f}%)</div>
                <div style="color: #64748B; font-size: 13px; margin-top: 4px;">Khách hàng dưới ngưỡng quyết định ({threshold*100:.0f}%). Tạm thời không đưa vào danh sách Cold Calling để tiết kiệm chi phí.</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Thông tin phân khúc K-Means
        st.markdown(f"""
        <div style="background-color: #F1F5F9; border-radius: 4px; padding: 10px 14px; margin-bottom: 16px; font-size: 13px;">
            <strong>Phân khúc K-Means tự động:</strong> {user_cluster_name}<br>
            <span style="color: #64748B; font-size: 12px;">Được gán trực tiếp bằng mô hình KMeans (K=3) đã huấn luyện dựa trên Tuổi ({inp_age}) và Số dư ({inp_bal:,} EUR).</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Khuyến nghị chiến lược nghiệp vụ (Actionable Playbook)
        st.markdown("**Kịch bản hành động chi tiết dành cho chuyên viên (Actionable Playbook):**")
        if user_cluster_id == 1 or inp_age >= 60:
            st.markdown("""
            • <strong>Sản phẩm đề xuất:</strong> Tiết kiệm dưỡng lão an nhàn, nhận lãi định kỳ hàng tháng vào tài khoản hưu trí.<br>
            • <strong>Kênh tư vấn tối ưu:</strong> Hẹn gặp trực tiếp tại quầy giao dịch chi nhánh hoặc gọi điện thoại bàn buổi sáng (9:00 - 10:30).<br>
            • <strong>Thông điệp then chốt:</strong> Nhấn mạnh độ an toàn vốn 100%, ngân hàng bảo hiểm tiền gửi Nhà nước, thủ tục nhận lãi đơn giản.
            """, unsafe_allow_html=True)
        elif user_cluster_id == 2 or inp_bal >= 3000:
            st.markdown("""
            • <strong>Sản phẩm đề xuất:</strong> Chứng chỉ tiền gửi có kỳ hạn 12 - 24 tháng với bậc thang lãi suất thưởng dành riêng cho khách hàng VIP.<br>
            • <strong>Kênh tư vấn tối ưu:</strong> Bàn giao cho Giám đốc Quan hệ Khách hàng Ưu tiên (Premier/Private RM) chăm sóc riêng.<br>
            • <strong>Thông điệp then chốt:</strong> Tối ưu hóa lợi suất dòng tiền nhàn rỗi lớn, đi kèm đặc quyền phòng chờ sân bay và thẻ tín dụng cao cấp.
            """, unsafe_allow_html=True)
        else:
            if inp_hou == 'yes' or inp_loa == 'yes':
                st.markdown("""
                • <strong>Sản phẩm đề xuất:</strong> Gói tích lũy linh hoạt số tiền nhỏ (từ 50 EUR/tháng) tự động trích từ lương qua App Mobile Banking.<br>
                • <strong>Lưu ý nghiệp vụ:</strong> Khách hàng đang chịu áp lực nợ vay; tuyệt đối không tư vấn các gói tiền gửi kỳ hạn dài với số vốn lớn để tránh gây căng thẳng dòng tiền.
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                • <strong>Sản phẩm đề xuất:</strong> Tiết kiệm mục tiêu ngắn hạn (3 - 6 tháng) mở trực tuyến với lãi suất ưu đãi cộng thêm 0,2%.<br>
                • <strong>Kênh tư vấn:</strong> Gửi thông báo Push Notification qua ứng dụng Mobile Banking hoặc tin nhắn Zalo ZNS trước khi gọi điện.
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
