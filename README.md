# Phân tích dữ liệu khách hàng và dự đoán quyết định gửi tiền tiết kiệm tại ngân hàng

Hệ thống phân tích dữ liệu thực nghiệm và hỗ trợ ra quyết định tiếp thị tiền gửi có kỳ hạn tại ngân hàng thương mại ứng dụng học máy nâng cao (Logistic Regression, Random Forest, XGBoost, LightGBM), phân cụm khách hàng K-Means và phương pháp diễn giải SHAP (Explainable AI).

---

## 1. Cấu trúc thư mục dự án
```text
BankMarketingPrediction-main/
├── app/
│   └── app.py                     # Ứng dụng Web Enterprise BI Dashboard (Streamlit)
├── dataset/
│   ├── Bank_Marketing_Dataset.csv # Dữ liệu gốc UCI (45.211 dòng, 17 cột)
│   ├── cleaned/
│   │   └── bank_cleaned.csv       # Dữ liệu đã làm sạch ngoại lệ IQR Capping
│   ├── model/
│   │   ├── best_model.pkl         # Mô hình tối ưu (XGBoost, ROC-AUC: 0.9309)
│   │   ├── xgboost_model.pkl      # Mô hình Extreme Gradient Boosting
│   │   ├── lightgbm_model.pkl     # Mô hình LightGBM
│   │   ├── rf_model.pkl           # Mô hình Random Forest Classifier
│   │   ├── lr_model.pkl           # Mô hình Logistic Regression (Baseline)
│   │   ├── kmeans_model.pkl       # Mô hình phân cụm K-Means (K=3)
│   │   ├── scaler_kmeans.pkl      # Scaler cho phân cụm K-Means
│   │   ├── scaler.pkl             # StandardScaler fit trên tập Train
│   │   ├── scaler_pre_call.pkl    # Scaler cho kịch bản trước cuộc gọi
│   │   ├── shap_explainer.pkl     # SHAP TreeExplainer
│   │   └── shap_background.pkl    # Dữ liệu nền phục vụ diễn giải SHAP
│   └── processed/
│       ├── feature_columns.json   # 42 thuộc tính One-Hot (kịch bản Benchmark)
│       ├── feature_columns_pre_call.json # 41 thuộc tính One-Hot (loại bỏ duration)
│       ├── X_train_scaled.pkl
│       ├── X_test_scaled.pkl
│       ├── y_train.pkl
│       └── y_test.pkl
├── figures/                       # Toàn bộ 11 biểu đồ phân tích và diễn giải 300 DPI
├── notebooks/                     # Hệ thống 6 Jupyter Notebooks từ tiền xử lý đến SHAP
│   ├── 01_Data_understanding.ipynb
│   ├── 02_DataCleaning.ipynb
│   ├── 03_EDA_Visualization.ipynb
│   ├── 04_DataPreparation_LeakageHandling.ipynb
│   ├── 05_ModelTraining_Tuning_Evaluation.ipynb
│   └── 06_SHAP_Explainability_Conclusion.ipynb
├── requirements.txt               # Thư viện phụ thuộc chuẩn
├── CHANGELOG.md                   # Bản ghi chi tiết các hạng mục nâng cấp
└── README.md
```

---

## 2. Các điểm nâng cấp then chốt & Cấu trúc Web Dashboard
1. **Kiểm soát rủi ro Data Leakage (biến V12 - duration)**: Thiết lập rõ ràng 2 kịch bản: Chấm điểm thực tế trước cuộc gọi (Pre-call Lead Scoring, loại bỏ duration) và Chuẩn đối sánh sau cuộc gọi (Post-call Benchmark).
2. **Bộ mô hình thế hệ mới**: Thay thế k-NN bằng **XGBoost** (ROC-AUC: 0.9309, PR-AUC: 0.6227) và **LightGBM** (F1: 0.5880, Recall: 88.09%).
3. **Phân cụm K-Means thực nghiệm (K=3)**: Khảo sát điểm uốn Elbow, trực quan hóa không gian phân khúc khách hàng 2D/3D và tích hợp phân loại cụm thời gian thực.
4. **Minh bạch hóa với SHAP**: Khảo sát chiều hướng tác động và xếp hạng tầm quan trọng của các đặc trưng bằng lý thuyết trò chơi Shapley.
5. **Giao diện Enterprise BI Dashboard chuẩn mực**:
   - **Thanh điều hướng Sidebar**: Dark Navy (`#0F172A`), bộ chuyển đổi 4 thuật toán và hộp thông tin tổng hợp dataset gốc (45.211 mẫu, 17 thuộc tính).
   - **Phân hệ 1 - Phân tích dữ liệu khách hàng (Khám phá EDA)**: 4 KPI động trực tiếp từ dữ liệu gốc, bảng duyệt dữ liệu thực tế và phân tích cơ cấu ngành nghề, học vấn.
   - **Phân hệ 2 - Phân tích hành vi và phân cụm K-Means**: Quy luật tuổi tác hình chữ U, tác động của rào cản nợ vay, trực quan hóa không gian phân cụm K-Means ($K=3$).
   - **Phân hệ 3 - Đánh giá mô hình học máy (XGBoost & Benchmark)**: Bảng định lượng 4 thuật toán với 7 chỉ số, biểu đồ Benchmark cột đa chiều, ma trận nhầm lẫn tương tác và đối chứng định lượng rò rỉ dữ liệu Pre-call vs Post-call.
   - **Phân hệ 4 - Dự đoán quyết định gửi tiền tiết kiệm**: Form 16 thuộc tính, kịch bản Pre-call chống Look-ahead bias, thanh trượt Decision Threshold (0.20 - 0.80), Gauge đo xác suất, phân cụm K-Means và Actionable Playbook.

---

## 3. Hướng dẫn khởi chạy ứng dụng Web
### Cách 1: Khởi chạy bằng 1 click chuột
Nhấp đúp vào tệp `CHAY_WEB.bat` tại thư mục bài làm.

### Cách 2: Khởi chạy qua Terminal
```bash
pip install -r requirements.txt
streamlit run app/app.py
```
Ứng dụng sẽ tự động mở tại: `http://localhost:8501`.
