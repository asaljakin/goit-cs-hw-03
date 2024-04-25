import sqlite3
from faker import Faker
import random

# Підключення до бази даних SQLite
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Створення таблиць
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    fullname TEXT,
                    email TEXT UNIQUE
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS status (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
                 )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    status_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (status_id) REFERENCES status (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                 )''')

# Заповнення таблиць випадковими значеннями за допомогою Faker
fake = Faker()

# Заповнення таблиці users
for _ in range(10):
    name = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

# Заповнення таблиці status
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (?)", (status,))

# Заповнення таблиці tasks
for _ in range(20):
    title = fake.sentence()
    description = fake.text()
    status_id = random.randint(1, len(statuses))
    user_id = random.randint(1, 10)
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                   (title, description, status_id, user_id))

# Збереження змін та закриття з'єднання
conn.commit()
conn.close()
