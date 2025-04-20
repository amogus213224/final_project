from telebot import TeleBot
from config import API_TOKEN
from config import DATABASE
from logic import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(API_TOKEN)
hideBoard = types.ReplyKeyboardRemove() 
def get_data(num):
    
    conn = sqlite3.connect('data.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()
    # Запрос данных из нужного столбца
    if num == 0:
        cursor.execute("SELECT question FROM faq WHERE Is_Closed = 0")  # Укажите ваш столбец и таблицу
        rows = cursor.fetchall()
    elif num == 1:
        cursor.execute("SELECT question FROM faq WHERE Is_Closed > 0")  # Укажите ваш столбец и таблицу
        rows = cursor.fetchall()
    elif num == 2:
        cursor.execute("SELECT question FROM faq WHERE Is_Closed = 2")  # Укажите ваш столбец и таблицу
        rows = cursor.fetchall()
    # Преобразование данных в список
    data_list = [row[0] for row in rows]  # row[0] - это первый (и единственный) элемент каждой строки
    conn.close()
    return data_list

def get_answ(text):
    conn = sqlite3.connect('data.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()
    answer = cursor.execute("SELECT answer FROM faq WHERE question = ? and Is_Closed > 0", (text,))
    return answer

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("❓ Выбрать вопрос")
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! раз ты написал сюда, то скорее всего у тебя возник вопрос! выбери уже существующие вопросы или напиши /question, чтобы его отправить его сотруднику на рассмотрение!", reply_markup=markup)



@bot.message_handler(commands=['question'])
def handle_question(message):
        bot.send_message(message.chat.id, 'Напишите вопрос, который вы хотите задать')
        bot.register_next_step_handler(message, question)
def question(message):
        admin = manager2.admin_id()
        question = message.text
        user_id = message.chat.id
        manager2.add_user_answer(user_id,question)
        idi = manager2.get_id(question)
        bot.send_message(admin[0][0], f'Вопрос от @{message.from_user.username}:\n{question}\nid вопроса: {idi[0][0]}')
        bot.send_message(message.chat.id, f'Вопрос отправлен, ожидайте ответа🕛\nid вопроса: {idi[0][0]}')


@bot.message_handler(commands=['answer'])
def handle_answer(message):
       admins = manager2.admin_id()
       for i in admins:
              if i[0]==message.chat.id:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn = types.KeyboardButton("Выбрать из списка 📋")
                    markup.add(btn)
                    bot.send_message(message.chat.id, 'Отправьте айди вопроса на который вы хотите ответить или выберите вопросы из списка',reply_markup=markup)
                    bot.register_next_step_handler(message, answer)
def answer(message):
        ans = message.text
        if ans == 'Выбрать из списка 📋':
                data_list = get_data(0)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for item in data_list:
                        keyboard.add(types.KeyboardButton(item))
                bot.send_message(message.chat.id, "Выбери вопрос из списка ниже".format(message.from_user), reply_markup=keyboard)
                bot.register_next_step_handler(message, answer3)
              
        else:
                closed = manager2.is_closed(ans)
                if int(closed[0][0]) == 0:
                        all_id =  manager2.get_all_id()
                        for i in all_id:
                                if i[0]==int(ans):
                                        quest = manager2.get_question(int(ans))
                                        bot.send_message(message.chat.id, f'Вопрос #{ans}:\n{quest[0][0]} ')
                                        bot.send_message(message.chat.id, 'Отправьте ваш ответ на вопрос')
                                        bot.register_next_step_handler(message, answer2 , ans = ans)
                else:
                        bot.send_message(message.chat.id, 'На этот вопрос уже ответили❌')
def answer2(message,ans):
        ans2 = message.text
        user = manager2.get_user_id(int(ans))
        bot.send_message(user[0][0], f'Пришел ответ на вопрос с id:{ans}\n{ans2}')
        manager2.update_Closed(int(ans))
        manager2.update_answer(ans2,int(ans))
        bot.send_message(message.chat.id, 'Ответ успешно отправлен✅')

def answer3(message):
      ans = message.text
      ans = manager2.get_id(ans)
      closed = manager2.is_closed(ans[0][0])
      ans = ans[0][0]
      if int(closed[0][0]) == 0:
            all_id =  manager2.get_all_id()
            for i in all_id:
                  if i[0]==int(ans):
                        quest = manager2.get_question(int(ans))
                        bot.send_message(message.chat.id, f'Вопрос #{ans}:\n{quest[0][0]} ')
                        bot.send_message(message.chat.id, 'Отправьте ваш ответ на вопрос')
                        bot.register_next_step_handler(message, answer2 , ans = ans)
   


                     
              

       
@bot.message_handler(content_types=['text'])
def func(message):
    data_list = get_data(1)
    if(message.text == "❓ Выбрать вопрос"):
        data_list = get_data(2)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for item in data_list:
            keyboard.add(types.KeyboardButton(item))
        bot.send_message(message.chat.id, "Хорошо, {0.first_name}! Выбери вопрос ниже или задай свой".format(message.from_user), reply_markup=keyboard)
    elif message.text in data_list:
        answer = get_answ(message.text)
        bot.send_message(message.chat.id, answer)



if __name__ == '__main__':
     manager2 = Database_Manager(DATABASE)
     bot.polling(none_stop=True)