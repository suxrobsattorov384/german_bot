import json
import os


DATABASE_FILE = 'user_progress.json'

def load_user_data():
    """User ma'lumotlarini yuklash"""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_data(data):
    """User ma'lumotlarini saqlash"""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_progress(user_id):
    """Foydalanuvchi progressini olish"""
    data = load_user_data()
    return data.get(str(user_id), {})

def update_user_progress(user_id, progress):
    """Foydalanuvchi progressini yangilash"""
    data = load_user_data()
    data[str(user_id)] = progress
    save_user_data(data)
