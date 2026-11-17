import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="green_corridor"
    )

def insert_record(plate_number, image_path):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO vehicle_records (plate_number, image_path)
    VALUES (%s, %s)
    """

    cursor.execute(query, (plate_number, image_path))

    conn.commit()
    cursor.close()
    conn.close()

def fetch_records():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vehicle_records ORDER BY detected_at DESC")
    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records
def clear_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vehicle_records")

    conn.commit()
    cursor.close()
    conn.close()