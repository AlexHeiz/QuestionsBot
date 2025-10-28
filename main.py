import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import sqlite3
import time
from dotenv import load_dotenv
import os

current_time = time.time()
local_time = time.localtime(current_time)
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
connect = sqlite3.connect('db.db')
cursor = connect.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (chat_ID INT,"
    "time TEXT,"
    "q0 TEXT, w0 TEXT,"
    "q1 TEXT, w1 TEXT,"
    "q2 TEXT, w2 TEXT);")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

questions = [
    "Как вас зовут?",
    "Сколько вам лет?",
    "В каком городе вы живете?"
]
answs = [
    "Ваше имя",
    "Ваш возраст",
    "Ваш город"
]

answers = {}
async def start(update, context):
    user_id = update.effective_user.id
    cursor.execute("SELECT * FROM users WHERE chat_ID = ?",
                   (user_id,))
    record = cursor.fetchone()
    if record:
        cursor.execute("UPDATE users SET time = ? WHERE chat_ID = ?",
                       (formatted_time, user_id))
        connect.commit()
        logging.info(f"Обновлена запись для chat_id: {user_id}")
    else:
        cursor.execute("INSERT INTO users (chat_ID, time, q0, w0, q1, w1, q2, w2) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, formatted_time, '', '', '', '', '', ''))
        connect.commit()
        logging.info(f"Создана новая запись для chat_id: {user_id}")

    # Инициируем ответы пользователя
    answers[user_id] = {'question_index': 0, 'answers': []}
    await update.message.reply_text("Привет! Я задам вам несколько вопросов.")
    await ask_next_question(update, user_id)

# async def start(update, context):
#     user_id = update.effective_user.id
#     cursor.execute("INSERT INTO users (chat_ID, time, q0, w0, q1, w1, q2, w2) "
#                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, formatted_time,
#                                                        '', '', '', '', '', ''))
#     connect.commit()
#     logging.info(f'user_id: {user_id}')
#     answers[user_id] = {'question_index': 0, 'answers': []}
#     await update.message.reply_text("Привет! Я задам вам несколько вопросов.")
#     await ask_next_question(update, user_id)


async def ask_next_question(update: Update, user_id: int):
    question_index = answers[user_id]['question_index']

    logging.info(f'question_index: {question_index}')
    if question_index < len(questions):
        await update.message.reply_text(questions[question_index])
        logging.info(f"USER ANSWER: {answers[user_id]['answers']}")
    else:
        await update.message.reply_text("Спасибо за ответы! Вот что вы мне рассказали:\n" +
                                        "\n".join(f"{q}: {a}" for q, a in zip(answs, answers[user_id]['answers'])))

        del answers[user_id]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in answers:
        await update.message.reply_text("Пожалуйста, начните с команды /start.")
        return
    answer = update.message.text
    answers[user_id]['answers'].append(answer)
    print(f"q{answers[user_id]['question_index']}")
    print(f"a{answers[user_id]['question_index']}")
    print(f'{questions[answers[user_id]["question_index"]]}')
    print(answer)
    print(user_id)
    cursor.execute(f"UPDATE users SET q{answers[user_id]['question_index']} = ? WHERE chat_ID = ?",
                   (f'{questions[answers[user_id]["question_index"]]}', user_id))
    connect.commit()
    cursor.execute(f"UPDATE users SET w{answers[user_id]['question_index']} = ? WHERE chat_ID = ?",
                   (answer, user_id))

    connect.commit()
    answers[user_id]['question_index'] += 1
    await ask_next_question(update, user_id)


async def unknown(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Извините, данной команды я не понимаю :(")


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    application = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(unknown_handler)
    application.run_polling()
