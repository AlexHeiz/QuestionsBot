# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import sqlite3
#

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
#
# questions = [
#     "Как вас зовут?",
#     "Сколько вам лет?",
#     "В каком городе вы живете?"
# ]
# answs = [
#     "Ваше имя",
#     "Ваш возраст",
#     "Ваш город"
# ]
#
# answers = {}
# async def start(update, context):
#     user_id = update.effective_user.id
#     logging.info(f'user_id: {user_id}')
#     answers[user_id] = {'question_index': 0, 'answers': []}
#     await update.message.reply_text("Привет! Я задам вам несколько вопросов.")
#     await ask_next_question(update, user_id)
#
#
#
#
#
# async def ask_next_question(update: Update, user_id: int):
#     question_index = answers[user_id]['question_index']
#     logging.info(f'question_index: {question_index}')
#     text = update.message.text
#     current_question_index = answers[user_id]['question_index']
#     if question_index < len(questions):
#         if current_question_index == 2:
#             age = 0
#             try:
#                 age = int(text)
#                 if not age or age <= 0 or None:
#                     await update.message.reply_text("Пожалуйста, введите честный возраст.")
#                     return
#                 answers[user_id]['answers'].append(age)
#             except ValueError or age < 0:
#                 await update.message.reply_text("Пожалуйста, введите число.")
#                 return
#                 # await update.message.reply_text(questions[question_index])
#                 # logging.info(f"USER ANSWER: {answers[user_id]['answers']}")
#         await update.message.reply_text(questions[question_index])
#         logging.info(f"USER ANSWER: {answers[user_id]['answers']}")
#     else:
#         await update.message.reply_text("Спасибо за ответы! Вот что вы мне рассказали:\n" +
#                                         "\n".join(f"{q}: {a}" for q, a in zip(answs, answers[user_id]['answers'])))
#         del answers[user_id]
#
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     if user_id not in answers:
#         await update.message.reply_text("Пожалуйста, начните с команды /start.")
#         return
#     answer = update.message.text
#     answers[user_id]['answers'].append(answer)
#     answers[user_id]['question_index'] += 1
#     await ask_next_question(update, user_id)
#
#
#
# async def unknown(update, context):
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text="Извините, данной команды я не понимаю :(")
#
#
# if __name__ == '__main__':
#     TOKEN = '7596343718:AAFjX9c5LUmaPgrXTBCUzrqUcXNvGJUG__0'
#     application = ApplicationBuilder().token(TOKEN).build()
#     start_handler = CommandHandler('start', start)
#     unknown_handler = MessageHandler(filters.COMMAND, unknown)
#     application.add_handler(start_handler)
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     application.add_handler(unknown_handler)
#     application.run_polling()
connect = sqlite3.connect('db.db')
cursor = connect.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users ("
#                "name TEXT,"
#                "age INT);")
# cursor.execute("INSERT INTO users (name, age) VALUES (?,"
#                " ?);",
#                ('aaa', 18))
# connect.commit()

cursor.execute("SELECT * FROM users")


data = cursor.fetchall()
for el in data:
    print(el)