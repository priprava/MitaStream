import telebot, aiChat, time
from telebot import types
from collections import defaultdict
last_message_time = defaultdict(int)

def check_subscription(user_id):
    CHANNEL_ID = # Замените на реальный ID
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка проверки подписки: {e}")
        return False
    
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

bot = telebot.TeleBot('Token')
CHANNEL_ID = # Замените на реальный ID

@bot.message_handler(commands=['start'])
def start(message):
    if check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, "Вы подписаны! Вот ваш контент...")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подписаться", url=f"https://t.me/dapohkakayasilka"))
        markup.add(types.InlineKeyboardButton("Проверить подписку", callback_data="check_sub"))
        
        bot.send_message(
            message.chat.id,
            "Для использования бота необходимо подписаться на наш канал",
            reply_markup=markup
        )

@bot.message_handler(content_types = ['text'])
def start(message):
    current_time = time.time()
    if check_subscription(message.from_user.id):
        if current_time - last_message_time[message.chat.id] < 900:  # 900 секунд = 15 минут
            bot.reply_to(message, f"⏳ Пожалуйста, подождите {int((900 - (current_time - last_message_time[message.chat.id])) // 60)} минут между сообщениями.")
            return
        last_message_time[message.chat.id] = current_time
        aiChat.theme.append(message.text)
        bot.reply_to(message, "Тема успешно добавлена")

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Подписаться", url=f"https://t.me/dapohkakayasilka"))
        markup.add(types.InlineKeyboardButton("Проверить подписку", callback_data="check_sub"))
        
        bot.send_message(
            message.chat.id,
            "Для использования бота необходимо подписаться на наш канал",
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Вы подписаны! Доступ открыт.")
        # Действия для подписанных пользователей
    else:
        bot.answer_callback_query(call.id, "❌ Вы ещё не подписаны!", show_alert=True)

def start_bot():
    print("Бот запущен...")
    bot.infinity_polling()

if __name__ == '__main__':
    start_bot()
