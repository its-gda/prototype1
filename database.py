import sqlite3
import os

  # Create folder for images if it doesn't exist
if not os.path.exists("uploads"):
      os.makedirs("uploads")

def get_connection():
      return sqlite3.connect("store_data.db", check_same_thread=False)

def init_db():
      conn = get_connection()
      cursor = conn.cursor()

      # Users Table
      cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT UNIQUE,
                          password TEXT,
                          tier TEXT DEFAULT 'Free')''')

      # Stores Table
      cursor.execute('''CREATE TABLE IF NOT EXISTS stores (
                          user_id INTEGER PRIMARY KEY,
                          store_name TEXT,
                          logo_path TEXT,
                          brand_color TEXT DEFAULT '#FFFFFF',
                          layout TEXT DEFAULT 'Grid',
                          FOREIGN KEY(user_id) REFERENCES users(id))''')

      # Products Table
      cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          name TEXT,
                          description TEXT,
                          price REAL,
                          link TEXT,
                          image_path TEXT,
                          FOREIGN KEY(user_id) REFERENCES users(id))''')
      conn.commit()
      conn.close()

def add_user(username, password):
      try:
          conn = get_connection()
          cursor = conn.cursor()
          cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
          conn.commit()
          conn.close()
          return True
      except sqlite3.IntegrityError:
          return False

def verify_user(username, password):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
      user = cursor.fetchone()
      conn.close()
      return user[0] if user else None

def update_store(user_id, name, color, layout, logo_path=None):
      conn = get_connection()
      cursor = conn.cursor()
      if logo_path:
          cursor.execute("INSERT OR REPLACE INTO stores (user_id, store_name, brand_color, layout, logo_path) VALUES (?, ?, ?, ?, ?)",
                         (user_id, name, color, layout, logo_path))
      else:
          cursor.execute("INSERT OR REPLACE INTO stores (user_id, store_name, brand_color, layout) VALUES (?, ?, ?, ?)",
                         (user_id, name, color, layout))
      conn.commit()
      conn.close()

def get_store_details(user_id):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM stores WHERE user_id = ?", (user_id,))
      data = cursor.fetchone()
      conn.close()
      return data

def add_product(user_id, name, desc, price, link, image_path):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("INSERT INTO products (user_id, name, description, price, link, image_path) VALUES (?, ?, ?, ?, ?, ?)",
                     (user_id, name, desc, price, link, image_path))
      conn.commit()
      conn.close()

def get_products(user_id):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
      rows = cursor.fetchall()
      conn.close()
      return rows

def get_all_premium_stores():
      conn = get_connection()
      cursor = conn.cursor()
      # Joins users and stores to find only Premium users
      cursor.execute("SELECT stores.store_name, stores.logo_path, users.username FROM stores JOIN users ON stores.user_id = users.id WHERE users.tier = 'Premium'")
      rows = cursor.fetchall()
      conn.close()
      return rows

def update_user_tier(user_id, tier):
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("UPDATE users SET tier = ? WHERE id = ?", (tier, user_id))
      conn.commit()
      conn.close()

init_db()