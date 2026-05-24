import csv
import random
from datetime import datetime, timedelta

def generate_precise_time_csv(file_name, n, start_str, end_str, start_h_limit, end_h_limit):
    # Định dạng nhập vào: Tháng/Ngày/Năm Giờ:Phút
    input_format = "%m/%d/%Y %H:%M"
    time_list = []
    
    try:
        # Giờ bắt đầu chính xác (ví dụ 18:00 ngày 20)
        start_dt = datetime.strptime(start_str, input_format)
        # Giờ kết thúc chính xác (nên để 23:59 ngày 26 để bao phủ hết ngày)
        end_dt = datetime.strptime(end_str, input_format)
    except ValueError:
        print("Lỗi: Định dạng nhập vào phải là Month/Day/Year Hour:Minute (VD: 03/20/2026 18:00)")
        return

    delta_seconds = int((end_dt - start_dt).total_seconds())
    
    if delta_seconds <= 0:
        print("Lỗi: Thời điểm bắt đầu phải trước thời điểm kết thúc.")
        return

    count = 0
    # Tăng số lần thử để đảm bảo tìm đủ N hàng trong khung giờ hẹp
    max_attempts = n * 20 
    attempts = 0

    while count < n and attempts < max_attempts:
        attempts += 1
        # 1. Random giây trong khoảng tổng
        random_sec = random.randint(0, delta_seconds)
        random_dt = start_dt + timedelta(seconds=random_sec)
        
        # 2. Kiểm tra khung giờ quy định (ví dụ 7h - 22h)
        if start_h_limit <= random_dt.hour <= end_h_limit:
            # Đảm bảo phút và giây cũng ngẫu nhiên
            random_dt = random_dt.replace(minute=random.randint(0, 59), second=random.randint(0, 59))
            
            # Kiểm tra lại lần nữa sau khi replace phút/giây để chắc chắn không vượt quá end_dt
            if start_dt <= random_dt <= end_dt:
                time_list.append(random_dt)
                count += 1

    # 3. Sắp xếp tăng dần
    time_list.sort()

    # 4. Ghi file
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for dt in time_list:
            formatted_time = dt.strftime("%m/%d/%Y %H:%M")
            writer.writerow([formatted_time])

    if count < n:
        print(f"Lưu ý: Chỉ tạo được {count}/{n} hàng do khung giờ giới hạn quá hẹp.")
    else:
        print(f"Thành công! Đã tạo {n} hàng vào file '{file_name}'.")

# --- CẤU HÌNH ---
N_ROWS = 30
# Ngày 20 bắt đầu từ 18:00
START_POINT = "05/24/2026 21:20" 
# Ngày 26 kết thúc lúc 23:59 để lấy được các giờ tối ngày 26
END_POINT = "05/25/2026 21:59"    

# Giới hạn khung giờ hoạt động mỗi ngày
LIMIT_START_H = 7
LIMIT_END_H = 23 

generate_precise_time_csv("time.csv", N_ROWS, START_POINT, END_POINT, LIMIT_START_H, LIMIT_END_H)