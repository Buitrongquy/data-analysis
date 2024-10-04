import os
import pymysql
from dotenv import load_dotenv

# Load các biến môi trường từ file .env
load_dotenv()

def getConnection():
    try:
        # Kết nối đến cơ sở dữ liệu sử dụng thông tin từ biến môi trường
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            charset=os.getenv('DB_CHARSET', 'utf8mb4')
        )
        print("Kết nối thành công đến cơ sở dữ liệu!")
        return connection
    except pymysql.MySQLError as e:
        print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        return None
