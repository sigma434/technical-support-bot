import telebot
from config import BOT_TOKEN
from lwdb import save_to_db

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, """Привет! Я бот-помощник интернет-магазина «ВАШЕ НАЗВАНИЕ ИНТЕРНЕТ МАГАЗИНА».

Я здесь, чтобы быстро решить ваши вопросы. Умею:

✅ Отвечать на частые вопросы (доставка, оплата, возврат)
✅ Связывать с живым специалистом, если нужно

🔧 У нас два отдела:
• Программисты — если не работает сайт или оплата
• Отдел продаж — вопросы про товары, заказы, возвраты

💬 Просто напишите свой вопрос, и я постараюсь помочь!

📌 Попробуйте:
• «Как оформить заказ?»
• «Не проходит оплата»
• «Где мой заказ?»

""")

@bot.message_handler(commands=['faq'])
def connection_w_staff(message):
    bot.send_message(message.chat.id, )
    
@bot.message_handler(commands=['save'])
def s_a_c(message):
    text = message.text.replace('/save', '')


    message_id = save_to_db(
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.first_name,
        issue=text
    )

#СТРУКТУРА ДЛЯ МЕНЯ БУДУ ПИСАТЬ КАПСОМ
#КРЧ БЕРЕШЬ СОХРАНЯЕШЬ ФАЙЛ ПЕРЕКИДЫВЕШЬ ЕГО В ДБ ЖТО С КЬЮА
# С ФАКЙУЮ БЕРЕШЬ ДОБАВЛЯЕШЬ КНОПОЧКИ С КЛЮЧАМИ ОН ИХ БЕРЕТ ПЕРЕКИДЫВАЕТ СЮДЫ А ТЫ БЕРЕШЬ ИХ И С ПОМОЗЬЮ ИМПОРТИРОВАННОГО СЛОВАРЯ ОТВЕЧАЕШЬ НА ЕГО ВОПРОС
# вроде как все рассказал


bot.infinity_polling()