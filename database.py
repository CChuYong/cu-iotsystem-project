import pymysql

device_key = "u093xakdf93284"

create_query = """CREATE TABLE IF NOT EXISTS iot_state(
    device_key VARCHAR(16) PRIMARY KEY,
    desired_temp INT NOT NULL
)"""

select_query = """SELECT * FROM iot_state WHERE device_key = """ + device_key

def initialize():
    try:
        global connection
        connection = pymysql.connect()
    except pymysql as e:
        print("Database Error")
    print("Database Connected")

    # 데이터베이스 테이블 기본 생성 (있음말고~)
    cursor = connection.cursor()
    cursor.execute(create_query)
    connection.commit()
    cursor.close()

def read_desired_temp():
    try:
        cursor = connection.cursor()
        cursor.execute(select_query)
        for row in cursor:
            return row["desired_temp"]
        return 0.0
    finally:
        cursor.close()

def shutdown():
    connection.close()