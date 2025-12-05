import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('support.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  problem TEXT,
                  department TEXT,
                  status TEXT DEFAULT 'open',
                  created TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS faq
                 (id INTEGER PRIMARY KEY,
                  keyword TEXT,
                  answer TEXT)''')
    
    faq_data = [
        ('заказ оформить', 'Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.'),
        ('статус заказ', 'Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.'),
        ('отменить заказ', 'Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.'),
        ('товар поврежден', 'При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.'),
        ('техподдержка связь', 'Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.'),
        ('доставка информация', 'Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.'),
        ('доставка срок', 'Доставка занимает 3-7 рабочих дней в зависимости от региона.'),
        ('оплата способ', 'Оплата картой, СБП или наличными при получении. При проблемах - напишите нам.'),
        ('возврат', 'Возврат в течение 14 дней с сохранением товарного вида и упаковки. Нужен чек.'),
        ('сайт проблема', 'Если сайт не работает, очистите кэш браузера или напишите программистам.'),
        ('аккаунт вход', 'Для восстановления пароля нажмите "Забыли пароль" на странице входа.')
    ]
    
    c.executemany('INSERT OR IGNORE INTO faq (keyword, answer) VALUES (?, ?)', faq_data)
    conn.commit()
    conn.close()

def add_ticket(user_id, problem, department):
    conn = sqlite3.connect('support.db')
    c = conn.cursor()
    c.execute('INSERT INTO tickets (user_id, problem, department, created) VALUES (?, ?, ?, ?)',
              (user_id, problem, department, datetime.now().isoformat()))
    conn.commit()
    ticket_id = c.lastrowid
    conn.close()
    return ticket_id

def get_faq_answer(keyword):
    conn = sqlite3.connect('support.db')
    c = conn.cursor()
    c.execute('SELECT answer FROM faq WHERE keyword LIKE ?', ('%' + keyword + '%',))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None