import telebot
from config import BOT_TOKEN, ADMIN_ID
from lwdb import save_to_db
from telebot import types
from faq import faq_template

bot = telebot.TeleBot(BOT_TOKEN)


def get_faq_keyboard():
    """Обычная клавиатура с вопросами (внизу экрана)"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    for question in faq_template.keys():
        ks = types.KeyboardButton(question)
        keyboard.add(ks)
    
    # Кнопка "Назад" (чтобы убрать клавиатуру)
    keyboard.add(types.KeyboardButton("🔙 Закрыть FAQ"))
    
    return keyboard

def format_answer(question, answer):
    return f"{question}\n\n{answer}"

def is_admin(user_id):
    return user_id == ADMIN_ID


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, """Привет! Я бот-помощник интернет-магазина «ВАШЕ НАЗВАНИЕ ИНТЕРНЕТ МАГАЗИНА».

Я здесь, чтобы быстро решить ваши вопросы. Умею:

✅ Отвечать на частые вопросы (доставка, оплата, возврат)
✅ Связывать с живым специалистом, если нужно

🔧 У нас два отдела:
• Программисты — если не работает сайт или оплата
• Отдел продаж — вопросы про товары, заказы, возвраты

💬 Просто напишите /faq, и я постараюсь помочь!

📌 Попробуйте:
• «Что такое [название продукта/сервиса]?»
• «Как начать пользоваться [название продукта/сервиса]?»
• «Что делать, если [название продукта/сервиса] не запускается?»

❔ Остались еще вопросы попробуйте:
• /save дальше напишите подробную ситуацию с который вы столкнулись

""")

@bot.message_handler(commands=['faq'])
def show_faq(message):
    bot.send_message(
        message.chat.id,
        "📚 Часто задаваемые вопросы\n\n"
        "Нажмите на интересующий вопрос:",
        reply_markup=get_faq_keyboard(),
    )
    
@bot.message_handler(commands=['save'])
def s_a_c(message):
    text = message.text.replace('/save', '')

    message_id = save_to_db(
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.first_name,
        issue=text
    )

    bot.send_message(message.chat.id, "Мы передали вашу проблему специалистам. Они свяжутся с вами в ближайшее время.")


    user_info = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    bot.send_message(
        ADMIN_ID,
        f"Новый вопрос от пользователя!\n\n"
        f"Пользователь: {user_info}\n"
        f"ID: {message.from_user.id}\n"
        f"Вопрос: {text}\n\n"
        f"Чтобы ответить, используйте:\n"
        f"/answer {message.from_user.id} [текст] - ответить"
    )


@bot.message_handler(commands=['answer'])
def answer_to_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "У вас нет прав для этой команды.")
        return
    
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(
            message.chat.id,
            "Укажите ID пользователя и текст ответа.\n"
            "Пример: /answer 11... Ваш заказ уже отправлен."
        )
        return
    
    try:
        user_id = int(parts[1])
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный ID пользователя. Введите число."
        )
        return
    
    answer_text = parts[2]
    
    try:
        bot.send_message(
            user_id,
            f"Ответ от специалиста:\n{answer_text}\n"
            f"Если у вас остались вопросы, напишите их снова."
        )
        
        bot.send_message(message.chat.id,f"Ответ отправлен пользователю (ID: {user_id})!")
        
    except Exception as error:
        bot.send_message(
            message.chat.id,
            f"Ошибка при отправке ответа: {str(error)}"
        )



@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    
    
    if text == "🔙 Закрыть FAQ":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "FAQ закрыт.\nНапишите /faq чтобы открыть снова.",
            reply_markup=keyboard
        )
        return
    
    if text in faq_template:
        answer = faq_template[text]
        response = format_answer(text, answer)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(
            message.chat.id,
            "Я не нашел ответ на ваш вопрос.\n\n"
            "Напишите /faq чтобы увидеть список всех вопросов."
        )


bot.infinity_polling()