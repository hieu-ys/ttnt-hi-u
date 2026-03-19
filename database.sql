CREATE DATABASE FlowerDB;
GO USE FlowerDB;
GO -- 1. Bảng NguoiDung (Bảng Tài khoản)
    CREATE TABLE NguoiDung (
        id INT IDENTITY(1, 1) PRIMARY KEY,
        tendangnhap VARCHAR(50) UNIQUE NOT NULL,
        matkhau VARCHAR(255) NOT NULL,
        hoten NVARCHAR(100) NOT NULL,
        ngaytao DATETIME DEFAULT GETDATE()
    );
GO -- 2. Bảng Hoa (Bảng Thông tin hoa)
    CREATE TABLE Hoa (
        id INT IDENTITY(1, 1) PRIMARY KEY,
        tenhoa NVARCHAR(100) NOT NULL,
        ho NVARCHAR(100),
        mota NVARCHAR(MAX),
        chamsoc NVARCHAR(MAX),
        hinh_url NVARCHAR(500)
    );
GO -- 3. Bảng YeuThich (Bảng Các loại hoa được yêu thích)
    CREATE TABLE YeuThich (
        id_nguoidung INT,
        id_hoa INT,
        PRIMARY KEY (id_nguoidung, id_hoa),
        FOREIGN KEY (id_nguoidung) REFERENCES NguoiDung(id) ON DELETE CASCADE,
        FOREIGN KEY (id_hoa) REFERENCES Hoa(id) ON DELETE CASCADE
    );
GO -- 4. Bảng LichSuNhanDien (Bảng Lịch sử nhận diện)
    CREATE TABLE LichSuNhanDien (
        id INT IDENTITY(1, 1) PRIMARY KEY,
        id_nguoidung INT,
        hinh_base64 VARCHAR(MAX),
        ketqua_json NVARCHAR(MAX),
        thoigian DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (id_nguoidung) REFERENCES NguoiDung(id) ON DELETE CASCADE
    );
GO -- CHÈN DỮ LIỆU MẪU (Đã khắc phục lỗi Insert bằng chữ N để hỗ trợ Tiếng Việt có dấu Unicode)
INSERT INTO Hoa (tenhoa, ho, mota, chamsoc, hinh_url)
VALUES (
        N'Hoa Hồng',
        N'Rosaceae',
        N'Loài hoa có nhiều cánh xếp lớp, thường có gai ở thân, mang ý nghĩa tượng trưng cho tình yêu và sắc đẹp.',
        N'Tưới nước 1-2 lần/ngày. Trồng nơi có nhiều ánh nắng. Bón phân định kỳ 1 tháng/lần.',
        N 'https://th.bing.com/th/id/OIP.fF91vGmPOwXhON7fbiVgowHaFj?w=244&h=183&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
    ),
    (
        N'Hoa Hướng Dương',
        N'Asteraceae',
        N'Hoa có bông lớn, cánh màu vàng rực rỡ, hoa mang đặc tính hướng quang, luôn nhắm về phía mặt trời mọc.',
        N'Cần rất nhiều ánh sáng mặt trời tự nhiên. Tưới nước đều đặn nhưng không làm úng rễ.',
        N'https://www.bing.com/th/id/OIP.jDrDbYuliLcnYc3lugwbZwHaFX?w=238&h=211&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2'
    ),
    (
        N'Hoa Tulip',
        N'Liliaceae',
        N'Hoa có hình chuông hoặc ngôi sao 6 cánh chụm, nhiều màu sắc đa dạng, là biểu tượng quốc hoa của đất nước Hà Lan.',
        N'Trồng ở nơi khí hậu ôn đới, mát mẻ. Đất cần có độ tơi xốp, thoát nước tốt. Tưới nước vừa phải.',
        N'https://www.bing.com/th/id/OIP.5sgEuXgIbZh1pn4rp_hRZwHaFj?w=240&h=211&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2'
    ),
    (
        N'Hoa Cúc',
        N'Asteraceae',
        N'Hoa mọc thành cụm, cánh mỏng nhỏ và nhiều, có sức sống mãnh liệt, biểu tượng của sự trường thọ.',
        N'Dễ trồng, ưa ánh sáng dịu nhẹ. Tưới nước hàng ngày. Tránh để ngập úng gốc rễ sâu.',
        N'https://www.bing.com/th/id/OIP.rpf8TZsG-Rm1DYC1CWPotAHaFj?w=224&h=211&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2'
    ),
    (
        N'Hoa Phong Lan',
        N'Orchidaceae',
        N'Loài thực vật thân đốt mang vẻ đẹp thanh tao, sang trọng, thường mọc bám (biểu sinh) trên thân cây khác gỗ hoặc trồng trong chậu than.',
        N 'Chăm sóc đòi hỏi kỹ thuật cao. Nên tưới nước dạng phun sương. Tuyệt đối tránh ánh nắng gắt trực tiếp làm cháy lá.',
        N'https://th.bing.com/th/id/OIP.wXKGoB0cpD48GdGwddRfoQHaFj?w=213&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
    );
GO
