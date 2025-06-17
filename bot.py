import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, MESSAGES, LEVELS, LANGUAGES
from keyboards import (get_language_keyboard, get_level_keyboard, get_kapital_keyboard,
                      get_results_keyboard, get_main_menu_reply_keyboard)
from database import get_user_progress, update_user_progress
from test_loader import test_loader
import time
import random
import asyncio

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# User ma'lumotlarini saqlash
user_data = {}
user_tests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i - til tanlash"""
    user_id = update.effective_user.id
    
    # User ma'lumotlarini boshlang'ich holatga keltirish
    user_data[user_id] = {
        'language': 'uz',
        'level': None
    }
    
    # Til tanlash xabari va keyboard
    await update.message.reply_text(
        MESSAGES['uz']['welcome'],
        reply_markup=get_language_keyboard()
    )

# PASTKI MENU MESSAGE HANDLER
async def handle_menu_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pastki menu xabarlarini boshqarish"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # User ma'lumotlarini tekshirish
    if user_id not in user_data:
        user_data[user_id] = {'language': 'uz', 'level': None}
    
    user_language = user_data[user_id].get('language', 'uz')
    print(f"🔍 DEBUG: Pastki menu xabari: {message_text}")
    
    # Test boshlash
    if message_text in ['🎯 Test boshlash', '🎯 Начать тест', '🎯 Start Test', '🎯 Test starten']:
        await update.message.reply_text(
            MESSAGES[user_language]['select_level'],
            reply_markup=get_level_keyboard()
        )
    
    # Natijalarim
    elif message_text in ['📊 Natijalarim', '📊 Мои результаты', '📊 My Results', '📊 Meine Ergebnisse']:
        await show_results_message(update, user_id, user_language)
    
    # Tilni o'zgartirish
    elif message_text in ['🌐 Tilni o\'zgartirish', '🌐 Сменить язык', '🌐 Change Language', '🌐 Sprache ändern']:
        await update.message.reply_text(
            "🌐 Yangi tilni tanlang:",
            reply_markup=get_language_keyboard()
        )
    
    # Yordam
    elif message_text in ['ℹ️ Yordam', 'ℹ️ Помощь', 'ℹ️ Help', 'ℹ️ Hilfe']:
        await update.message.reply_text(MESSAGES[user_language]['help_info'])
    
    # Sozlamalar
    elif message_text in ['⚙️ Sozlamalar', '⚙️ Настройки', '⚙️ Settings', '⚙️ Einstellungen']:
        settings_text = f"""⚙️ SOZLAMALAR
{'━' * 25}
👤 User ID: {user_id}
🌐 Til: {LANGUAGES.get(user_language, 'O\'zbek')}
🎯 Joriy daraja: {user_data[user_id].get('level', 'Tanlanmagan')}

🔄 Sozlamalarni o'zgartirish uchun tegishli tugmalardan foydalaning.
        """
        await update.message.reply_text(settings_text)
    
    else:
        # Noma'lum xabar
        await update.message.reply_text(
            f"❓ Noma'lum buyruq. Pastki menudagi tugmalardan foydalaning.",
            reply_markup=get_main_menu_reply_keyboard(user_language)
        )

async def show_results_message(update, user_id, user_language):
    """Natijalarni xabar sifatida ko'rsatish"""
    progress = get_user_progress(user_id)
    
    if not progress:
        results_text = f"""📊 NATIJALARIM
{'━' * 25}
❌ Hali testlar topshirilmagan.
🎯 Birinchi testni topshiring!
        """
    else:
        total_tests = progress.get('total_tests', 0)
        correct_answers = progress.get('correct_answers', 0)
        accuracy = (correct_answers / max(total_tests, 1)) * 100
        
        results_text = f"""📊 NATIJALARIM
{'━' * 25}
✅ Topshirilgan testlar: {total_tests}
🎯 To'g'ri javoblar: {correct_answers}
📈 Aniqlik: {accuracy:.1f}%

🏆 DARAJALAR:
{'━' * 25}
        """
        
        # Har daraja bo'yicha ma'lumot
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            level_progress = progress.get('levels', {}).get(level, {})
            completed = level_progress.get('completed_kapitals', [])
            if completed:
                results_text += f"\n{LEVELS[level]} - {len(completed)}/12 kapital"

    await update.message.reply_text(
        results_text,
        reply_markup=get_results_keyboard()
    )

# ✅ YAGONA CALLBACK HANDLER
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback query handler"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    print(f"🔍 Callback data: {data}")
    print(f"👤 User ID: {user_id}")
    
    # User ma'lumotlarini tekshirish
    if user_id not in user_data:
        user_data[user_id] = {'language': 'uz', 'level': None}
    
    user_language = user_data[user_id].get('language', 'uz')
    
    # Language selection
    if data.startswith('lang_'):
        language = data.split('_')[1]
        user_data[user_id]['language'] = language
        print(f"🌐 Til tanlandi: {language}")
        
        # Pastki menuni ko'rsatish
        await query.edit_message_text(
            f"✅ Til o'zgartirildi: {LANGUAGES[language]}\n\n🎯 Endi pastki menudagi tugmalardan foydalaning!"
        )
        
        # Pastki menuni yuborish
        await query.message.reply_text(
            MESSAGES[language]['select_level'],
            reply_markup=get_main_menu_reply_keyboard(language)
        )
    
    # Level selection
    elif data.startswith('level_'):
        level = data.split('_')[1]
        user_data[user_id]['level'] = level
        print(f"📊 Level tanlandi: {level}, Til: {user_language}")
        
        # Xabarni yangilash - kapitallar ko'rsatish
        await query.edit_message_text(
            MESSAGES[user_language]['select_kapital'].format(level=level),
            reply_markup=get_kapital_keyboard(level)
        )
    
    # Kapital selection ✅ BU MUHIM!
    elif data.startswith('kapital_'):
        parts = data.split('_')
        level = parts[1]
        kapital = int(parts[2])
        print(f"📚 Kapital tanlandi: {level} - {kapital}")
        
        await start_test(update, context, level, kapital)
    
    # Start test now
    elif data.startswith('start_now_'):
        user_id = int(data.split('_')[2])
        print(f"🚀 Test boshlandi: User {user_id}")
        await show_question(update, context, user_id)
    
    # Answer handling
    elif data.startswith('answer_'):
        await handle_answer(update, context)
    
    # Next question
    elif data.startswith('next_'):
        await next_question(update, context)
    
    # Orqaga tugmasi
    elif data == 'back_to_levels':
        await query.edit_message_text(
            MESSAGES[user_language]['select_level'],
            reply_markup=get_level_keyboard()
        )
    
    # Statistika
    elif data == 'general_stats':
        await show_general_stats(query, user_id, user_language)
    elif data == 'level_stats':
        await show_level_stats(query, user_id, user_language)
    
    else:
        print(f"❓ Noma'lum callback: {data}")

# ✅ YAXSHILANGAN TEST FUNKSIYALARI
async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str, kapital: int):
    """Testni boshlash - YAXSHILANGAN"""
    print(f"🎯 start_test CHAQIRILDI: {level} - {kapital}")
    
    user_id = update.effective_user.id
    language = user_data.get(user_id, {}).get('language', 'uz')
    
    print(f"👤 User: {user_id}, Til: {language}")
    
    try:
        # Test ma'lumotlarini olish
        test_info = test_loader.get_test_info(level, kapital, language)
        print(f"📋 Test info olindi: {bool(test_info)}")
        
        if not test_info:
            print(f"❌ Test info bo'sh!")
            await update.callback_query.edit_message_text("❌ Test topilmadi!")
            return
        
        # Savollarni olish
        questions = test_loader.get_questions(level, kapital, count=100, language=language)
        print(f"❓ Questions olindi: {len(questions)} ta")
        
        if not questions:
            print(f"❌ Savollar bo'sh!")
            await update.callback_query.edit_message_text("❌ Savollar topilmadi!")
            return
        
        # Test sessiyasini boshlash
        user_tests[user_id] = {
            'level': level,
            'kapital': kapital,
            'questions': questions,
            'current_question': 0,
            'correct_answers': 0,
            'start_time': time.time(),
            'answers': [],
            'language': language,
            'streak': 0,  # ✅ Yangi
            'max_streak': 0  # ✅ Yangi
        }
        
        print(f"✅ Test sessiyasi yaratildi")
        
        # 🎨 CHIROYLI TEST MA'LUMOTI
        text = f"""🎯 **TEST TAYYOR!**
{'━' * 30}
📚 **Daraja:** {level}
📖 **Kapital:** {kapital}
❓ **Savollar:** {len(questions)} ta
⏱️ **Vaqt:** Cheklanmagan
🎯 **Maqsad:** 70%+ natija

🚀 **Testni boshlaysizmi?**
{'━' * 30}
💡 Har bir savol uchun diqqat bilan o'ylang!"""
        
        keyboard = [[InlineKeyboardButton("🚀 Ha, boshlash!", callback_data=f"start_now_{user_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        print(f"✅ Test info yuborildi")
        
    except Exception as e:
        print(f"❌ start_test'da xatolik: {e}")
        await update.callback_query.edit_message_text(f"❌ Xatolik: {str(e)}")

async def show_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Savolni ko'rsatish - YAXSHILANGAN"""
    test_session = user_tests.get(user_id)
    
    if not test_session:
        return
    
    current_q_index = test_session['current_question']
    questions = test_session['questions']
    
    if current_q_index >= len(questions):
        # Test tugadi
        await finish_test(update, context, user_id)
        return
    
    question = questions[current_q_index]
    
    # 🎨 PROGRESS BAR
    progress = int((current_q_index / len(questions)) * 20)
    progress_bar = "█" * progress + "░" * (20 - progress)
    progress_percent = int((current_q_index / len(questions)) * 100)
    
    # ⏱️ VAQT HISOBLASH
    elapsed = int((time.time() - test_session['start_time']) / 60)
    
    # 🔥 STREAK MA'LUMOTI
    streak = test_session.get('streak', 0)
    correct = test_session.get('correct_answers', 0)
    
    # 🎨 CHIROYLI SAVOL MATNI
    text = f"""🎯 **SAVOL {current_q_index + 1}/{len(questions)}** {progress_bar} {progress_percent}%
{'━' * 35}
📚 {test_session['level']} - Kapital {test_session['kapital']} | ⏱️ {elapsed}:00
🔥 Streak: {streak} | ✅ To'g'ri: {correct}/{current_q_index}

❓ **{question['question']}**

🔸 **A)** {question['options'][0]}
🔸 **B)** {question['options'][1]}  
🔸 **C)** {question['options'][2]}
🔸 **D)** {question['options'][3]}

{'━' * 35}
💡 Diqqat bilan o'qing va javob bering!
"""

    # 🎨 CHIROYLI TUGMALAR
    keyboard = [
        [
            InlineKeyboardButton("🔸 A", callback_data=f"answer_{user_id}_0"),
            InlineKeyboardButton("🔸 B", callback_data=f"answer_{user_id}_1"),
        ],
        [
            InlineKeyboardButton("🔸 C", callback_data=f"answer_{user_id}_2"),
            InlineKeyboardButton("🔸 D", callback_data=f"answer_{user_id}_3"),
        ],
        [
            InlineKeyboardButton("⏸️ Pauza", callback_data=f"pause_{user_id}"),
            InlineKeyboardButton("❌ To'xtatish", callback_data=f"stop_{user_id}"),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await update.callback_query.edit_message_text(
            text, 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except:
        await update.callback_query.message.reply_text(
            text, 
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Javobni qayta ishlash - YAXSHILANGAN"""
    query = update.callback_query
    await query.answer()
    
    # Callback data'ni parse qilish
    parts = query.data.split('_')
    if len(parts) != 3 or parts[0] != 'answer':
        return
    
    user_id = int(parts[1])
    answer_index = int(parts[2])
    test_session = user_tests.get(user_id)
    if not test_session:
        return
    
    # Javobni tekshirish
    current_q_index = test_session['current_question']
    question = test_session['questions'][current_q_index]
    
    result = test_loader.validate_answer(question, answer_index)
    
    # Natijani saqlash
    test_session['answers'].append({
        'question_id': question.get('id'),
        'user_answer': answer_index,
        'correct_answer': result['correct_answer'],
        'is_correct': result['is_correct'],
        'points': result['points']
    })
    
    # Streak va statistikani yangilash
    if result['is_correct']:
        test_session['correct_answers'] += 1
        test_session['streak'] = test_session.get('streak', 0) + 1
        if test_session['streak'] > test_session.get('max_streak', 0):
            test_session['max_streak'] = test_session['streak']
    else:
        test_session['streak'] = 0
    
    # 🎨 CHIROYLI JAVOB ANIMATSIYASI
    if result['is_correct']:
        # ✅ TO'G'RI JAVOB
        celebration = random.choice(['🎉', '🎊', '⭐', '🌟', '💫'])
        praise = random.choice(['Ajoyib!', 'Zo\'r!', 'Mukammal!', 'A\'lo!', 'Juda yaxshi!'])
        
        response = f"""{celebration} **TO'G'RI JAVOB!** {celebration}
{'━' * 30}
💚 **{praise}**
✅ Javobingiz: **{question['options'][answer_index]}**
🔥 Streak: {test_session['streak']}
💎 Ball: +{result['points']}

📊 **Hozirgi natija:** {test_session['correct_answers']}/{current_q_index + 1}
{'━' * 30}
"""
    else:
        # ❌ NOTO'G'RI JAVOB
        sad_emoji = random.choice(['😔', '😞', '😕', '🤔'])
        
        response = f"""❌ **Afsuski noto'g'ri...** {sad_emoji}
{'━' * 30}
❤️ **Sizning javobingiz:** {question['options'][answer_index]}
💚 **To'g'ri javob:** {question['options'][result['correct_answer']]}
🔥 Streak: {test_session.get('streak', 0)} → 0

💡 **TUSHUNTIRISH:**
{result.get('explanation', 'Keyingi safar diqqat bilan o\'qing!')}

📊 **Hozirgi natija:** {test_session['correct_answers']}/{current_q_index + 1}
{'━' * 30}
"""
    
    # Keyingi savol tugmasi
    keyboard = [
        [InlineKeyboardButton("➡️ Keyingi savol", callback_data=f"next_{user_id}")],
        [InlineKeyboardButton("📊 Hozirgi natija", callback_data=f"current_stats_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')

async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Keyingi savolga o'tish"""
    query = update.callback_query
    await query.answer()
    
    user_id = int(query.data.split('_')[1])
    test_session = user_tests.get(user_id)
    
    if not test_session:
        return
    
    # Keyingi savolga o'tish
    test_session['current_question'] += 1
    await show_question(update, context, user_id)


async def show_general_stats(query, user_id, user_language):
    """Umumiy statistikani ko'rsatish - YAXSHILANGAN"""
    progress = get_user_progress(user_id)
    
    # 📊 CHIROYLI STATISTIKA
    stats_text = f"""📈 **UMUMIY STATISTIKA**
{'━' * 35}
👤 **User ID:** {user_id}
🗓️ **Ro'yxatdan o'tgan:** {progress.get('join_date', 'Noma\'lum')}
🔥 **Faollik:** {progress.get('activity_days', 0)} kun
⏰ **Umumiy vaqt:** {progress.get('total_time', 0)} daqiqa

🎯 **TEST NATIJALARI:**
{'━' * 35}
✅ **Jami testlar:** {progress.get('total_tests', 0)}
🎯 **To'g'ri javoblar:** {progress.get('correct_answers', 0)}
❌ **Noto'g'ri javoblar:** {progress.get('wrong_answers', 0)}
📊 **O'rtacha ball:** {progress.get('average_score', 0):.1f}%

🏆 **YUTUQLAR:**
{'━' * 35}
🔥 **Eng uzun streak:** {progress.get('max_streak', 0)}
⭐ **Eng yaxshi natija:** {progress.get('best_score', 0)}%
💎 **Jami ball:** {progress.get('total_points', 0)}
"""
    
    await query.edit_message_text(
        stats_text,
        reply_markup=get_results_keyboard(),
        parse_mode='Markdown'
    )

async def show_level_stats(query, user_id, user_language):
    """Daraja bo'yicha statistikani ko'rsatish - YAXSHILANGAN"""
    progress = get_user_progress(user_id)
    levels_data = progress.get('levels', {})
    
    stats_text = f"""🎯 **DARAJA BO'YICHA STATISTIKA**
{'━' * 40}
"""
    
    for level_code, level_name in LEVELS.items():
        level_data = levels_data.get(level_code, {})
        completed = len(level_data.get('completed_kapitals', []))
        total_score = level_data.get('total_score', 0)
        
        if completed > 0:
            avg_score = total_score / completed
            # Progress bar
            progress_filled = int((completed / 12) * 10)
            progress_bar = "▓" * progress_filled + "░" * (10 - progress_filled)
            
            stats_text += f"""📚 **{level_name}**
Progress: {progress_bar} **{completed}/12**
O'rtacha: **{avg_score:.1f}%**
Status: {'🟢 Faol' if completed > 0 else '⚪ Boshlanmagan'}
{'━' * 40}
"""
        else:
            stats_text += f"""📚 **{level_name}**
Progress: ░░░░░░░░░░ **0/12**
Status: ⚪ **Boshlanmagan**
{'━' * 40}
"""
    
    await query.edit_message_text(
        stats_text,
        reply_markup=get_results_keyboard(),
        parse_mode='Markdown'
    )

def main():
    """Botni ishga tushirish"""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler'larni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # PASTKI MENU uchun Message Handler qo'shish
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_messages))
    
    # Botni ishga tushirish
    print("🚀 Bot ishga tushdi...")
    print("📱 Telegram'da botingizni sinab ko'ring!")
    print("📋 Pastki menu qo'shildi!")
    print("🎨 Chiroyli dizayn qo'shildi!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str, kapital: int):
    """Testni boshlash - YAXSHILANGAN"""
    print(f"🎯 start_test CHAQIRILDI: {level} - {kapital}")
    
    user_id = update.effective_user.id
    language = user_data.get(user_id, {}).get('language', 'uz')
    
    print(f"👤 User: {user_id}, Til: {language}")
    
    try:
        # Test ma'lumotlarini olish
        test_info = test_loader.get_test_info(level, kapital, language)
        print(f"📋 Test info olindi: {bool(test_info)}")
        
        if not test_info:
            print(f"❌ Test info bo'sh!")
            await update.callback_query.edit_message_text("❌ Test topilmadi!")
            return
        
        # 100 ta savol olish
        questions = test_loader.get_questions(level, kapital, count=100, language=language)
        print(f"❓ Questions olindi: {len(questions)} ta")
        
        if not questions:
            print(f"❌ Savollar bo'sh!")
            await update.callback_query.edit_message_text("❌ Savollar topilmadi!")
            return
        
        # Test sessiyasini boshlash
        user_tests[user_id] = {
            'level': level,
            'kapital': kapital,
            'questions': questions,
            'current_question': 0,
            'correct_answers': 0,
            'start_time': time.time(),
            'answers': [],
            'language': language,
            'streak': 0,
            'max_streak': 0
        }
        
        print(f"✅ Test sessiyasi yaratildi")
        
        # Vaqt hisoblash
        estimated_time = len(questions) * 1.5  # 1.5 daqiqa/savol
        
        # Chiroyli test ma'lumoti
        text = f"""🎯 **TEST TAYYOR!**
{'━' * 30}
📚 **Daraja:** {level}
📖 **Kapital:** {kapital}
❓ **Savollar:** {len(questions)} ta
⏱️ **Taxminiy vaqt:** {int(estimated_time)} daqiqa
🎯 **Maqsad:** 70%+ natija

🚀 **Testni boshlaysizmi?**
{'━' * 30}
💡 Bu katta test! Tayyor bo'lganingizdan ishonch hosil qiling!"""
        
        keyboard = [[InlineKeyboardButton("🚀 Ha, boshlash!", callback_data=f"start_now_{user_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        print(f"✅ Test info yuborildi")
        
    except Exception as e:
        print(f"❌ start_test'da xatolik: {e}")
        await update.callback_query.edit_message_text(f"❌ Xatolik: {str(e)}")


async def show_results_message(update, user_id, user_language):
    """Natijalarni xabar sifatida ko'rsatish - YAXSHILANGAN"""
    progress = get_user_progress(user_id)
    
    if not progress:
        # Hali test topshirmagan holatda
        results_text = f"""📊 **NATIJALARIM**
{'━' * 35}
🎯 **Xush kelibsiz!**

❌ Hali testlar topshirilmagan
🚀 Birinchi testingizni boshlang!

💡 **Maslahat:**
• A1 darajasidan boshlang
• Har kuni 10-15 daqiqa mashq qiling
• Doimiylik - muvaffaqiyat kaliti!

{'━' * 35}
🎯 Hoziroq test boshlaysizmi?"""
        
        keyboard = [
            [InlineKeyboardButton("🚀 Birinchi testni boshlash", callback_data="level_A1")],
            [InlineKeyboardButton("📚 Darajalar haqida", callback_data="about_levels")]
        ]
        
    else:
        # Statistika mavjud bo'lsa
        total_tests = progress.get('total_tests', 0)
        correct_answers = progress.get('correct_answers', 0)
        wrong_answers = progress.get('wrong_answers', 0)
        total_questions = correct_answers + wrong_answers
        accuracy = (correct_answers / max(total_questions, 1)) * 100
        
        # Daraja bo'yicha progress
        levels_data = progress.get('levels', {})
        completed_levels = 0
        total_kapitals = 0
        
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            level_data = levels_data.get(level, {})
            completed = len(level_data.get('completed_kapitals', []))
            total_kapitals += completed
            if completed >= 6:  # Yarim daraja
                completed_levels += 0.5
            if completed >= 12:  # To'liq daraja
                completed_levels += 0.5
        
        # Eng yaxshi natija
        best_score = progress.get('best_score', 0)
        avg_score = progress.get('average_score', 0)
        
        # Faollik kunlari
        activity_days = progress.get('activity_days', 0)
        total_time = progress.get('total_time', 0)
        
        # Daraja aniqlash
        if accuracy >= 90:
            level_status = "🌟 EXPERT"
            level_emoji = "🏆"
        elif accuracy >= 80:
            level_status = "🥇 ADVANCED"
            level_emoji = "⭐"
        elif accuracy >= 70:
            level_status = "🥈 INTERMEDIATE"
            level_emoji = "👍"
        elif accuracy >= 60:
            level_status = "🥉 BEGINNER"
            level_emoji = "📚"
        else:
            level_status = "📖 LEARNING"
            level_emoji = "🌱"
        
        results_text = f"""📊 **NATIJALARIM** {level_emoji}
{'━' * 40}
🏆 **STATUS:** {level_status}
📈 **Umumiy aniqlik:** {accuracy:.1f}%

📋 **TEST STATISTIKASI:**
✅ To'g'ri javoblar: **{correct_answers:,}**
❌ Noto'g'ri javoblar: **{wrong_answers:,}**
📊 Jami testlar: **{total_tests:,}**
🎯 Eng yaxshi natija: **{best_score}%**
📈 O'rtacha natija: **{avg_score:.1f}%**

⏰ **FAOLLIK:**
🔥 Faol kunlar: **{activity_days}** kun
⏱️ Jami vaqt: **{total_time}** daqiqa
📚 Tugallangan kapitallar: **{total_kapitals}**

🎯 **DARAJA BO'YICHA PROGRESS:**
{'━' * 40}"""

        # Har daraja uchun batafsil ma'lumot
        for level_code in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            level_name = LEVELS.get(level_code, level_code)
            level_data = levels_data.get(level_code, {})
            completed = len(level_data.get('completed_kapitals', []))
            avg_score_level = level_data.get('average_score', 0)
            
            # Progress bar
            progress_filled = int((completed / 12) * 10)
            progress_bar = "▓" * progress_filled + "░" * (10 - progress_filled)
            
            # Status emoji
            if completed == 12:
                status_emoji = "✅"
                status_text = "Tugallangan"
            elif completed >= 6:
                status_emoji = "🔄"
                status_text = "Jarayonda"
            elif completed > 0:
                status_emoji = "🟡"
                status_text = "Boshlangan"
            else:
                status_emoji = "⚪"
                status_text = "Boshlanmagan"
            
            results_text += f"""
{status_emoji} **{level_name}**
{progress_bar} **{completed}/12** ({status_text})"""
            
            if completed > 0:
                results_text += f" | O'rtacha: **{avg_score_level:.1f}%**"
        
        results_text += f"""

{'━' * 40}
🎯 **Keyingi maqsad:** {get_next_goal(progress)}
💡 **Tavsiya:** {get_recommendation(progress)}"""
        
        # Tugmalar
        keyboard = [
            [
                InlineKeyboardButton("📈 Batafsil statistika", callback_data="detailed_stats"),
                InlineKeyboardButton("🏆 Yutuqlarim", callback_data="achievements")
            ],
            [
                InlineKeyboardButton("📊 Grafik ko'rish", callback_data="progress_chart"),
                InlineKeyboardButton("🔄 Yangilash", callback_data="refresh_stats")
            ],
            [
                InlineKeyboardButton("🎯 Test boshlash", callback_data="start_new_test"),
                InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home_page")
            ]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        results_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def get_next_goal(progress):
    """Keyingi maqsadni aniqlash"""
    total_tests = progress.get('total_tests', 0)
    accuracy = progress.get('accuracy', 0)
    levels_data = progress.get('levels', {})
    
    # Eng kam tugallangan darajani topish
    for level_code in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
        level_data = levels_data.get(level_code, {})
        completed = len(level_data.get('completed_kapitals', []))
        if completed < 12:
            remaining = 12 - completed
            return f"{LEVELS[level_code]} darajasini tugallash ({remaining} kapital qoldi)"
    
    return "Barcha darajalarni takrorlash va natijani yaxshilash"

def get_recommendation(progress):
    """Shaxsiy tavsiya berish"""
    accuracy = progress.get('accuracy', 0)
    total_tests = progress.get('total_tests', 0)
    activity_days = progress.get('activity_days', 0)
    
    if accuracy < 60:
        return "Asosiy qoidalarni takrorlang va sekinroq ishlang"
    elif accuracy < 80:
        return "Yaxshi! Har kuni 15-20 daqiqa mashq qiling"
    elif activity_days < 7:
        return "Doimiylik muhim! Har kuni kamida 1 ta test topsiring"
    elif total_tests < 50:
        return "Ko'proq amaliyot qiling, tajriba to'plang"
    else:
        return "Ajoyib! Qiyinroq darajalarni sinab ko'ring"

# Qo'shimcha callback handlerlar
async def handle_detailed_stats(query, user_id):
    """Batafsil statistika"""
    progress = get_user_progress(user_id)
    
    # Haftalik/oylik statistika
    # Eng ko'p xato qilingan mavzular
    # Vaqt bo'yicha tahlil
    # va boshqalar...

async def handle_achievements(query, user_id):
    """Yutuqlar tizimi"""
    progress = get_user_progress(user_id)
    achievements = []
    
    # Turli yutuqlarni tekshirish
    if progress.get('total_tests', 0) >= 10:
        achievements.append("🎯 Birinchi 10 test")
    
    if progress.get('accuracy', 0) >= 90:
        achievements.append("🌟 90%+ aniqlik")
    
    # va boshqalar...
