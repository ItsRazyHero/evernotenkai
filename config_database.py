import sqlite3


def create_database():
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_sum INTEGER,
            discount_level INTEGER
        )
    ''')

    conn.commit()
    conn.close()


def create_users_database():
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            birth_day TEXT
        )
    ''')

    conn.commit()
    conn.close()


def set_user_bday_by_user_id(user_id, bday):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET birth_day = ?
        WHERE user_id = ?
    ''', (bday, user_id))

    conn.commit()
    conn.close()


def create_user(user_id):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (user_id, order_sum, discount_level)
        VALUES (?, ?, ?)
    ''', (user_id, 0, 0))

    conn.commit()
    conn.close()


def get_user_by_user_id(user_id):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))

    return cursor.fetchone()


def add_position():
    conn = sqlite3.connect('database.db')

    name = f"🍊 Апельсин"
    category = '🍪 Печенье'
    price = 55
    rating = 4.3
    description = 'Состав: мука миндальная, пудра сахарная, яйцо, сахарный песок, пюре апельсиновое, пектин.'
    image = "imgs/cookies/cook_05.jpg"
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO desert (desert_name, category, price, rating, description, image)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (f"{name}", f'{category}', price, rating, f"{description}", f"{image}"))

    conn.commit()
    conn.close()


def delete_order_by_tag(tag):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM orders WHERE order_tag = ?
    ''', (tag,))

    conn.commit()
    conn.close()


def get_order_by_tag(tag):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM orders WHERE order_tag = ?
    ''', (tag,))

    return cursor.fetchone()


def update_user(user_id, order_sum, discount_level):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users
        SET order_sum = ?, discount_level = ?
        WHERE user_id = ?
    ''', (order_sum, discount_level, user_id))

    conn.commit()
    conn.close()


def get_unique_categories() -> list[tuple]:
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT category FROM desert
    ''')

    return cursor.fetchall()


def get_elements() -> list[tuple]:
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM desert
    ''')

    return cursor.fetchall()


def get_elements_by_category(category) -> list[tuple]:
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT desert_name, category, image FROM desert
        WHERE category = ?
    ''', (category,))

    return cursor.fetchall()


def get_elements_by_name(name) -> list[tuple]:
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT price, rating, description, image FROM desert
        WHERE desert_name = ?
    ''', (name,))

    return cursor.fetchall()


def delete_by_name(name):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM desert
        WHERE desert_name = ?
    ''', (name,))

    conn.commit()
    conn.close()


def create_order(tag, user, price, desc):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (order_tag, user, price, description)
        VALUES (?,?,?,?)
    ''', (tag, user, price, desc))

    conn.commit()
    conn.close()


def get_first_9_orders() -> list[tuple]:
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM orders
        LIMIT 9
    ''')

    return cursor.fetchall()


def replace_row_by_name(name, category, price, rating, description, image):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        UPDATE desert
        SET category = ?, price = ?, rating = ?, description = ?, image = ?
        WHERE desert_name = ?
    ''', (category, price, rating, description, image, name))

    conn.commit()
    conn.close()


def delete_by_name_and_category(name, category):
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM desert
        WHERE desert_name = ? AND category = ?
    ''', (name, category))

    conn.commit()
    conn.close()


def delete_table_by_name():
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS users
    ''')

    conn.commit()
    conn.close()


def main():
    update_user(6474105213, 100, 0)


if __name__ == '__main__':
    main()
