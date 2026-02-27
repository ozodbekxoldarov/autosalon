import mysql.connector
from mysql.connector import Error
import getpass
import sys
import time

# ====== Database helper class ======
class Database:
    def __init__(self, host, user, password, database):
        self.cfg = {'host': host, 'user': user, 'password': password, 'database': database}
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.cfg)
        except Error as e:
            print("DB ga ulanishda xatolik:", e)
            sys.exit(1)

    def fetch_all(self, query, params=None):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetch_one(self, query, params=None):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        cursor.close()
        return row

    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        self.conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def close(self):
        if self.conn:
            self.conn.close()

# ====== App logic ======
class App:
    def __init__(self, db: Database):
        self.db = db

    def run(self):
        self.db.connect()
        print("=== Avtosalon konsol ilovasi ===")
        while True:
            print("\n1) Ro'yhatdan o'tish")
            print("2) Avtomobillar jadvali")
            print("3) Qidirish (model bo'yicha)")
            print("4) Avtomobilni ko'rish (id bo'yicha)")
            print("5) Sotib olish")
            print("6) Chiqish")
            choice = input("Tanlov (1-6): ").strip()
            if choice == '1':
                self.register_customer()
            elif choice == '2':
                self.show_cars()
            elif choice == '3':
                self.search_cars()
            elif choice == '4':
                self.view_car_by_id()
            elif choice == '5':
                self.buy_car()
            elif choice == '6':
                print("Dastur tugadi. Xayr!")
                self.db.close()
                break
            else:
                print("Noto'g'ri tanlov. qayta urinib ko'ring.")

    def register_customer(self):
        print("\n-- Ro'yhatdan o'tish --")
        fn = input("Ism: ").strip()
        ln = input("Familiya: ").strip()
        phone = input("Telefon: ").strip()
        email = input("Email: ").strip()
        passport = input("Pasport raqami: ").strip()

        if not fn or not ln:
            print("Ism va familiya majburiy.")
            return
        q = """INSERT INTO customers (first_name, last_name, phone, email, passport)
               VALUES (%s,%s,%s,%s,%s)"""
        try:
            cid = self.db.execute(q, (fn, ln, phone, email, passport))
            print(f"Muvaffaqiyat! Mijoz id: {cid}")
        except Exception as e:
            print("Xato:", e)

    def show_cars(self):
        rows = self.db.fetch_all("SELECT id, brand, model, year, price, color FROM cars ORDER BY id")
        if not rows:
            print("Avtomobil yo'q.")
            return
        print("\n-- Avtomobillar jadvali --")
        print(f"{'id':<4} {'brand':<10} {'model':<18} {'year':<6} {'price':>10} {'color':<8}")
        for r in rows:
            print(f"{r['id']:<4} {r['brand'] or '-':<10} {r['model']:<18} {r['year'] or '-':<6} {r['price']:>10} {r['color'] or '-':<8}")

    def search_cars(self):
        term = input("Qidirish (model nomi yozing): ").strip()
        if not term:
            print("Hech narsa kiritilmadi.")
            return
        q = "SELECT id, brand, model, year, price FROM cars WHERE model LIKE %s"
        rows = self.db.fetch_all(q, (f"%{term}%",))
        if not rows:
            print("Hech narsa topilmadi.")
            return
        print(f"\nTopildi: {len(rows)} ta")
        for r in rows:
            print(f"id:{r['id']} - {r['brand']} {r['model']} ({r['year']}) - ${r['price']}")

    def view_car_by_id(self):
        try:
            cid = int(input("Avtomobil id sini kiriting: ").strip())
        except:
            print("Id butun son bo'lishi kerak.")
            return
        q = "SELECT * FROM cars WHERE id = %s"
        car = self.db.fetch_one(q, (cid,))
        if not car:
            print("Bunday avtomobil topilmadi.")
            return
        print("\n-- Avtomobil ma'lumotlari --")
        for k, v in car.items():
            print(f"{k}: {v}")

    def buy_car(self):
        try:
            cid = int(input("Sotib olinadigan avtomobil id: ").strip())
        except:
            print("Id noto'g'ri.")
            return
        car = self.db.fetch_one("SELECT * FROM cars WHERE id = %s", (cid,))
        if not car:
            print("Bunday avtomobil yo'q.")
            return
        print(f"Siz tanladingiz: {car['brand']} {car['model']} - Narxi: {car['price']}")
        # mijozni aniqlash (ixtiyoriy): ro'yhatda bo'lgan mijoz id sini so'rash
        buyer = input("Mijoz passport yoki telefon kiriting (ro'yhatda bo'lsa): ").strip()
        # to'lov summasi
        try:
            amount = float(input("To'lov (sumda yoki valyutada): ").strip())
        except:
            print("To'lov noto'g'ri kiritildi.")
            return
        price = float(car['price'])
        if amount < price:
            print("To'lov yetarli emas. Xarid amalga oshmadi.")
            return
        # agar yetarli bo'lsa: o'chirish va tasdiq
        try:
            self.db.execute("DELETE FROM cars WHERE id = %s", (cid,))
            print("Siz muvaffaqiyatli sotib oldingiz! Avtomobil bazadan o'chirildi.")
            # ixtiyoriy: purchase history hozir yo'q, keyinchalik qo'shsa bo'ladi
            if amount > price:
                change = amount - price
                print(f"To'lovdan ortiq summasi: {change:.2f}")
        except Exception as e:
            print("Xatolik yuz berdi:", e)
    