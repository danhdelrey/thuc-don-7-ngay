# Thực đơn 7 ngày

App Android nhỏ (WebView, chạy offline) để xem thực đơn nấu ăn 7 ngày cho 1 người và tick checklist món ăn, đi chợ.

**Tải bản mới nhất:** [thuc-don-7-ngay.apk](../../releases/latest/download/thuc-don-7-ngay.apk)

- Nội dung app nằm trong `app/assets/index.html`. Sửa file này rồi push lên `main` là GitHub Actions tự build và tạo Release mới.
- Build không dùng Gradle: `build.sh` gọi trực tiếp aapt2, javac, d8, apksigner có sẵn trên runner.
- Khóa ký app lưu trong GitHub Secrets (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`), nên các bản cập nhật cài đè lên nhau được.
