import telebot
from telebot import types
import config
import logic
import database

bot = telebot.TeleBot(config.token)
database.init_db()

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('❓ FAQ')
    btn2 = types.KeyboardButton('👨‍💻 Тех.проблемы')
    btn3 = types.KeyboardButton('📦 Проблемы с заказом')
    btn4 = types.KeyboardButton('📞 Контакты')
    btn5 = types.KeyboardButton('📋 Мои обращения')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот поддержки "Продаем все на свете".\nВыберите вариант:',
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        'Доступные команды:\n'
        '/start - Главное меню\n'
        '/faq - Частые вопросы\n'
        '/tech - Техпроблемы (сайт, оплата)\n'
        '/order - Проблемы с заказом\n'
        '/tickets - Мои обращения\n'
        '/contact - Контакты'
    )

@bot.message_handler(commands=['faq'])
def faq_command(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("📦 Оформление заказа", callback_data="faq_order")
    btn2 = types.InlineKeyboardButton("📊 Статус заказа", callback_data="faq_status")
    btn3 = types.InlineKeyboardButton("❌ Отмена заказа", callback_data="faq_cancel")
    btn4 = types.InlineKeyboardButton("⚠️ Поврежденный товар", callback_data="faq_damaged")
    btn5 = types.InlineKeyboardButton("📞 Техподдержка", callback_data="faq_support")
    btn6 = types.InlineKeyboardButton("🚚 Доставка", callback_data="faq_delivery")
    btn7 = types.InlineKeyboardButton("💳 Оплата", callback_data="faq_payment")
    btn8 = types.InlineKeyboardButton("↩️ Возврат", callback_data="faq_return")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    
    bot.send_message(
        message.chat.id,
        'Выберите тему FAQ:',
        reply_markup=markup
    )

@bot.message_handler(commands=['tech'])
def tech_command(message):
    msg = bot.send_message(
        message.chat.id,
        'Опишите техническую проблему (сайт не работает, ошибка оплаты и т.д.):',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, process_tech_problem)

def process_tech_problem(message):
    ticket_id = logic.create_ticket(message.from_user.id, message.text, 'tech')
    bot.send_message(
        message.chat.id,
        f'✅ Обращение #{ticket_id} создано для программистов!\n'
        f'Проблема: {message.text[:100]}...\n\n'
        'Специалист свяжется в рабочее время.',
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['order'])
def order_command(message):
    msg = bot.send_message(
        message.chat.id,
        'Опишите проблему с заказом или товаром:',
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, process_order_problem)

def process_order_problem(message):
    ticket_id = logic.create_ticket(message.from_user.id, message.text, 'sales')
    bot.send_message(
        message.chat.id,
        f'✅ Обращение #{ticket_id} создано для отдела продаж!\n'
        f'Проблема: {message.text[:100]}...\n\n'
        'Менеджер свяжется в рабочее время.',
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['tickets'])
def tickets_command(message):
    tickets_info = logic.get_user_tickets_info(message.from_user.id)
    bot.send_message(
        message.chat.id,
        tickets_info if tickets_info else 'У вас нет обращений.',
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['contact'])
def contact_command(message):
    bot.send_message(
        message.chat.id,
        '📞 Контакты поддержки:\n\n'
        'Email: support@продаемвсе.ру\n'
        'Телефон: 8-800-XXX-XX-XX\n'
        'Часы работы: Пн-Пт 9:00-18:00\n\n'
        'По срочным вопросам создавайте обращения через /tech или /order',
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text
    
    if text == '❓ FAQ':
        faq_command(message)
    elif text == '👨‍💻 Тех.проблемы':
        tech_command(message)
    elif text == '📦 Проблемы с заказом':
        order_command(message)
    elif text == '📞 Контакты':
        contact_command(message)
    elif text == '📋 Мои обращения':
        tickets_command(message)
    else:
        faq_answer = logic.check_faq(text)
        if faq_answer:
            bot.send_message(message.chat.id, faq_answer, reply_markup=main_menu())
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("👨‍💻 Техпроблемы", callback_data="create_tech")
            btn2 = types.InlineKeyboardButton("📦 Проблемы с заказом", callback_data="create_sales")
            markup.add(btn1, btn2)
            
            bot.send_message(
                message.chat.id,
                'Не нашел ответ. Создать обращение к специалистам?',
                reply_markup=markup
            )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith('faq_'):
        import database
        
        topic_map = {
            'faq_order': database.get_faq_answer('заказ оформить'),
            'faq_status': database.get_faq_answer('статус заказ'),
            'faq_cancel': database.get_faq_answer('отменить заказ'),
            'faq_damaged': database.get_faq_answer('товар поврежден'),
            'faq_support': database.get_faq_answer('техподдержка связь'),
            'faq_delivery': database.get_faq_answer('доставка информация'),
            'faq_payment': database.get_faq_answer('оплата способ'),
            'faq_return': database.get_faq_answer('возврат')
        }
        
        answer = topic_map.get(call.data, 'Информация не найдена')
        bot.send_message(call.message.chat.id, answer, reply_markup=main_menu())
    
    elif call.data == 'create_tech':
        msg = bot.send_message(
            call.message.chat.id, 
            'Опишите техническую проблему:',
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(msg, process_tech_problem)
    
    elif call.data == 'create_sales':
        msg = bot.send_message(
            call.message.chat.id, 
            'Опишите проблему с заказом:',
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(msg, process_order_problem)

if __name__ == '__main__':
    print('Оно вроде запустилось (но это нэ точно)')
    bot.polling(none_stop=True)