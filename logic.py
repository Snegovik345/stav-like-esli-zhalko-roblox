import database

def main_menu():
    return None  

def check_faq(message):
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['оформить заказ', 'как заказать', 'сделать заказ']):
        return database.get_faq_answer('заказ оформить')
    elif any(word in message_lower for word in ['статус заказ', 'где мой заказ', 'отследить']):
        return database.get_faq_answer('статус заказ')
    elif any(word in message_lower for word in ['отменить заказ', 'отмена заказ']):
        return database.get_faq_answer('отменить заказ')
    elif any(word in message_lower for word in ['поврежден', 'сломан', 'брак', 'дефект']):
        return database.get_faq_answer('товар поврежден')
    elif any(word in message_lower for word in ['связаться', 'техподдержк', 'помощь']):
        return database.get_faq_answer('техподдержка связь')
    elif any(word in message_lower for word in ['доставк', 'доставить', 'срок доставк']):
        return database.get_faq_answer('доставка информация')
    elif any(word in message_lower for word in ['оплат', 'оплатить', 'способ оплат']):
        return database.get_faq_answer('оплата способ')
    elif 'возврат' in message_lower:
        return database.get_faq_answer('возврат')
    elif any(word in message_lower for word in ['сайт', 'не работ', 'ошибк']):
        return database.get_faq_answer('сайт проблема')
    elif any(word in message_lower for word in ['аккаунт', 'войти', 'пароль', 'логин']):
        return database.get_faq_answer('аккаунт вход')
    
    for word in message_lower.split():
        answer = database.get_faq_answer(word)
        if answer:
            return answer
    
    return None

def create_ticket(user_id, problem, department):
    return database.add_ticket(user_id, problem, department)

def get_department_name(dept_code):
    return {
        'tech': '👨‍💻 Программисты',
        'sales': '📦 Отдел продаж'
    }.get(dept_code, 'Неизвестный отдел')

def get_user_tickets_info(user_id):
    import sqlite3
    conn = sqlite3.connect('support.db')
    c = conn.cursor()
    c.execute('SELECT id, problem, department, status, created FROM tickets WHERE user_id = ? ORDER BY created DESC', (user_id,))
    tickets = c.fetchall()
    conn.close()
    
    if not tickets:
        return None
    
    result = "📋 Ваши обращения:\n\n"
    for ticket in tickets:
        ticket_id, problem, dept, status, created = ticket
        dept_name = get_department_name(dept)
        result += f"#{ticket_id} - {dept_name}\n"
        result += f"Проблема: {problem[:50]}...\n"
        result += f"Статус: {status} | {created[:10]}\n\n"
    
    return result