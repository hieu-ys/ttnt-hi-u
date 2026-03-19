1. Chuẩn bị môi trường

Trước tiên, cần cài đặt Python để có thể chạy chương trình. Truy cập trang chủ Python tại https://www.python.org
 để tải và cài đặt. Trong quá trình cài đặt, cần tích chọn mục “Add Python to PATH” để có thể sử dụng Python trong Command Prompt.

Ngoài ra, nên cài đặt Visual Studio Code (VS Code) để thuận tiện cho việc viết và chạy chương trình. Có thể tải tại https://code.visualstudio.com
 và cài thêm tiện ích mở rộng Python.

2. Cài đặt các thư viện cần thiết

Sau khi cài đặt Python, mở Command Prompt hoặc Terminal tại thư mục chứa file chương trình và tiến hành cài đặt các thư viện cần thiết bằng lệnh:

pip install flask flask-bcrypt flask-cors pillow mysql-connector-python requests

Các thư viện này phục vụ cho việc xây dựng server, mã hóa mật khẩu, xử lý ảnh, kết nối cơ sở dữ liệu và gửi yêu cầu HTTP.

3. Cài đặt và cấu hình cơ sở dữ liệu MySQL

Tiếp theo, cần cài đặt MySQL để lưu trữ dữ liệu. Truy cập https://dev.mysql.com/downloads/
 để tải và cài đặt.

Sau khi cài đặt xong, mở MySQL và tạo một cơ sở dữ liệu mới bằng câu lệnh:

CREATE DATABASE your_database_name;

Sau đó, mở file chương trình Python (ví dụ: app.py) và tìm đến phần cấu hình kết nối MySQL. Thay đổi các thông tin như tên database, tên người dùng và mật khẩu cho phù hợp với máy của bạn. Ví dụ:

host = "localhost"
user = "root"
password = "mật_khẩu_mysql"
database = "your_database_name"
4. Tổ chức thư mục chương trình

Do chương trình sử dụng Flask với thư mục tĩnh là thư mục hiện tại, các file giao diện như HTML, CSS, JavaScript cần được đặt cùng thư mục với file app.py. Ví dụ cấu trúc thư mục:

project/
│── app.py
│── index.html
│── login.html
│── script.js
5. Chạy chương trình

Sau khi hoàn tất các bước trên, mở Terminal tại thư mục chứa file app.py và chạy lệnh:

python app.py

Nếu chương trình chạy thành công, màn hình sẽ hiển thị địa chỉ:

http://127.0.0.1:5000
6. Truy cập ứng dụng

Mở trình duyệt web và truy cập địa chỉ:

http://localhost:5000

để sử dụng hệ thống.

7. Một số lỗi thường gặp và cách khắc phục

Nếu xuất hiện lỗi “ModuleNotFoundError”, nguyên nhân là chưa cài thư viện. Cần chạy lại lệnh pip install tương ứng.

Nếu không kết nối được MySQL, cần kiểm tra lại tên database, tài khoản, mật khẩu hoặc đảm bảo MySQL đang chạy.

Nếu xuất hiện lỗi “Address already in use”, có thể do cổng 5000 đang được sử dụng. Khi đó có thể đổi sang cổng khác trong code.

Nếu gặp lỗi liên quan đến xử lý ảnh, cần đảm bảo đã cài đặt thư viện Pillow.


Quy trình cài đặt và chạy chương trình bao gồm các bước chính: cài đặt môi trường (Python, VS Code), cài thư viện, cấu hình cơ sở dữ liệu, tổ chức file và chạy server. Khi thực hiện đúng các bước trên, chương trình sẽ hoạt động ổn định trên máy tính cá nhân.
