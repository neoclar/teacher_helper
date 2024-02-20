
import telebot
import tools.pdf as pdf
import os
# import re
import genenerators.Math.equations as equations
import genenerators.Math.progression as progression
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from tools.SQL import Database, conv_dict, conv_str, conv_list


token = '6802426286:AAGr8y4Il4T2K_1s3cnVTHj-4bPg2nvNPO0'

themes = {
    'Math': {'Уравнения': equations, 'Прогрессия': progression},
    'Info': {'Что-то': '', 'Ещё что-то': ''}
}

sub_names = {
    'Math': 'Математика',
    'Info': 'Информатика (в разработке)'
}

steps_down = {'theme': 'sub',  'vars': 'theme', 'tasks': 'vars'}

bot = telebot.TeleBot(token)
def easyopen(path):
    with open(path, 'rb') as misc:
        f=misc.read()
    return f

@bot.message_handler(commands=["start", "help"])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, '''Привет! Я бот, который поможет тебе в создании заданий!
по команде /create появится окно с созданием твоего варианта.''')

@bot.message_handler(commands=["create"])
def inline(message: telebot.types.Message):
    db = Database("database.db")
    # print(conv_list(db.get_tables()))
    db.delete_string('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={message.from_user.id})')
    db.add_string('users', user_id_out=message.from_user.id)
    markup = InlineKeyboardMarkup(row_width=1)
    db.execute(f"""INSERT OR IGNORE INTO tasks_common (user_id)
                  VALUES ((SELECT user_id_in FROM users WHERE user_id_out={message.from_user.id}))""")
    buttons = [InlineKeyboardButton(sub_names[subject], callback_data=f"['sub', '{subject}']" if sub_names[subject]!='Info' else 'ignore') for subject in list(themes)]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Выбери предмет', reply_markup=markup)

@bot.callback_query_handler(func=lambda c:True)
def inline(callback: telebot.types.CallbackQuery):
    db = Database("database.db")
    if eval(callback.data)[0]=='back':
        callback.data = eval(callback.data)[1]
        if callback.data == 'sub':
            db.delete_string('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
            db.add_string('users', user_id_out=callback.from_user.id)
            markup = InlineKeyboardMarkup(row_width=1)
            db.execute(f"""INSERT OR IGNORE INTO tasks_common (user_id)
                        VALUES ((SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id}))""")
            buttons = [InlineKeyboardButton(sub_names[subject], callback_data=f"['sub', '{subject}']" if sub_names[subject]!='Info' else 'ignore') for subject in list(themes)]
            markup.add(*buttons)
            bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)
            bot.send_message(callback.from_user.id, 'Выбери предмет', reply_markup=markup)
            return
        elif callback.data[0] == 'tasks':
            dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
            print(len(list(eval('{'+str(dict_data['tasks'][0])+'}'))))
            if len(list(eval('{'+str(dict_data['tasks'][0])+'}')))!=1:
                taskdb = eval('{'+str(dict_data['tasks'][0])+'}')
                del taskdb[max(list(taskdb))]
                db.rename_cell('tasks_common', tasks=str(taskdb)[1:-1], __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
            else:
                callback.data = ['theme', dict_data['theme'][0]]
                db.delete_cell('tasks_common', column='tasks', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
        bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.id)
        callback.message.id = bot.send_message(callback.from_user.id, 'Обрабатываю').id
        callback.data = str(callback.data)
    if eval(callback.data)[0]=='sub':
        sub = eval(callback.data)[1]
        db.rename_cell('tasks_common', sub=sub, __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
        # db.add_string('tasks_common', user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})', sub=sub)
        markup = InlineKeyboardMarkup(row_width=5)
        buttons = [InlineKeyboardButton(var, callback_data=f"['vars', '{var}']") for var in range(1, 26)]
        buttons.append(InlineKeyboardButton('Назад', callback_data=f"['back', 'sub']"))
        markup.add(*buttons)
        message = f'''
Предмет: {sub_names[eval(callback.data)[1]]}
Выбери количество вариантов
'''
        bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.id, text=message, reply_markup=markup)
    elif eval(callback.data)[0]=='vars':
        vars = eval(callback.data)[1]
        db.rename_cell('tasks_common', vars=vars, __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
        markup = InlineKeyboardMarkup(row_width=1)
        dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
        buttons = [InlineKeyboardButton(theme, callback_data=f"['theme', '{theme}']") for theme in list(themes[dict_data['sub'][0]])]
        buttons.append(InlineKeyboardButton('Назад', callback_data=f"'sub', '{dict_data['sub'][0]}'"))
        markup.add(*buttons)
        message = f'''
Предмет: {sub_names[str(dict_data['sub'])[2:-2]]}
Вариантов: {str(dict_data['vars'])[1:-1]}
Выбери тему
'''
        bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.id, text=message, reply_markup=markup)
    elif eval(callback.data)[0]=='theme':
        theme = eval(callback.data)[1]
        db.rename_cell('tasks_common', theme=theme, __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
        dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [InlineKeyboardButton(str(task), callback_data=f"['tasks', '{task}']") for task in list(eval(f"themes[{str(dict_data['sub'])[1:-1]}][{str(dict_data['theme'])[1:-1]}]").TASKLIB)]
        buttons.append(InlineKeyboardButton('Назад', callback_data=f"'vars', {dict_data['vars'][0]}"))
        markup.add(*buttons)
        dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
        message = f'''
Предмет: {sub_names[str(dict_data['sub'])[2:-2]]}
Вариантов: {str(dict_data['vars'])[1:-1]}
Тема: {str(dict_data['theme'])[2:-2]}
Выбери первое задание
'''
        bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.id, text=message, reply_markup=markup)
    elif eval(callback.data)[0]=='tasks':
        task = eval(callback.data)[1]
        dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
        taskdb = eval('{'+str(dict_data['tasks'][0])+'}')
        # print(taskdb)
        # print(task, task!='back')
        if task!='back':
            if taskdb=={None}:
                db.rename_cell('tasks_common', tasks=f"1:'{task}'", __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
            else:
                db.rename_cell('tasks_common', tasks=f"{str(taskdb)[1:-1]},{max(list(taskdb))+1}:'{task}'", __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})')
            dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
            taskdb = eval('{'+str(dict_data['tasks'][0])+'}')
        # print(dict_data)
        # if dict_data['vars']>max(list(taskdb)):
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [InlineKeyboardButton(str(task), callback_data=f"['tasks', '{task}']") for task in list(eval(f"themes[{str(dict_data['sub'])[1:-1]}][{str(dict_data['theme'])[1:-1]}]").TASKLIB)]
        buttons.append(InlineKeyboardButton('Убрать последнее задание' if len(list(taskdb))!=0 else 'Назад', callback_data=f"['back', ['tasks', 'back']]"))
        buttons.append(InlineKeyboardButton('Готово', callback_data="['end']"))
        markup.add(*buttons)
        message = f'''
Предмет: {sub_names[str(dict_data['sub'])[2:-2]]}
Вариантов: {str(dict_data['vars'])[1:-1]}
Тема: {str(dict_data['theme'])[2:-2]}{str([f"""
Задание {num}: {task}""" for num, task in zip(taskdb.keys(), taskdb.values())]+['' if taskdb!={None} or task=='back' else f"""
Задание 1: {task}"""])}
Выбери задание или нажми "Готово"
'''.replace('\\n', '\n').replace("['", '').replace("']", '').replace("', '", '')

# Задание {num}: {task}""" for num, task in zip(taskdb.keys(), taskdb.values())]+[f"""
# Задание {max(taskdb.keys())+1}: {task}"""] if taskdb!={} or task=='back' else f"""
# Задание 1: {task}""")}

        bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.id, text=message, reply_markup=markup)
    elif eval(callback.data)[0]=='end':
        dict_data = conv_dict(db.get_all_data_filter('tasks_common', __i__user_id=f'(SELECT user_id_in FROM users WHERE user_id_out={callback.from_user.id})'))
        module = themes[dict_data['sub'][0]][dict_data['theme'][0]]
        mod_tasks = module.TASKLIB
        taskdb = eval('{'+str(dict_data['tasks'][0])+'}')
        tasks = [mod_tasks[task_name] for task_name in taskdb.values()]
        html_task, html_answer = send_pdf(tasks, int(dict_data['vars'][0]))
        
        context = {'sub': sub_names[dict_data['sub'][0]], 'theme': dict_data['theme'][0], 'tasks': html_task}
        file_task = pdf.create(context, 'files/pdfgens/tasks', 'files/templates/task.html')
        bot.send_document(callback.from_user.id, easyopen(file_task), visible_file_name='Задания.pdf')
        os.remove(file_task)
        context = {'sub': sub_names[dict_data['sub'][0]], 'theme': dict_data['theme'][0], 'tasks': html_answer}
        file_answer = pdf.create(context, 'files/pdfgens/answers', 'files/templates/answer.html')
        bot.send_document(callback.from_user.id, easyopen(file_answer), visible_file_name='Ответы.pdf')
        os.remove(file_answer)
        # bot.send_message(callback.from_user.id, 'message', reply_markup=InlineKeyboardMarkup(row_width=5).add(InlineKeyboardButton('var', callback_data='1'*64))) # Больше 64 выходит ошибка

def send_pdf(tasks, vars):
    html_task_vars = []
    html_answer_vars = []
    for vari in range(1, vars+1):
        html_task = []
        html_answer = []
        previous_tasks = []
        for i, _task in zip(range(1, len(tasks)+1), tasks):
            if isinstance(_task, str):
                task = eval(_task)
            else:
                task = _task()
            while task in previous_tasks:
                if isinstance(_task, str):
                    task = eval(_task)
                else:
                    task = _task()
            previous_tasks.append(task)
            if _task.__globals__['TASKDES'][_task]!='':
                html_task.append(f'''
                <h4 style="color: #2e6c80;">{i}. {_task.__globals__['TASKDES'][_task]}</h4>
                <p style="padding-left: 25px; font-size: 20px;"><strong>{task[0]}</strong></p>
                <p font-size: 20px;><strong>Ответ: ____________________</strong></p>''')
            else:
                html_task.append(f'''
                <h4> <span style="color: #2e6c80;">{i}.</span> {task[0]}</h4>
                <p font-size: 20px;><strong>Ответ: ____________________</strong></p>''')
            html_answer.append(f'''
            <h4 style="color: #2e6c80;"><strong>{i}.</h4> Ответ: {task[1]}</strong>''')
        html_task_vars.append([vari, html_task])
        html_answer_vars.append([vari, html_answer])
    # print(html_task)
    return html_task_vars, html_answer_vars

@bot.message_handler(content_types=['text'])
def react_text(message):
    bot.send_message(message.chat.id, 'Я не знаю, что тебе ответить...')



bot.polling()



# @bot.message_handler(commands=['start', 'help'])
# # InputTextMessageContent
# def choice_subject(message):
#     markup = InlineKeyboardMarkup(row_width=1)
#     subjects = ['Math', 'russ']

#     buttons = [InlineKeyboardButton(subject, callback_data=subject) for subject in subjects]
#     markup.add(*buttons)
#     bot.send_message(message.chat.id, 'Выбери предмет', reply_markup=markup)
#     # bot.register_next_step_handler(message, choice_count_variants)

# def get_subject(message):
#     markup = InlineKeyboardMarkup(row_width=1)
#     subjects = ['Math', 'russ']
#     buttons = [InlineKeyboardButton(subject, callback_data=subject) for subject in subjects]
#     markup.add(*buttons)
#     bot.send_message(message.chat.id, 'Выбери предмет', reply_markup=markup)
#     bot.register_next_step_handler(message, choice_count_variants)


# def choice_count_variants(message):
#     markup = InlineKeyboardMarkup(row_width=3)
#     buttons = [InlineKeyboardButton(subject, callback_data=subject) for subject in range(9)]
#     markup.add(*buttons)
#     bot.send_message(message.chat.id, 'Выбери количество вариантов', reply_markup=markup)
#     bot.register_next_step_handler(message, choice_count_variants)

# def choice_count_variants(message):
#     markup = InlineKeyboardMarkup(row_width=3)
#     buttons = [InlineKeyboardButton(subject, callback_data=subject) for subject in range(9)]
#     markup.add(*buttons)
#     bot.send_message(message.chat.id, 'Выбери количество заданий', reply_markup=markup)
#     bot.register_next_step_handler(message, function)


# @bot.callback_query_handler(func=lambda call:True)
# def inline_handler(callback_query):
#     print(callback_query)
#     choice_count_variants(callback_query)
