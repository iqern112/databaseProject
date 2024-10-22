from flask import Flask, render_template
import pyodbc
import pandas as pd

# ตั้งค่าการเชื่อมต่อแบบ Windows Authentication
server = 'ASUS\\SQLEXPRESS'
database = 'FIFAPlayer'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# ฟังก์ชันเพื่อคิวรี่ข้อมูลจากฐานข้อมูล
def query_database():
    try:
        # เชื่อมต่อกับ SQL Server โดยใช้ Windows Authentication
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            
            # คิวรี่ข้อมูลจากตาราง FIFA22
            query = 'SELECT TOP 10 * FROM [dbo].[FIFA22]'
            cursor.execute(query)
            
            # ดึงข้อมูลทั้งหมดจากคิวรี่
            rows = cursor.fetchall()
            
            # นำข้อมูลคิวรี่มาใส่ใน DataFrame
            columns = [column[0] for column in cursor.description]  # ดึงชื่อคอลัมน์
            df = pd.DataFrame.from_records(rows, columns=columns)
            return df
    
    except Exception as err:
        print('เกิดข้อผิดพลาด:', err)
        return None

# สร้าง Flask แอปพลิเคชัน
app = Flask(__name__)

# Route สำหรับแสดงข้อมูลที่คิวรี่มา
@app.route('/')
def index():
    data = query_database()  # คิวรี่ข้อมูล
    if data is not None:
        # ส่งข้อมูลไปแสดงใน template
        return render_template('index.html', tables=[data.to_html(classes='data', header="true")])
    else:
        return "เกิดข้อผิดพลาดในการคิวรี่ข้อมูล"

# เริ่ม Flask เซิร์ฟเวอร์
if __name__ == '__main__':
    app.run(debug=True)
