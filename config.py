import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Tillar
LANGUAGES = {
    'uz': '🇺🇿 O\'zbek',
    'ru': '🇷🇺 Русский', 
    'en': '🇬🇧 English',
    'de': '🇩🇪 Deutsch'
}

# Darajalar
LEVELS = {
    'A1': '🟢 A1 - Boshlang\'ich',
    'A2': '🟡 A2 - Elementar', 
    'B1': '🔵 B1 - O\'rta',
    'B2': '🟠 B2 - Yuqori o\'rta',
    'C1': '🟣 C1 - Ilg\'or',
    'C2': '⚫ C2 - Mukammal'
}

# Xabarlar
MESSAGES = {
    'uz': {
        'welcome': '''🇩🇪 DEUTSCH LERNEN BOT
━━━━━━━━━━━━━━━━━━━━━

👋 Assalomu alaykum va xush kelibsiz!

🎯 **Bu bot orqali siz:**
• Nemis tilini bosqichma-bosqich o'rganasiz
• A1 dan C2 gacha barcha darajalarni o'zlashtirasiz  
• 72 ta kapital bo'yicha test topshirasiz
• O'z natijalaringizni kuzatib borasiz

🌟 **Boshlash uchun tilni tanlang:**''',

        'select_level': '''🎯 DARAJA TANLASH
━━━━━━━━━━━━━━━━━━━━━

📚 **Qaysi darajadan boshlaysiz?**

🟢 **A1** - Yangi boshlovchilar uchun
🟡 **A2** - Asosiy bilimlar
🔵 **B1** - O'rta daraja
🟠 **B2** - Mustaqil foydalanuvchi
🟣 **C1** - Ilg'or daraja
⚫ **C2** - Mukammal bilim

💡 Agar ishonchingiz komil bo'lmasa, A1 dan boshlang!''',

        'select_kapital': '''📖 {level} KAPITALLARI
━━━━━━━━━━━━━━━━━━━━━

🎯 **{level} darajasida 12 ta kapital mavjud**

📋 Har bir kapitalda:
• 15-20 ta yangi so'z
• Grammatika qoidalari
• Amaliy mashqlar
• Test savollari

🔥 **Qaysi kapitaldan boshlaysiz?**

💡 Ketma-ketlikda o'rganish tavsiya etiladi!''',

        'test_started': '''🎯 TEST BOSHLANDI!
━━━━━━━━━━━━━━━━━━━━━

📚 **Daraja:** {level}
📖 **Kapital:** {kapital}

⏰ **Vaqt:** Cheklanmagan
❓ **Savollar soni:** 15 ta
🎯 **O'tish balli:** 70%

🔥 **Qoidalar:**
• Har savolga diqqat bilan javob bering
• Bir marta tanlangan javobni o'zgartirib bo'lmaydi
• Natija darhol ko'rsatiladi

✅ **Tayyor bo'lsangiz, birinchi savolga o'ting!**''',

        'help_info': '''ℹ️ YORDAM VA MA'LUMOT
━━━━━━━━━━━━━━━━━━━━━

🤖 **Bot haqida:**
Bu bot Nemis tilini o'rganish uchun mo'ljallangan. Barcha darajalar uchun testlar va materiallar mavjud.

📖 **Qanday foydalanish:**

1️⃣ **Boshlash:** Tilni va darajangizni tanlang
2️⃣ **O'rganish:** Kapitallarni ketma-ket o'rganing  
3️⃣ **Test:** Har kapital oxirida test topshiring
4️⃣ **Tahlil:** Natijalaringizni kuzatib boring

🎯 **Darajalar:**
• **A1-A2:** Boshlang'ich (0-2 yil)
• **B1-B2:** O'rta (2-4 yil)  
• **C1-C2:** Ilg'or (4+ yil)

📊 **Baholash tizimi:**
• 90-100% - A'lo
• 80-89% - Yaxshi
• 70-79% - Qoniqarli
• 70% dan past - Takrorlash kerak

💡 **Maslahatlar:**
• Har kuni 15-30 daqiqa vaqt ajrating
• Noto'g'ri javoblarni qayta ko'rib chiqing
• Grammatikaga alohida e'tibor bering

📞 **Yordam:** @your_username''',

        'my_results': '''📊 MENING NATIJALARIM
━━━━━━━━━━━━━━━━━━━━━

👤 **Shaxsiy statistika**''',

        'no_results': '''📊 NATIJALAR TOPILMADI
━━━━━━━━━━━━━━━━━━━━━

❌ **Hali birorta test topshirilmagan**

🎯 **Birinchi testni topshirish uchun:**
1. Pastki menuda "🎯 Test boshlash" tugmasini bosing
2. Darajangizni tanlang
3. Birinchi kapitaldan boshlang

💪 **Muvaffaqiyat yo'lida birinchi qadamni tashlang!**''',

        'settings_info': '''⚙️ SOZLAMALAR
━━━━━━━━━━━━━━━━━━━━━

🔧 **Joriy sozlamalar:**

👤 **Foydalanuvchi ID:** {user_id}
🌐 **Interfeys tili:** {language}
🎯 **Joriy daraja:** {level}
📅 **Ro'yxatdan o'tgan:** {join_date}
🔥 **Faollik:** {activity_days} kun

⚡ **Tezkor sozlamalar:**
• Tilni o'zgartirish uchun "🌐 Tilni o'zgartirish" tugmasini bosing
• Darajani o'zgartirish uchun "🎯 Test boshlash" orqali yangi daraja tanlang

🔄 **Ma'lumotlarni tozalash:**
Barcha natijalarni o'chirish uchun @admin ga murojaat qiling''',

        'language_changed': '''✅ TIL MUVAFFAQIYATLI O'ZGARTIRILDI!
━━━━━━━━━━━━━━━━━━━━━

🌐 **Yangi til:** {language}

🎯 **Endi pastki menudagi tugmalardan foydalaning:**

🎯 **Test boshlash** - Yangi test topshirish
📊 **Natijalarim** - Statistikani ko'rish  
🌐 **Tilni o'zgartirish** - Boshqa tilga o'tish
ℹ️ **Yordam** - Qo'llanma va maslahatlar
⚙️ **Sozlamalar** - Shaxsiy sozlamalar

🔥 **Omad tilaymiz!**''',

        'test_completed': '''🎉 TEST YAKUNLANDI!
━━━━━━━━━━━━━━━━━━━━━

📊 **Sizning natijangiz:**

✅ **To'g'ri javoblar:** {correct}/{total}
📈 **Foiz:** {percentage}%
🏆 **Baho:** {grade}

{result_message}

📚 **Keyingi qadamlar:**
{next_steps}''',

        'excellent_result': '''🌟 **AJOYIB NATIJA!**
Siz bu mavzuni mukammal o'zlashtirdingiz!''',

        'good_result': '''👍 **YAXSHI NATIJA!**
Yaxshi bilim ko'rsatdingiz, davom eting!''',

        'satisfactory_result': '''📖 **QONIQARLI NATIJA!**
Asosiy bilimlar o'zlashtirildi, biroz ko'proq mashq qiling.''',

        'poor_result': '''📚 **TAKRORLASH KERAK!**
Bu mavzuni qaytadan o'rganishni tavsiya etamiz.''',

        'continue_next': '''➡️ Keyingi kapitalga o'tishingiz mumkin
🔄 Bu kapitalni qayta topshiring
📊 Natijalaringizni ko'rib chiqing''',

        'study_again': '''📖 Materialni qayta o'rganing
🔄 Testni qayta topshiring  
💡 Yordam bo'limini o'qing'''
    },

    'ru': {
        'welcome': '''🇩🇪 DEUTSCH LERNEN BOT
━━━━━━━━━━━━━━━━━━━━━

👋 Добро пожаловать!

🎯 **С помощью этого бота вы:**
• Изучите немецкий язык пошагово
• Освоите все уровни от A1 до C2
• Пройдете тесты по 72 главам
• Отследите свои результаты

🌟 **Выберите язык для начала:**''',

        'select_level': '''🎯 ВЫБОР УРОВНЯ
━━━━━━━━━━━━━━━━━━━━━

📚 **С какого уровня начнете?**

🟢 **A1** - Для новичков
🟡 **A2** - Базовые знания
🔵 **B1** - Средний уровень
🟠 **B2** - Независимый пользователь
🟣 **C1** - Продвинутый уровень
⚫ **C2** - Совершенное знание

💡 Если не уверены, начните с A1!''',

        'select_kapital': '''📖 ГЛАВЫ {level}
━━━━━━━━━━━━━━━━━━━━━

🎯 **На уровне {level} доступно 12 глав**

📋 В каждой главе:
• 15-20 новых слов
• Правила грамматики
• Практические упражнения
• Тестовые вопросы

🔥 **С какой главы начнете?**

💡 Рекомендуется изучать последовательно!''',

        'help_info': '''ℹ️ ПОМОЩЬ И ИНФОРМАЦИЯ
━━━━━━━━━━━━━━━━━━━━━

🤖 **О боте:**
Этот бот предназначен для изучения немецкого языка. Доступны тесты и материалы для всех уровней.

📖 **Как использовать:**

1️⃣ **Начало:** Выберите язык и уровень
2️⃣ **Изучение:** Проходите главы последовательно
3️⃣ **Тестирование:** Сдавайте тест после каждой главы
4️⃣ **Анализ:** Отслеживайте результаты

📞 **Помощь:** @your_username'''
    },

    'en': {
        'welcome': '''🇩🇪 DEUTSCH LERNEN BOT
━━━━━━━━━━━━━━━━━━━━━

👋 Welcome!

🎯 **With this bot you will:**
• Learn German step by step
• Master all levels from A1 to C2
• Take tests on 72 chapters
• Track your progress

🌟 **Choose your language to start:**''',

        'select_level': '''🎯 LEVEL SELECTION
━━━━━━━━━━━━━━━━━━━━━

📚 **Which level will you start with?**

🟢 **A1** - For beginners
🟡 **A2** - Basic knowledge
🔵 **B1** - Intermediate level
🟠 **B2** - Independent user
🟣 **C1** - Advanced level
⚫ **C2** - Perfect knowledge

💡 If unsure, start with A1!''',

        'help_info': '''ℹ️ HELP & INFORMATION
━━━━━━━━━━━━━━━━━━━━━

🤖 **About the bot:**
This bot is designed for learning German. Tests and materials are available for all levels.

📞 **Support:** @your_username'''
    },

    'de': {
        'welcome': '''🇩🇪 DEUTSCH LERNEN BOT
━━━━━━━━━━━━━━━━━━━━━

👋 Willkommen!

🎯 **Mit diesem Bot werden Sie:**
• Deutsch Schritt für Schritt lernen
• Alle Niveaus von A1 bis C2 meistern
• Tests zu 72 Kapiteln absolvieren
• Ihren Fortschritt verfolgen

🌟 **Wählen Sie Ihre Sprache zum Starten:**''',

        'select_level': '''🎯 NIVEAU-AUSWAHL
━━━━━━━━━━━━━━━━━━━━━

📚 **Mit welchem Niveau beginnen Sie?**

🟢 **A1** - Für Anfänger
🟡 **A2** - Grundkenntnisse
🔵 **B1** - Mittelstufe
🟠 **B2** - Selbständige Sprachverwendung
🟣 **C1** - Fortgeschrittene Kenntnisse
⚫ **C2** - Annähernd muttersprachliche Kenntnisse

💡 Falls unsicher, beginnen Sie mit A1!''',

        'help_info': '''ℹ️ HILFE & INFORMATION
━━━━━━━━━━━━━━━━━━━━━

🤖 **Über den Bot:**
Dieser Bot ist zum Deutschlernen konzipiert. Tests und Materialien sind für alle Niveaus verfügbar.

📞 **Support:** @your_username'''
    }
}

# Motivatsion xabarlar
MOTIVATIONAL_MESSAGES = {
    'uz': [
        "🔥 Ajoyib! Davom eting!",
        "💪 Siz zo'rsiz! Oldinga!",
        "🌟 Mukammal natija!",
        "🎯 To'g'ri yo'ldasiz!",
        "⚡ Energiya to'la!",
        "🚀 Yuqori parvoz!",
        "🏆 Champion kabi!",
        "💎 Qimmatli bilim!",
        "🎊 Tabriklaymiz!",
        "🔝 Eng yaxshi natija!"
    ],
    'ru': [
        "🔥 Отлично! Продолжайте!",
        "💪 Вы великолепны!",
        "🌟 Превосходный результат!",
        "🎯 Вы на правильном пути!",
        "⚡ Полны энергии!",
        "🚀 Высокий полет!",
        "🏆 Как чемпион!",
        "💎 Ценные знания!",
        "🎊 Поздравляем!",
        "🔝 Лучший результат!"
    ],
    'en': [
        "🔥 Excellent! Keep going!",
        "💪 You're amazing!",
        "🌟 Perfect result!",
        "🎯 You're on the right track!",
        "⚡ Full of energy!",
        "🚀 Flying high!",
        "🏆 Like a champion!",
        "💎 Valuable knowledge!",
        "🎊 Congratulations!",
        "🔝 Best result!"
    ],
    'de': [
        "🔥 Ausgezeichnet! Weiter so!",
        "💪 Sie sind großartig!",
        "🌟 Perfektes Ergebnis!",
        "🎯 Sie sind auf dem richtigen Weg!",
        "⚡ Voller Energie!",
        "🚀 Hoch hinaus!",
        "🏆 Wie ein Champion!",
        "💎 Wertvolles Wissen!",
        "🎊 Herzlichen Glückwunsch!",
        "🔝 Bestes Ergebnis!"
    ]
}

# Baho tizimlari
GRADE_SYSTEM = {
    'uz': {
        'A': {'min': 90, 'name': 'A\'lo', 'emoji': '🌟', 'message': 'Mukammal natija!'},
        'B': {'min': 80, 'name': 'Yaxshi', 'emoji': '👍', 'message': 'Juda yaxshi!'},
        'C': {'min': 70, 'name': 'Qoniqarli', 'emoji': '📖', 'message': 'Yaxshi harakat!'},
        'F': {'min': 0, 'name': 'Takrorlash kerak', 'emoji': '📚', 'message': 'Qayta urinib ko\'ring!'}
    },
    'ru': {
        'A': {'min': 90, 'name': 'Отлично', 'emoji': '🌟', 'message': 'Превосходный результат!'},
        'B': {'min': 80, 'name': 'Хорошо', 'emoji': '👍', 'message': 'Очень хорошо!'},
        'C': {'min': 70, 'name': 'Удовлетворительно', 'emoji': '📖', 'message': 'Хорошая попытка!'},
        'F': {'min': 0, 'name': 'Нужно повторить', 'emoji': '📚', 'message': 'Попробуйте еще раз!'}
    },
    'en': {
        'A': {'min': 90, 'name': 'Excellent', 'emoji': '🌟', 'message': 'Perfect result!'},
        'B': {'min': 80, 'name': 'Good', 'emoji': '👍', 'message': 'Very good!'},
        'C': {'min': 70, 'name': 'Satisfactory', 'emoji': '📖', 'message': 'Good effort!'},
        'F': {'min': 0, 'name': 'Need to repeat', 'emoji': '📚', 'message': 'Try again!'}
    },
    'de': {
        'A': {'min': 90, 'name': 'Ausgezeichnet', 'emoji': '🌟', 'message': 'Perfektes Ergebnis!'},
        'B': {'min': 80, 'name': 'Gut', 'emoji': '👍', 'message': 'Sehr gut!'},
        'C': {'min': 70, 'name': 'Befriedigend', 'emoji': '📖', 'message': 'Gute Leistung!'},
        'F': {'min': 0, 'name': 'Wiederholen', 'emoji': '📚', 'message': 'Versuchen Sie es nochmal!'}
    }
}

# Kapital nomlari
KAPITAL_NAMES = {
    'uz': {
        1: "Kapital",
        2: "Kapital", 
        3: "Kapital",
        4: "Kapital",
        5: "Kapital",
        6: "Kapital",
        7: "Kapital",
        8: "Kapital",
        9: "Kapital",
        10: "Kapital",
        11: "Kapital",
        12: "Kapital"
    },
    'ru': {
        1: "Kapital",
        2: "Kapital", 
        3: "Kapital",
        4: "Kapital",
        5: "Kapital",
        6: "Kapital",
        7: "Kapital",
        8: "Kapital",
        9: "Kapital",
        10: "Kapital",
        11: "Kapital",
        12: "Kapital"
    },
    'en': {
       1: "Kapital",
        2: "Kapital", 
        3: "Kapital",
        4: "Kapital",
        5: "Kapital",
        6: "Kapital",
        7: "Kapital",
        8: "Kapital",
        9: "Kapital",
        10: "Kapital",
        11: "Kapital",
        12: "Kapital"
    },
    'de': {
       1: "Kapital",
        2: "Kapital", 
        3: "Kapital",
        4: "Kapital",
        5: "Kapital",
        6: "Kapital",
        7: "Kapital",
        8: "Kapital",
        9: "Kapital",
        10: "Kapital",
        11: "Kapital",
        12: "Kapital"
    }
}

# Daraja tavsiflari
LEVEL_DESCRIPTIONS = {
    'uz': {
        'A1': "🟢 Boshlang'ich daraja - Asosiy so'zlar va oddiy gaplar",
        'A2': "🟡 Elementar daraja - Kundalik mavzularda muloqot",
        'B1': "🔵 O'rta daraja - Mustaqil nutq va yozuv",
        'B2': "🟠 Yuqori o'rta - Murakkab mavzularda fikr bildirish", 
        'C1': "🟣 Ilg'or daraja - Erkin va tabiiy muloqot",
        'C2': "⚫ Mukammal daraja - Ona tili darajasida bilim"
    },
    'ru': {
        'A1': "🟢 Начальный уровень - Основные слова и простые фразы",
        'A2': "🟡 Элементарный уровень - Общение на повседневные темы",
        'B1': "🔵 Средний уровень - Самостоятельная речь и письмо",
        'B2': "🟠 Выше среднего - Выражение мыслей по сложным темам",
        'C1': "🟣 Продвинутый уровень - Свободное и естественное общение", 
        'C2': "⚫ Совершенный уровень - Знание на уровне родного языка"
    },
    'en': {
        'A1': "🟢 Beginner level - Basic words and simple phrases",
        'A2': "🟡 Elementary level - Communication on everyday topics",
        'B1': "🔵 Intermediate level - Independent speech and writing",
        'B2': "🟠 Upper intermediate - Expressing ideas on complex topics",
        'C1': "🟣 Advanced level - Fluent and natural communication",
        'C2': "⚫ Proficient level - Native-like knowledge"
    },
    'de': {
        'A1': "🟢 Anfängerniveau - Grundwörter und einfache Sätze",
        'A2': "🟡 Grundstufe - Kommunikation über Alltagsthemen", 
        'B1': "🔵 Mittelstufe - Selbständiges Sprechen und Schreiben",
        'B2': "🟠 Obere Mittelstufe - Meinungsäußerung zu komplexen Themen",
        'C1': "🟣 Fortgeschrittene Stufe - Fließende und natürliche Kommunikation",
        'C2': "⚫ Kompetente Sprachverwendung - Muttersprachliches Niveau"
    }
}

# Xatolik xabarlari
ERROR_MESSAGES = {
    'uz': {
        'no_level': "❌ Avval darajangizni tanlang!",
        'no_kapital': "❌ Kapital topilmadi!",
        'test_error': "❌ Testda xatolik yuz berdi. Qayta urinib ko'ring!",
        'database_error': "❌ Ma'lumotlar bazasida xatolik. Admin bilan bog'laning!",
        'unknown_command': "❓ Noma'lum buyruq. Pastki menudagi tugmalardan foydalaning."
    },
    'ru': {
        'no_level': "❌ Сначала выберите уровень!",
        'no_kapital': "❌ Глава не найдена!",
        'test_error': "❌ Ошибка в тесте. Попробуйте еще раз!",
        'database_error': "❌ Ошибка базы данных. Обратитесь к админу!",
        'unknown_command': "❓ Неизвестная команда. Используйте кнопки в нижнем меню."
    },
    'en': {
        'no_level': "❌ Please select your level first!",
        'no_kapital': "❌ Chapter not found!",
        'test_error': "❌ Test error occurred. Please try again!",
        'database_error': "❌ Database error. Contact admin!",
        'unknown_command': "❓ Unknown command. Use bottom menu buttons."
    },
    'de': {
        'no_level': "❌ Bitte wählen Sie zuerst Ihr Niveau!",
        'no_kapital': "❌ Kapitel nicht gefunden!",
        'test_error': "❌ Testfehler aufgetreten. Bitte versuchen Sie es erneut!",
        'database_error': "❌ Datenbankfehler. Kontaktieren Sie den Admin!",
        'unknown_command': "❓ Unbekannter Befehl. Verwenden Sie die Schaltflächen im unteren Menü."
    }
}

# Statistika xabarlari
STATS_MESSAGES = {
    'uz': {
        'total_users': "👥 Jami foydalanuvchilar",
        'active_today': "🔥 Bugun faol",
        'tests_completed': "✅ Testlar topshirildi", 
        'average_score': "📊 O'rtacha ball",
        'top_performers': "🏆 Eng yaxshi natijalar",
        'learning_streak': "🔥 O'rganish seriyasi",
        'daily_goal': "🎯 Kunlik maqsad",
        'weekly_progress': "📈 Haftalik taraqqiyot"
    },
    'ru': {
        'total_users': "👥 Всего пользователей",
        'active_today': "🔥 Активны сегодня",
        'tests_completed': "✅ Тестов пройдено",
        'average_score': "📊 Средний балл", 
        'top_performers': "🏆 Лучшие результаты",
        'learning_streak': "🔥 Серия обучения",
        'daily_goal': "🎯 Дневная цель",
        'weekly_progress': "📈 Недельный прогресс"
    },
    'en': {
        'total_users': "👥 Total users",
        'active_today': "🔥 Active today",
        'tests_completed': "✅ Tests completed",
        'average_score': "📊 Average score",
        'top_performers': "🏆 Top performers", 
        'learning_streak': "🔥 Learning streak",
        'daily_goal': "🎯 Daily goal",
        'weekly_progress': "📈 Weekly progress"
    },
    'de': {
        'total_users': "👥 Gesamte Benutzer",
        'active_today': "🔥 Heute aktiv",
        'tests_completed': "✅ Tests abgeschlossen",
        'average_score': "📊 Durchschnittliche Punktzahl",
        'top_performers': "🏆 Beste Leistungen",
        'learning_streak': "🔥 Lernserie",
        'daily_goal': "🎯 Tagesziel",
        'weekly_progress': "📈 Wöchentlicher Fortschritt"
    }
}

# Vaqt formatlari
TIME_FORMATS = {
    'uz': {
        'seconds': "soniya",
        'minutes': "daqiqa", 
        'hours': "soat",
        'days': "kun",
        'weeks': "hafta",
        'months': "oy",
        'years': "yil"
    },
    'ru': {
        'seconds': "секунд",
        'minutes': "минут",
        'hours': "часов", 
        'days': "дней",
        'weeks': "недель",
        'months': "месяцев",
        'years': "лет"
    },
    'en': {
        'seconds': "seconds",
        'minutes': "minutes",
        'hours': "hours",
        'days': "days", 
        'weeks': "weeks",
        'months': "months",
        'years': "years"
    },
    'de': {
        'seconds': "Sekunden",
        'minutes': "Minuten",
        'hours': "Stunden",
        'days': "Tage",
        'weeks': "Wochen", 
        'months': "Monate",
        'years': "Jahre"
    }
}
