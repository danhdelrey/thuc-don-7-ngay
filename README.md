# Thực đơn 7 ngày

App Android nhỏ (WebView, chạy offline): 7 thực đơn nấu nhanh cho 1 người, chọn tự do thứ tự ăn, nhắc rã đông cho ngày mai, checklist món ăn và đi chợ.

**Tải bản mới nhất:** [thuc-don-7-ngay.apk](../../releases/latest/download/thuc-don-7-ngay.apk)

- Nội dung app nằm trong `app/assets/index.html`. Sửa file này rồi push lên `main` là GitHub Actions tự build và tạo Release mới.
- Build không dùng Gradle: `build.sh` gọi trực tiếp aapt2, javac, d8, apksigner có sẵn trên runner.
- Khóa ký app lưu trong GitHub Secrets (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`), nên các bản cập nhật cài đè lên nhau được.
