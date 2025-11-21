import openpyxl
import customtkinter as ctk 
from tkinter import messagebox
import sqlite3
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def connect_db():
    return sqlite3.connect("store.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER,
                        quantity INTEGER,
                        date TEXT,
                        FOREIGN KEY (product_id) REFERENCES products(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        position TEXT NOT NULL,
                        salary REAL NOT NULL,
                        hire_date TEXT NOT NULL)''')
    
    # Добавляем сотрудников только если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        employees_data = [
            ('Иванов Иван Иванович', 'Продавец', 45000, '15-01-2020'),
            ('Петрова Анна Сергеевна', 'Менеджер', 60000, '20-03-2021'),
            ('Сидоров Алексей Владимирович', 'Менеджер', 60000, '10-05-2019'),
            ('Кузнецова Елена Дмитриевна', 'Продавец', 45000, '05-11-2022'),
            ('Васильев Дмитрий Петрович', 'Администратор', 70000, '12-09-2023')
        ]
        cursor.executemany(
            "INSERT INTO employees (name, position, salary, hire_date) VALUES (?, ?, ?, ?)",
            employees_data
        )

    # Добавляем продукцию только если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        products_data = [
            ('Джинсы', 3500.00, 50),
            ('Куртка кожаная', 11000.00, 30),
            ('Кроссовки для бега', 4000.00, 50),
            ('Носки мужские', 50.00, 120),
            ('Плащ-дождевик', 500.00, 10),
            ('Ботинки зимние', 5000.00, 40),
            ('Кепка с сеткой', 1100.00, 65)
        ]
        cursor.executemany(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            products_data
        )
    
    conn.commit()
    conn.close()


def authenticate():
    login = entry_login.get()
    password = entry_password.get()

    if login == "admin" and password == "123456":
        login_win.destroy()
        main_window()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

def main_window():
    global root
    root = ctk.CTk()
    root.title("Информационная система магазина одежды")
    root.geometry("900x400")
    create_tables()

    frame = ctk.CTkFrame(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    button_width = 25

    # Секция "Работа с товаром"
    ctk.CTkLabel(frame, text="Работа с товаром", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=40, pady=5, sticky="w")
    ctk.CTkButton(frame, text="Добавить товар", command=add_product, width=button_width).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Редактировать товар", command=edit_product, width=button_width).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Удалить товар", command=delete_product, width=button_width).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Просмотр списка товара", command=view_products, width=button_width).grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    # Секция "Продажи"
    ctk.CTkLabel(frame, text="Продажи", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=100, pady=5, sticky="w")
    ctk.CTkButton(frame, text="Добавить продажу", command=add_sale, width=button_width).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Посмотреть отчеты о продажах", command=view_sales_reports, width=button_width).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Секция "Управление персоналом" 
    ctk.CTkLabel(frame, text="Управление персоналом", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=25, pady=5, sticky="w")
    ctk.CTkButton(frame, text="Добавить сотрудника", command=add_employee, width=button_width).grid(row=1, column=2, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Редактировать сотрудника", command=edit_employee, width=button_width).grid(row=2, column=2, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Удалить сотрудника", command=delete_employee, width=button_width).grid(row=3, column=2, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(frame, text="Просмотр списка сотрудников", command=view_employees, width=button_width).grid(row=4, column=2, padx=10, pady=5, sticky="ew")

    root.mainloop()

def login_window():
    global entry_login, entry_password, login_win
    login_win = ctk.CTk()
    login_win.title("Авторизация")
    login_win.geometry("300x200")

    frame = ctk.CTkFrame(login_win)
    frame.pack(pady=20)

    ctk.CTkLabel(frame, text="Логин").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_login = ctk.CTkEntry(frame)
    entry_login.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Пароль").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_password = ctk.CTkEntry(frame, show="*")
    entry_password.grid(row=1, column=1, pady=5)

    ctk.CTkButton(login_win, text="Войти", command=authenticate).pack(pady=10)

    login_win.mainloop()

# ===== Функции для работы с продукцией =====
def add_product():
    def save_product():
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите добавить продукцию?"):
            name = entry_name.get()
            price = float(entry_price.get())
            quantity = int(entry_quantity.get())

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Продукция добавлена")
            add_window.destroy()

    add_window = ctk.CTkToplevel(root)
    add_window.title("Добавление продукции")

    frame = ctk.CTkFrame(add_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="Название").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_name = ctk.CTkEntry(frame)
    entry_name.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Цена").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_price = ctk.CTkEntry(frame)
    entry_price.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(frame, text="Количество").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_quantity = ctk.CTkEntry(frame)
    entry_quantity.grid(row=2, column=1, pady=5)

    ctk.CTkButton(add_window, text="Сохранить", command=save_product).pack(pady=10)

def edit_product():
    def update_product():
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите обновить продукцию?"):
            product_id = int(entry_id.get())
            name = entry_name.get()
            price = float(entry_price.get())
            quantity = int(entry_quantity.get())

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?", 
                        (name, price, quantity, product_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Продукция обновлена")
            edit_window.destroy()

    edit_window = ctk.CTkToplevel(root)
    edit_window.title("Редактирование продукции")

    frame = ctk.CTkFrame(edit_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Название").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_name = ctk.CTkEntry(frame)
    entry_name.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(frame, text="Цена").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_price = ctk.CTkEntry(frame)
    entry_price.grid(row=2, column=1, pady=5)

    ctk.CTkLabel(frame, text="Количество").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_quantity = ctk.CTkEntry(frame)
    entry_quantity.grid(row=3, column=1, pady=5)

    ctk.CTkButton(edit_window, text="Обновить", command=update_product).pack(pady=10)

def delete_product():
    def remove_product():
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить продукцию?"):
            product_id = int(entry_id.get())

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Продукция удалена")
            delete_window.destroy()

    delete_window = ctk.CTkToplevel(root)
    delete_window.title("Удаление продукции")

    frame = ctk.CTkFrame(delete_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, pady=5)

    ctk.CTkButton(delete_window, text="Удалить", command=remove_product).pack(pady=10)

def view_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    view_window = ctk.CTkToplevel(root)
    view_window.title("Список продукции")

    for product in products:
        ctk.CTkLabel(view_window, text=f"ID: {product[0]} | Название: {product[1]} | Цена: {product[2]} | Кол-во: {product[3]}").pack(anchor="w", padx=10, pady=2)

# ===== Функции для работы с продажами =====
def add_sale():
    def save_sale():
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите добавить продажу?"):
            product_id = int(entry_product_id.get())
            quantity = int(entry_quantity.get())
            date_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT quantity, price FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()

            if product and product[0] >= quantity:
                cursor.execute("INSERT INTO sales (product_id, quantity, date) VALUES (?, ?, ?)", (product_id, quantity, date_now))
                cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (product[0] - quantity, product_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Продажа добавлена")
                sale_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Недостаточно товара")

    sale_window = ctk.CTkToplevel(root)
    sale_window.title("Добавление продажи")

    frame = ctk.CTkFrame(sale_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ID продукции").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_product_id = ctk.CTkEntry(frame)
    entry_product_id.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Количество").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_quantity = ctk.CTkEntry(frame)
    entry_quantity.grid(row=1, column=1, pady=5)

    ctk.CTkButton(sale_window, text="Сохранить", command=save_sale).pack(pady=10)

def view_sales_reports():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT sales.id, products.name, sales.quantity, products.price, sales.date
                      FROM sales JOIN products ON sales.product_id = products.id''')
    sales = cursor.fetchall()
    total_sum = sum(s[2] * s[3] for s in sales)
    conn.close()

    report_window = ctk.CTkToplevel(root)
    report_window.title("Отчеты о продажах")

    for sale in sales:
        total_price = sale[2] * sale[3]
        ctk.CTkLabel(report_window, text=f"ID: {sale[0]} | Продукт: {sale[1]} | Кол-во: {sale[2]} | Сумма: {total_price} | Дата: {sale[4]}").pack(anchor="w", padx=10)

    ctk.CTkLabel(report_window, text=f"Общая сумма продаж: {total_sum}").pack(pady=10)

    def clear_sales():
        if messagebox.askyesno("Подтверждение", "Удалить все отчеты?"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sales")
            conn.commit()
            conn.close()
            messagebox.showinfo("Готово", "Все отчеты удалены")
            report_window.destroy()

    def export_to_excel():
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Продажи"

        headers = ["ID", "Продукт", "Кол-во", "Цена за шт.", "Дата", "Сумма"]
        sheet.append(headers)

        for sale in sales:
            total_price = sale[2] * sale[3]
            sheet.append([sale[0], sale[1], sale[2], sale[3], sale[4], total_price])

        sheet.append(["", "", "", "", "Итого:", total_sum])

        try:
            workbook.save("sales_report.xlsx")
            messagebox.showinfo("Успех", "Отчет успешно сохранен в файл sales_report.xlsx")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    ctk.CTkButton(report_window, text="Сохранить в EXCEL", command=export_to_excel).pack(pady=5)
    ctk.CTkButton(report_window, text="Очистить отчеты", command=clear_sales).pack(pady=5)

# ===== Функции для работы с сотрудниками =====
def add_employee():
    def save_employee():
        if messagebox.askyesno("Подтверждение", "Добавить сотрудника?"):
            name = entry_name.get()
            position = entry_position.get()
            salary = float(entry_salary.get())
            hire_date = entry_hire_date.get()

            if not hire_date:
                messagebox.showerror("Ошибка", "Укажите дату приёма на работу")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employees (name, position, salary, hire_date) VALUES (?, ?, ?, ?)", 
                         (name, position, salary, hire_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Сотрудник добавлен")
            add_window.destroy()

    add_window = ctk.CTkToplevel(root)
    add_window.title("Добавление сотрудника")

    frame = ctk.CTkFrame(add_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ФИО").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_name = ctk.CTkEntry(frame)
    entry_name.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="Должность").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_position = ctk.CTkEntry(frame)
    entry_position.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(frame, text="Зарплата").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_salary = ctk.CTkEntry(frame)
    entry_salary.grid(row=2, column=1, pady=5)

    ctk.CTkLabel(frame, text="Дата приёма (ДД-ММ-ГГГГ)").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_hire_date = ctk.CTkEntry(frame, placeholder_text="ДД-ММ-ГГГГ")
    entry_hire_date.grid(row=3, column=1, pady=5)

    ctk.CTkButton(add_window, text="Сохранить", command=save_employee).pack(pady=10)

def edit_employee():
    def update_employee():
        if messagebox.askyesno("Подтверждение", "Обновить данные сотрудника?"):
            employee_id = int(entry_id.get())
            name = entry_name.get()
            position = entry_position.get()
            salary = float(entry_salary.get())
            hire_date = entry_hire_date.get()

            if not hire_date:
                messagebox.showerror("Ошибка", "Укажите дату приёма на работу")
                return

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET name=?, position=?, salary=?, hire_date=? WHERE id=?", 
                         (name, position, salary, hire_date, employee_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Данные обновлены")
            edit_window.destroy()

    edit_window = ctk.CTkToplevel(root)
    edit_window.title("Редактирование сотрудника")

    frame = ctk.CTkFrame(edit_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(frame, text="ФИО").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_name = ctk.CTkEntry(frame)
    entry_name.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(frame, text="Должность").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_position = ctk.CTkEntry(frame)
    entry_position.grid(row=2, column=1, pady=5)

    ctk.CTkLabel(frame, text="Зарплата").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_salary = ctk.CTkEntry(frame)
    entry_salary.grid(row=3, column=1, pady=5)

    ctk.CTkLabel(frame, text="Дата приёма (ДД-ММ-ГГГГ)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_hire_date = ctk.CTkEntry(frame, placeholder_text="ДД-ММ-ГГГГ")
    entry_hire_date.grid(row=4, column=1, pady=5)

    # Заполняем текущие данные
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=?", (entry_id.get(),))
    employee = cursor.fetchone()
    conn.close()
    
    if employee:
        entry_name.insert(0, employee[1])
        entry_position.insert(0, employee[2])
        entry_salary.insert(0, str(employee[3]))
        entry_hire_date.insert(0, employee[4])

    ctk.CTkButton(edit_window, text="Обновить", command=update_employee).pack(pady=10)

def delete_employee():
    def remove_employee():
        if messagebox.askyesno("Подтверждение", "Удалить сотрудника?"):
            employee_id = int(entry_id.get())

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Сотрудник удален")
            delete_window.destroy()

    delete_window = ctk.CTkToplevel(root)
    delete_window.title("Удаление сотрудника")

    frame = ctk.CTkFrame(delete_window)
    frame.pack(pady=10, padx=10)

    ctk.CTkLabel(frame, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, pady=5)

    ctk.CTkButton(delete_window, text="Удалить", command=remove_employee).pack(pady=10)

def view_employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()

    view_window = ctk.CTkToplevel(root)
    view_window.title("Список сотрудников")
    view_window.geometry("800x400")

    scroll_frame = ctk.CTkScrollableFrame(view_window)
    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for employee in employees:
        emp_text = (f"ID: {employee[0]} | ФИО: {employee[1]} | Должность: {employee[2]} | "
                   f"Зарплата: {employee[3]} | Дата приёма: {employee[4]}")
        ctk.CTkLabel(scroll_frame, text=emp_text).pack(anchor="w", padx=10, pady=2)

# Запуск приложения
login_window()