import sqlite3
import os


def create_database():
    # 1. Kodun (main.py) olduğu klasörün yolunu al
    # Bu durumda 'current_dir' senin pythonSQL klasörün olacak
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Dosya yolunu 'pythonSQL/students.db' şeklinde birleştir
    db_path = os.path.join(current_dir, "students.db")

    # Temizlik: Eğer ana klasörde (DSandML) yanlışlıkla oluşan bir dosya varsa manuel silmelisin,
    # Ama bu kod artık sadece pythonSQL içine odaklanır.
    if os.path.exists(db_path):
        os.remove(db_path)

    # 3. Bağlantıyı tam yol (db_path) üzerinden kur
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE,
        city TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE Courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        instructor_name TEXT,
        credits INTEGER
    );
    """)


def insert_sample_data(cursor):
    students = [
        (1, 'Alice Johnson', 20, 'alice@gmail.com', "New York"),
        (2, 'Bob Smith', 19, 'bob@gmail.com', "Chicago"),
        (3, 'Carol White', 21, 'carol@gmail.com', "Boston"),
        (4, 'David Brown', 20, 'david@gmail.com', "New York"),
        (5, 'Emma Davis', 22, 'emma@gmail.com', "Seattle")
    ]

    cursor.executemany("INSERT INTO Students VALUES (?,?,?,?,?)", students)

    courses = [
        (1, 'Python Programming', 'Dr. Anderson', 3),
        (2, 'Web Development', 'Prof. Wilson', 4),
        (3, 'Data Science', 'Dr. Taylor', 3),
        (4, 'Mobile Apps', 'Prof. Garcia', 2)
    ]

    cursor.executemany("INSERT INTO Courses VALUES (?,?,?,?)", courses)

    print("Sample data inserted successfully")


def basic_sql_operations(cursor):
    # SELECT ALL
    print("-----------SELECT ALL-----------")
    cursor.execute("SELECT * FROM Students")
    records = cursor.fetchall()
    for record in records:
        print(record[0], record[1], record[2], record[3], record[4])

    # SELECT COLUMNS
    print("-----------SELECT COLUMNS-----------")
    cursor.execute("SELECT name, age FROM Students")
    records = cursor.fetchall()
    print(records)

    # WHERE CLAUSE
    print("-----------WHERE Age = 20-----------")
    cursor.execute("SELECT * FROM Students WHERE age = 20")
    records = cursor.fetchall()
    print(records)

    # ORDER BY
    print("-----------ORDER BY Age-----------")
    cursor.execute("SELECT * FROM Students ORDER BY Age")
    records = cursor.fetchall()
    print(records)

    # LIMIT
    print("----------Limit by 3 ----------")
    cursor.execute("SELECT * FROM Students LIMIT 3")
    records = cursor.fetchall()
    for row in records:
        print(row)


def sql_update_delete_insert_operations(conn, cursor):
    # 1) Insert
    cursor.execute("INSERT INTO Students VALUES (6, 'Frank Miller', 23, 'frank@gmail.com','Miami')")
    conn.commit()

    # 2) UPDATE
    cursor.execute("UPDATE Students SET age = 24 WHERE id = 6")
    conn.commit()

    # 3) DELETE
    cursor.execute("DELETE FROM Students WHERE id = 6")
    conn.commit()


def aggregate_functions(cursor):
    # 1) Count
    print("----------Aggregate Functions Count----------")
    cursor.execute("SELECT COUNT(*) FROM Students")
    result = cursor.fetchone()
    print(result[0])

    # 2) Average
    print("----------Aggregate Functions Average----------")
    cursor.execute("SELECT AVG(age) FROM Students")
    result = cursor.fetchone()
    print(result[0])

    # 3) MAX - MIN
    print("----------Aggregate Functions Max-Min----------")
    cursor.execute("SELECT MAX(age), MIN(age) FROM Students")
    result = cursor.fetchone()
    max_age, min_age = result
    print(max_age)
    print(min_age)

    # 4) GROUP BY
    print("----------Aggregate Functions Group by----------")
    cursor.execute("SELECT city, COUNT(*) FROM Students GROUP BY city")
    result = cursor.fetchall()
    print(result)


'''
    Basit
    1) Bütün kursların bilgilerini getirin
    2) Sadece eğitmenlerin ismini ve ders ismi bilgilerini getirin
    3) Sadece 21 yaşındaki öğrencileri getirin
    4) Sadece Chicago'da yaşayan öğrencileri getirin
    5) Sadece 'Dr. Anderson' tarafından verilen dersleri getirin
    6) Sadece ismi 'A' ile başlayan öğrencileri getirin
    7) Sadece 3 ve üzeri kredi olan dersleri getirin

    Detaylı
    1) Öğrencileri alphabetic şekilde dizerek getirin
    2) 20 yaşından büyük öğrencileri, ismine göre sıralayarak getirin
    3) Sadece 'New York' veya 'Chicago' da yaşayan öğrencileri getirin
    4) Sadece 'New York' ta yaşamayan öğrencileri getirin
'''

def answers(cursor):
    print("############################################")
    print("1) Bütün kursların bilgilerini getirin")
    cursor.execute("SELECT * FROM Courses")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("2) Sadece eğitmenlerin ismini ve ders ismi bilgilerini getirin")
    cursor.execute("SELECT instructor_name, course_name FROM Courses")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("3) Sadece 21 yaşındaki öğrencileri getirin")
    cursor.execute("SELECT * FROM Students WHERE age = 21")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("4) Sadece Chicago'da yaşayan öğrencileri getirin")
    cursor.execute("SELECT * FROM Students WHERE city = 'Chicago'")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("5) Sadece 'Dr. Anderson' tarafından verilen dersleri getirin")
    cursor.execute("SELECT * FROM Courses WHERE instructor_name = 'Dr. Anderson'")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("6) Sadece ismi 'A' ile başlayan öğrencileri getirin")
    cursor.execute("SELECT * FROM Students WHERE name LIKE 'A%'")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("7) Sadece 3 ve üzeri kredi olan dersleri getirin")
    cursor.execute("SELECT * FROM Courses WHERE credits >= 3")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("1) Öğrencileri alphabetic şekilde dizerek getirin")
    cursor.execute("SELECT * FROM Students ORDER BY name ASC")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("2) 20 yaşından büyük öğrencileri, ismine göre sıralayın")
    cursor.execute("SELECT * FROM Students WHERE age > 20 ORDER BY name ASC")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("3) Sadece 'New York' veya 'Chicago' da yaşayan öğrencileri getirin")
    cursor.execute("SELECT * FROM Students WHERE city = 'New York' OR city = 'Chicago'")
    result = cursor.fetchall()
    print(result)

    print("############################################")
    print("4) Sadece 'New York' ta yaşamayan öğrencileri getirin")
    cursor.execute("SELECT * FROM Students WHERE city != 'New York'")
    result = cursor.fetchall()
    print(result)





def main():
    conn, cursor = create_database()

    try:
        create_tables(cursor)
        insert_sample_data(cursor)
        basic_sql_operations(cursor)
        sql_update_delete_insert_operations(conn, cursor)
        aggregate_functions(cursor)
        answers(cursor)
        conn.commit()

    except sqlite3.Error as e:
        print("SQLite Error:", e)

    finally:
        conn.close()


if __name__ == '__main__':
    main()
