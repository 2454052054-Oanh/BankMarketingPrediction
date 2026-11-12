# Bank Marketing Prediction

Dự án phân tích dữ liệu và xây dựng mô hình học máy dự đoán quyết định mở sổ tiền gửi tiết kiệm có kỳ hạn tại ngân hàng (Term Deposit Prediction) dựa trên bộ dữ liệu Bank Marketing Dataset (UCI Machine Learning Repository).

## 1. Giới thiệu đề tài
Trong hoạt động ngân hàng bán lẻ, việc tiếp cận khách hàng qua điện thoại (Telemarketing) đại trà gây tốn kém chi phí và tỷ lệ chuyển đổi thấp (~11.7%). Dự án này ứng dụng các kỹ thuật Phân tích Dữ liệu và Học máy (Machine Learning) để:
- Phân tích khám phá (EDA) các yếu tố nhân khẩu học, tài chính và bối cảnh tiếp thị ảnh hưởng đến quyết định gửi tiền.
- Phân khúc khách hàng bằng thuật toán phân cụm K-Means ($K=3$).
- Huấn luyện và đánh giá các mô hình phân loại: Logistic Regression, Random Forest, LightGBM và XGBoost (kết hợp xử lý mất cân bằng lớp và kiểm soát rủi ro Data Leakage).
- Minh bạch hóa quyết định của mô hình bằng phương pháp SHAP (Explainable AI).
- Triển khai ứng dụng Web Dashboard tương tác hỗ trợ chuyên viên ngân hàng chấm điểm và ra quyết định thời gian thực.

## 2. Cấu trúc thư mục
```text
BankMarketingPrediction/
├── app/
│   └── app.py                     # Giao diện ứng dụng Web (Streamlit)
├── dataset/
│   ├── Bank_Marketing_Dataset.csv # Dữ liệu gốc UCI (45.211 dòng, 17 cột)
│   ├── cleaned/
│   │   └── bank_cleaned.csv       # Dữ liệu sạch sau tiền xử lý IQR Capping
│   ├── model/                     # Các mô hình học máy đã huấn luyện (.pkl)
│   └── processed/                 # Ma trận đặc trưng One-Hot
├── figures/                       # Các biểu đồ phân tích và đánh giá mô hình
├── notebooks/                     # Quy trình 6 Jupyter Notebooks
│   ├── 01_Data_understanding.ipynb
│   ├── 02_DataCleaning.ipynb
│   ├── 03_EDA_Visualization.ipynb
│   ├── 04_DataPreparation_LeakageHandling.ipynb
│   ├── 05_ModelTraining_Tuning_Evaluation.ipynb
│   └── 06_SHAP_Explainability_Conclusion.ipynb
├── requirements.txt               # Danh sách thư viện phụ thuộc
└── README.md
```

## 3. Hướng dẫn cài đặt và khởi chạy

### Yêu cầu môi trường
- Python 3.9+
- Các thư viện liệt kê trong `requirements.txt`

### Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Khởi chạy ứng dụng Web
```bash
streamlit run app/app.py
```
Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ mặc định: `http://localhost:8501`.

## 4. Kết quả thực nghiệm

Kết quả đánh giá trên tập kiểm tra độc lập (9.043 mẫu kiểm tra - Holdout 20%):

| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 83.48% | 40.04% | 83.46% | 0.5413 | 0.9060 | 0.5471 |
| **Random Forest** | 85.12% | 43.23% | 86.20% | 0.5759 | 0.9239 | 0.6015 |
| **LightGBM** | 85.04% | 44.13% | 88.09% | 0.5880 | 0.9304 | 0.6202 |
| **XGBoost** | 85.36% | 43.68% | 87.33% | 0.5824 | **0.9309** | **0.6227** |

*Ghi chú: Mô hình được huấn luyện có điều chỉnh trọng số hàm mất mát (Cost-Sensitive Learning, `scale_pos_weight = 7.55`) để giải quyết vấn đề mất cân bằng dữ liệu tự nhiên (7.55 : 1).*
