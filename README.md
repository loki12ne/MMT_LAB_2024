# MMT_LAB_2024
Mạng Máy Tính - LAB - SOCKET - Quản lý tải dữ liệu từ sever đến client

#THIS IS VIETNAMESE VERSION, PLEASE USE GOOGLE TRANSLATER FOR ENGLISH


######################################################################

LƯU Ý:

######################################################################
1. Tạo folder download_file, gắn path vào biến toàn cục download_path trong cả 4 file .py
2. Thay đổi IP và PORT cho phù hợp
3. Tạo file data.txt ở server chứa tên các file + kích thước file hiện có ở server
4. Tạo file input.txt ở client chứa các file yêu cầu
5. Khi chạy, nên sử dụng cmd, hoặc full screen (nếu dùng terminal)
6. Khi chạy, có thể thêm vào input.txt file mới, NHƯNG không được xoá tên file trước đó



######################################################################

NỘI DUNG:

######################################################################
1. Phần 1: 1 server -> 1 client -> 1 file/1 lần gửi
2. Phần 2: 1 server -> nhiều client -> nhiều file/1 lần gửi với mức độ ưu tiên khác nhau



######################################################################

SAMPLE FILE: data.txt

######################################################################

file 1.txt 54MB

file2.zip 34MB

file3.png 1GB



######################################################################

SAMPLE FILE: input.txt (PHẦN 1)

######################################################################

file2.txt

file9.png



######################################################################

SAMPLE FILE: input.txt (PHẦN 2) (3 độ ưu tiên: CRITICAL, HIGH, NORMAL)

CRITICAL = 10 NORMAL

HIGH = 4 NORMAL

######################################################################

file2.txt CRITICAL

file9.png HIGH



