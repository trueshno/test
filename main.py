import sqlite3
import telebot

# Подключение к базе данных
conn = sqlite3.connect('db/database.db')
cursor = conn.cursor()

# Создание экземпляра бота
bot = telebot.TeleBot('6620987116:AAGYKX-C3q2oMi-gY2oHc9yPVRlBRt5A1Xw')

# Функция для получения случайного вопроса из базы данных
def get_random_question():
    cursor.execute('SELECT question FROM test ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()[0]
    return question

# Функция для рассчета результата на основе ответов пользователя
def calculate_result(answers):
    # Здесь вы можете добавить логику для рассчета результата на основе ответов
    # В данном примере просто суммируем значения ответов
    result = sum(answers)
    return result

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для математической модели.")

# Обработчик сообщений с ответами на вопросы
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id

    if 'answers' not in bot.data:
        bot.data['answers'] = []

    try:
        answer = int(message.text)  # Предполагаем, что пользователь отвечает числом
        bot.data['answers'].append(answer)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите число в качестве ответа.")

    # Получаем новый вопрос из базы данных
    question = get_random_question()

    # Если получены все ответы, рассчитываем результат
    if len(bot.data['answers']) >= 5:
        result = calculate_result(bot.data['answers'])
        bot.send_message(chat_id, "Результат: {}".format(result))
        bot.data['answers'] = []  # Сбрасываем ответы для следующего набора вопросов
    else:
        # Отправляем новый вопрос пользователю
        bot.send_message(chat_id, "Следующий вопрос: {}".format(question))

# Обработчик команды /test
@bot.message_handler(commands=['test'])
def handle_test(message):
    chat_id = message.chat.id
    bot.data['answers'] = []  # Сбрасываем ответы для нового набора вопросов
    question = get_random_question()
    bot.send_message(chat_id, "Начинаем тест! Первый вопрос: {}".format(question))

# Главная функция, запускающая бота
def main():
    bot.polling()

if __name__ == '__main__':
    main()