from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, LEVELS, KAPITAL_NAMES, LEVEL_DESCRIPTIONS
import random

def get_language_keyboard():
    """Til tanlash keyboard"""
    keyboard = [
        [InlineKeyboardButton(LANGUAGES['uz'], callback_data='lang_uz'),
         InlineKeyboardButton(LANGUAGES['ru'], callback_data='lang_ru')],
        [InlineKeyboardButton(LANGUAGES['en'], callback_data='lang_en'),
         InlineKeyboardButton(LANGUAGES['de'], callback_data='lang_de')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_level_keyboard(language='uz'):
    """Daraja tanlash keyboard - tavsif bilan"""
    keyboard = []
    
    # A1-A2
    keyboard.append([
        InlineKeyboardButton(f"🟢 A1", callback_data='level_A1'),
        InlineKeyboardButton(f"🟡 A2", callback_data='level_A2')
    ])
    
    # B1-B2  
    keyboard.append([
        InlineKeyboardButton(f"🔵 B1", callback_data='level_B1'),
        InlineKeyboardButton(f"🟠 B2", callback_data='level_B2')
    ])
    
    # C1-C2
    keyboard.append([
        InlineKeyboardButton(f"🟣 C1", callback_data='level_C1'),
        InlineKeyboardButton(f"⚫ C2", callback_data='level_C2')
    ])
    
    # Qo'shimcha tugmalar
    keyboard.append([
        InlineKeyboardButton("ℹ️ Darajalar haqida", callback_data='level_info')
    ])
    
    return InlineKeyboardMarkup(keyboard)

def get_kapital_keyboard(level, language='uz'):
    """Kapital tanlash keyboard - nom bilan"""
    keyboard = []
    
    # 12 ta kapital - 2x6 grid
    for i in range(0, 12, 2):
        row = []
        for j in range(2):
            if i + j + 1 <= 12:
                kapital_num = i + j + 1
                kapital_name = KAPITAL_NAMES.get(language, KAPITAL_NAMES['uz']).get(kapital_num, f"Kapital {kapital_num}")
                
                # Kapital nomini qisqartirish
                if len(kapital_name) > 25:
                    kapital_name = kapital_name[:22] + "..."
                
                row.append(InlineKeyboardButton(
                    f'{kapital_num}. {kapital_name}', 
                    callback_data=f'kapital_{level}_{kapital_num}'
                ))
        keyboard.append(row)
    
    # Navigatsiya tugmalari
    keyboard.append([
        InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_levels'),
        InlineKeyboardButton('📊 Natijalar', callback_data='kapital_results')
    ])
    
    return InlineKeyboardMarkup(keyboard)

def get_test_keyboard():
    """Test davomida ishlatiladigan keyboard"""
    keyboard = [
        [InlineKeyboardButton('⏸️ Pauza', callback_data='test_pause')],
        [InlineKeyboardButton('❌ Testni to\'xtatish', callback_data='test_stop')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_test_result_keyboard(level, kapital_num, passed=True):
    """Test natijasi keyboard"""
    keyboard = []
    
    if passed:
        # Muvaffaqiyatli o'tgan bo'lsa
        if kapital_num < 12:
            keyboard.append([
                InlineKeyboardButton(f'➡️ Kapital {kapital_num + 1}', 
                                   callback_data=f'kapital_{level}_{kapital_num + 1}')
            ])
        
        keyboard.append([
            InlineKeyboardButton('🔄 Qayta topshirish', 
                               callback_data=f'kapital_{level}_{kapital_num}'),
            InlineKeyboardButton('📊 Batafsil natija', 
                               callback_data=f'detailed_result_{level}_{kapital_num}')
        ])
    else:
        # Muvaffaqiyatsiz bo'lsa
        keyboard.append([
            InlineKeyboardButton('🔄 Qayta urinish', 
                               callback_data=f'kapital_{level}_{kapital_num}'),
            InlineKeyboardButton('📖 Materialni o\'rganish', 
                               callback_data=f'study_material_{level}_{kapital_num}')
        ])
    
    # Umumiy tugmalar
    keyboard.append([
        InlineKeyboardButton('📋 Kapitallar', callback_data=f'show_kapitals_{level}'),
        InlineKeyboardButton('🏠 Bosh sahifa', callback_data='home_page')
    ])
    
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_reply_keyboard(language='uz'):
    """Pastki asosiy menu - boyitilgan"""
    if language == 'uz':
        keyboard = [
            ['🎯 Test boshlash', '📊 Natijalarim'],
            ['🌐 Tilni o\'zgartirish', '⚙️ Sozlamalar'],
            ['ℹ️ Yordam', '🏆 Reyting']
        ]
    elif language == 'ru':
        keyboard = [
            ['🎯 Начать тест', '📊 Мои результаты'],
            ['🌐 Сменить язык', '⚙️ Настройки'],
            ['ℹ️ Помощь', '🏆 Рейтинг']
        ]
    elif language == 'en':
        keyboard = [
            ['🎯 Start Test', '📊 My Results'],
            ['🌐 Change Language', '⚙️ Settings'],
            ['ℹ️ Help', '🏆 Rating']
        ]
    elif language == 'de':
        keyboard = [
            ['🎯 Test starten', '📊 Meine Ergebnisse'],
            ['🌐 Sprache ändern', '⚙️ Einstellungen'],
            ['ℹ️ Hilfe', '🏆 Bewertung']
        ]
    else:
        keyboard = [
            ['🎯 Test boshlash', '📊 Natijalarim'],
            ['🌐 Tilni o\'zgartirish', '⚙️ Sozlamalar'],
            ['ℹ️ Yordam', '🏆 Reyting']
        ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def get_results_keyboard(language='uz'):
    """Natijalar sahifasi keyboard - kengaytirilgan"""
    keyboard = [
        [InlineKeyboardButton('📈 Umumiy statistika', callback_data='general_stats'),
         InlineKeyboardButton('🎯 Daraja bo\'yicha', callback_data='level_stats')],
        [InlineKeyboardButton('📅 Haftalik hisobot', callback_data='weekly_report'),
         InlineKeyboardButton('🏆 Yutuqlarim', callback_data='achievements')],
        [InlineKeyboardButton('📊 Taqqoslash', callback_data='compare_results'),
         InlineKeyboardButton('📋 Eksport', callback_data='export_results')],
        [InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard(language='uz'):
    """Sozlamalar keyboard"""
    keyboard = [
        [InlineKeyboardButton('🌐 Tilni o\'zgartirish', callback_data='change_language'),
         InlineKeyboardButton('🔔 Bildirishnomalar', callback_data='notifications')],
        [InlineKeyboardButton('🎯 Kunlik maqsad', callback_data='daily_goal'),
         InlineKeyboardButton('⏰ Eslatma vaqti', callback_data='reminder_time')],
        [InlineKeyboardButton('🗑️ Ma\'lumotlarni tozalash', callback_data='clear_data'),
         InlineKeyboardButton('📤 Ma\'lumotlarni eksport', callback_data='export_data')],
        [InlineKeyboardButton('⬅️ Orqaga', callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_random_motivational_keyboard(language='uz'):
    """Tasodifiy motivatsion keyboard"""
    motivational_buttons = [
        "💪 Davom eting!",
        "🔥 Zo'r ketmoqda!",
        "🚀 Oldinga!",
        "⭐ Ajoyib!",
        "🎯 Maqsadga yaqin!"
    ]
    
    selected = random.choice(motivational_buttons)
    keyboard = [
        [InlineKeyboardButton(selected, callback_data='motivational_click')]
    ]
    return InlineKeyboardMarkup(keyboard)

def remove_keyboard():
    """Keyboardni olib tashlash"""
    from telegram import ReplyKeyboardRemove
    return ReplyKeyboardRemove()

def get_detailed_results_keyboard(language='uz'):
    """Batafsil natijalar keyboard - YANGI"""
    keyboard = [
        [
            InlineKeyboardButton('📈 Batafsil statistika', callback_data='detailed_stats'),
            InlineKeyboardButton('🏆 Yutuqlarim', callback_data='achievements')
        ],
        [
            InlineKeyboardButton('📊 Grafik ko\'rish', callback_data='progress_chart'),
            InlineKeyboardButton('🔄 Yangilash', callback_data='refresh_stats')
        ],
        [
            InlineKeyboardButton('🎯 Test boshlash', callback_data='start_new_test'),
            InlineKeyboardButton('🏠 Bosh sahifa', callback_data='home_page')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_first_time_keyboard(language='uz'):
    """Birinchi marta foydalanuvchi uchun - YANGI"""
    keyboard = [
        [InlineKeyboardButton("🚀 Birinchi testni boshlash", callback_data="level_A1")],
        [InlineKeyboardButton("📚 Darajalar haqida", callback_data="about_levels")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_level_progress_keyboard(level, language='uz'):
    """Daraja progress keyboard - YANGI"""
    keyboard = [
        [
            InlineKeyboardButton(f'📊 {level} statistikasi', callback_data=f'level_detailed_{level}'),
            InlineKeyboardButton(f'🎯 {level} testni boshlash', callback_data=f'level_{level}')
        ],
        [
            InlineKeyboardButton('⬅️ Orqaga', callback_data='show_results'),
            InlineKeyboardButton('🏠 Bosh sahifa', callback_data='home_page')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
