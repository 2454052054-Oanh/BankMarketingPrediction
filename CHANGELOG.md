# BẢN GHI THAY ĐỔI VÀ NÂNG CẤP HỆ THỐNG (CHANGELOG)
**Dự án:** Phân tích Dữ liệu Khách hàng và Dự đoán Quyết định Gửi tiền Tiết kiệm tại Ngân hàng
**Thời gian hoàn thành nâng cấp:** Tháng 11/2026

---

## 1. Nâng cấp Khoa học Dữ liệu & Xử lý rò rỉ dữ liệu (Data Leakage)
- **Kiểm soát rủi ro biến V12 (`duration`)**:
  - Phân tích rủi ro Look-ahead bias: Thời lượng cuộc gọi chưa biết trước khi bấm máy.
  - Thiết kế 2 kịch bản thực nghiệm độc lập:
    - *Kịch bản A (Realistic Pre-Call)*: Loại bỏ `duration` để chấm điểm danh sách khách hàng trước khi gọi điện (ROC-AUC đạt 0.8036, PR-AUC đạt 0.4725).
    - *Kịch bản B (Post-Call Benchmark)*: Giữ `duration` để đối sánh học thuật và đánh giá chất lượng cuộc gọi (ROC-AUC đạt 0.9309, PR-AUC đạt 0.6227).
- **Phòng chống Data Leakage trong tiền xử lý**:
  - Ngưỡng ngoại lai IQR Capping được tính toán độc lập trên tập Train, áp dụng sang tập Test.
  - Bộ chuẩn hóa `StandardScaler` chỉ khớp trên tập Train.
  - Phân chia phân tầng chuẩn (Stratified 80/20 Holdout) bảo toàn chính xác tỷ lệ nhãn 11.70% 'yes'.

## 2. Nâng cấp Bộ mô hình Machine Learning thế hệ mới & Phân cụm K-Means
- **Loại bỏ k-NN**: Do độ nhạy Recall thấp (31.0%) và suy giảm hiệu năng trong không gian 42 chiều do "Lời nguyền số chiều" (Curse of Dimensionality).
- **Triển khai 4 mô hình học máy hiện đại**:
  1. **Logistic Regression (Baseline)**: Cân bằng trọng số lớp (ROC-AUC: 0.9060, Recall: 83.46%).
  2. **Random Forest (Benchmark)**: 150 cây, kiểm soát quá khớp (ROC-AUC: 0.9239, Recall: 86.20%).
  3. **XGBoost (Extreme Gradient Boosting)**: Tối ưu với `scale_pos_weight = 7.55` (ROC-AUC: **0.9309**, PR-AUC: **0.6227**, CV-AUC: **0.9326**).
  4. **LightGBM (Leaf-wise Gradient Boosting)**: Tối ưu với `scale_pos_weight = 7.55` (F1-Score: **0.5880**, Recall: **88.09%**).
- **Huấn luyện và đóng gói mô hình phân cụm K-Means ($K=3$)**:
  - Sử dụng phương pháp Elbow xác định điểm gãy tối ưu tại $K=3$.
  - Đóng gói `kmeans_model.pkl` và `scaler_kmeans.pkl` phục vụ phân cụm khách hàng trực tiếp trên Web.
- **Kiểm định chéo 5-Fold Stratified Cross-Validation**: Đánh giá độ ổn định và kiểm tra khoảng cách Overfitting (`train_auc - test_auc` chỉ từ 0.02 đến 0.03).
- **Thử nghiệm Cost-Sensitive Learning vs SMOTE**: So sánh thực nghiệm chứng minh phương pháp gán trọng số hàm mất mát đạt hiệu quả vượt trội hơn so với SMOTE trên dữ liệu bảng.

## 3. Tích hợp XAI (Explainable AI) với SHAP
- Khởi tạo `shap.TreeExplainer` trên mô hình Boosting tối ưu.
- Xuất biểu đồ độ phân giải cao 300 DPI:
  - `figures/shap_summary_beeswarm.png`: Chiều hướng và mức độ tác động của từng đặc trưng (Hình 2 Báo cáo & Slide 12).
  - `figures/shap_importance_bar.png`: Xếp hạng tầm quan trọng toàn cục theo giá trị tuyệt đối SHAP (Slide 12).
- Lưu trữ `shap_explainer.pkl` và `shap_background.pkl` hỗ trợ diễn giải dự đoán cá thể trong ứng dụng Web.

## 4. Thiết kế lại Giao diện Streamlit chuẩn Enterprise BI & Đồng bộ 100% Sơ đồ, Đồ thị
- **Đồng bộ hóa toàn diện sơ đồ và đồ thị học thuật với Báo cáo và Slide**:
  - **Sơ đồ quy trình tiền xử lý 5 bước**: Tích hợp trực tiếp trên Web theo dạng thẻ pipeline hiện đại, khớp chính xác Slide 6 và Chương 3.1 Báo cáo.
  - **Hình 1 (Báo cáo) & Slide 7 (`kmeans_customer_clusters.png`)**: Hiển thị trọn vẹn cả đồ thị Elbow xác định K tối ưu (K=3) và biểu đồ phân cụm khách hàng K-Means với trọng tâm Centroids chữ X đỏ.
  - **Bảng 1 (Báo cáo) & Slide 9 (`model_comparison_metrics.png`)**: Bảng so sánh 4 mô hình (7 chỉ số) và biểu đồ cột 5 chỉ số hiệu năng trực quan.
  - **Slide 10 (`roc_curves_advanced.png`, `pr_curves_advanced.png`, `confusion_matrices_advanced.png`)**: Tích hợp bộ ba đồ thị đánh giá phân loại đa chiều chất lượng cao.
  - **Slide 11 (`pre_vs_post_call_leakage.png`)**: Biểu đồ đối chứng trực quan rò rỉ dữ liệu Pre-call vs Post-call.
  - **Hình 2 (Báo cáo) & Slide 12 (`shap_summary_beeswarm.png`, `shap_importance_bar.png`)**: Tích hợp biểu đồ SHAP Beeswarm và Feature Importance giải thích tính minh bạch của mô hình.
- **Tổ chức 4 phân hệ chức năng chuyên nghiệp**:
  1. *Tổng quan dữ liệu & Khám phá EDA*: 4 KPI động, sơ đồ pipeline 5 bước chuẩn hóa, biểu đồ chuyển đổi nhân khẩu học, ma trận tương quan Pearson, tác động tài chính nợ vay và bảng duyệt 10 bản ghi dữ liệu thực.
  2. *Phân tích hành vi & Phân cụm K-Means*: Đồ thị phương pháp Elbow xác định K tối ưu (K=3), biểu đồ phân cụm kèm Centroids, bảng thống kê đặc trưng 3 cụm, phân tích độ tuổi chữ U và rào cản nợ vay.
  3. *Đánh giá mô hình & Diễn giải SHAP*: Bảng tổng hợp hiệu năng 4 mô hình, biểu đồ 5 chỉ số, bộ ba ROC/PR/CM, đối chứng rò rỉ dữ liệu Look-ahead bias và giải thích SHAP Beeswarm minh bạch hóa cơ chế dự báo.
  4. *Chấm điểm & Dự đoán gửi tiết kiệm*: Bộ công cụ hỗ trợ ra quyết định thời gian thực với form 16 thuộc tính, kịch bản Pre-call/Post-call, thanh trượt Decision Threshold (0.20 - 0.80), đồng hồ Gauge đo xác suất, phân loại cụm K-Means và Actionable Playbook chi tiết cho chuyên viên ngân hàng.

## 5. Chuẩn hóa Toàn bộ Tài liệu Dự án
- **Hệ thống 6 Jupyter Notebooks**: Đầy đủ từ tiền xử lý, phân cụm đến mô hình hóa và SHAP.
- **Báo cáo Word (`BÁO CÁO BTL.docx`)**: Đúng 5 trang A4 chuẩn mực, tích hợp Hình 1 (K-Means Elbow), Hình 2 (SHAP Beeswarm), Bảng 1, 0 emoji, trích dẫn chuẩn APA.
- **Slide thuyết trình (`Hệ thống dự đoán khách hàng gửi tiết kiệm.pptx`)**: 14 slide Widescreen chuẩn mực tích hợp đầy đủ sơ đồ và biểu đồ độ nét cao.
- **Kịch bản thuyết trình (`KICH_BAN_THUYET_TRINH_CHI_TIET.docx`)**: Lời nói word-for-word 14 slide và hướng dẫn demo web 4 bước ăn khớp tuyệt đối với giao diện.
- **Cẩm nang kiến thức (`CAM_NANG_KIEN_THUC_TOAN_DIEN_A_Z.docx`)**: Giải thích bản chất từ con số 0, cấu trúc giao diện Web và bộ câu hỏi vấn đáp điểm 10.
- **Khởi chạy tự động (`CHAY_WEB.bat`)**: Nhấp đúp 1 chạm khởi động ứng dụng Web từ bất kỳ thư mục nào.
