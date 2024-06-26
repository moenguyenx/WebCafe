# WebCafe ☕

# 1. Khái quát hệ thống làm gì? Ai dùng? Vấn đề?
   - Với xu hướng tự kinh doanh cafe của nhiều cá nhân có ít vốn hiện nay nảy ra rất nhiều vấn đề như order chậm chạp hay bị nhầm đồ của khách do thiếu nhân lực dẫn đến 1 hay ít người phải tải rất nhiều đầu việc. Nhóm quyết định triển khai dự án Order Cafe thông minh.
   - Hệ thống sẽ được sử dụng trong các quán cafe nhỏ lẻ, khi khách vô ngồi bàn sẽ quét mã QR để truy cập trang web để có thể order đồ uống, sau khi ấn order thì nhân viên ở trong quầy phục vụ sẽ nhận được thông báo trên hệ thống là bàn nào gọi những món gì...giúp tiết kiệm thời gian và tránh nhầm lẫn.

# 2. Làm rõ chức năng, từng thông tin vào/ra hệ thống, từng hành vi hệ thống, từng nghiệp vụ người dùng
   - Chức năng:
     + Đối với khách hàng: có thể quét QR vào trang web để order tại bàn, xem tổng số tiền phải thanh toán (xem xét thêm chức năng thanh toán)
     + Đối với nhân viên: khi khách hàng order trên hệ thống sẽ hiển thị lên dashboard bàn nào gọi đồ gì...
     + Đối với chủ: theo dõi đơn hàng, doanh thu 

   - Từng thông tin vào/ra hệ thống
   - Từng hành vi hệ thống
   ![image](https://github.com/moenguyenx/WebCafe/assets/130982716/8ecf267d-0378-4192-a04c-cbed031a7b64)

# 3. Framework, Libs
   - Python Flask - Backend
   - Bootstrap - Frontend UI Library
   - JQuery - Embedded in html to call API for data
  
# 4. How to use?
   * Prerequisites:
     - Your MongoDB should have 'cafe' database and 5 collection name 'users, finance, menu, orders, drinks'
       ![image](https://github.com/moenguyenx/WebCafe/assets/130982716/ba072d0d-8428-4aa1-87b5-0ee22334c8fb)
     - Remember to add your own MongoDB URI in __init__.py.
     - The JSON Data for database is placed in "data" folder.

   - Fork this project
   - Create venv and install required libraries
     ```bash
     python -m venv venv
     .venv\Scripts\activate
     pip install -r requirement.txt
     ```
   - Run the server
      ```bash
      python run.py
      ```
  
