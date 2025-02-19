
# python3 -m venv my_venv
# source env/bin/activate
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from collections import defaultdict
from random import randint
from pdf import generate as generate_files

import generators.info
import generators.info.EGE14
import generators.info.systems
import generators.math
import generators.math.equations
import generators.math.progression

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = "6802426286:AAEQehlx2gzHrzNm95wfQI1OT8qL7GY32Wc"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

user_data = defaultdict(lambda: {
    "selected_tasks": [],
    "current_path": []
})
import generators
# MENU = {
#     "subjects": {
#         "computer_science": "💻 Computer Science",
#         "mathematics": "📚 Mathematics"
#     },
#     "topics": {
#         "computer_science": {
#             "ege14": "📊 EGE14",
#             "systems": "⚙️ Systems"
#         },
#         "mathematics": {
#             "equations": "📏 Equations",
#             "progression": "📈 Progression"
#         }
#     },
#     "tasks": {
#         "computer_science": {
#             "ege14": {"diff1": {"name": "Difficulty 1", "gen": lambda: generators.inf.EGE14.type1(1)},
#                       "diff2": {"name": "Difficulty 2", "gen": lambda: generators.inf.EGE14.type1(2)}},
#             "systems": {"diff1": {"name": "Difficulty 1", "gen": lambda: generators.inf.systems.convertions(1)},
#                         "diff2": {"name": "Difficulty 2", "gen": lambda: generators.inf.systems.convertions(2)},
#                         "diff3": {"name": "Difficulty 3", "gen": lambda: generators.inf.systems.convertions(3)},
#                         "diff4": {"name": "Difficulty 4", "gen": lambda: generators.inf.systems.convertions(4)}}
#         },
#         "mathematics": {
#             "equations": {"linear": {"name": "Linear", "gen": lambda: generators.math.equations.equation_line(randint(5,10),randint(1,4))},
#                           "square": {"name": "Square", "gen": lambda: generators.math.equations.equation_degree()},
#                           "biquadratic": {"name": "Biquadratic", "gen": lambda: generators.math.equations.equation_degree_bi()}},
#             "progression": {"arithmetic": {"name": "Arithmetic", "gen": lambda: generators.math.progression.arithmetic()},
#                             "geometric": {"name": "Geometric", "gen": lambda: generators.math.progression.geometric()}}
#         }
#     }
# }
MENU = {
    "subjects": {
        "computer_science": "💻 Информатика",
        "mathematics": "📚 Математика"
    },
    "topics": {
        "computer_science": {
            "ege14": "📊 EGE14",
            "systems": "⚙️ Системы счисления"
        },
        "mathematics": {
            "equations": "📏 Уравнения",
            "progression": "📈 Прогрессия"
        }
    },
    "tasks": {
        "computer_science": {
            "ege14": {"diff1": {"name": "Сложность1", "gen": lambda: generators.info.EGE14.type1(0)},
                      "diff2": {"name": "Сложность2", "gen": lambda: generators.info.EGE14.type1(1)}},
            "systems": {"diff1": {"name": "Сложность1", "gen": lambda: generators.info.systems.convertions(1)},
                        "diff2": {"name": "Сложность2", "gen": lambda: generators.info.systems.convertions(2)},
                        "diff3": {"name": "Сложность3", "gen": lambda: generators.info.systems.convertions(3)},
                        "diff4": {"name": "Сложность4", "gen": lambda: generators.info.systems.convertions(4)}}
        },
        "mathematics": {
            "equations": {"linear": {"name": "Линейные", "gen": lambda: generators.math.equations.equation_line(randint(5,10),randint(1,3))},
                          "square": {"name": "Квадратные", "gen": lambda: generators.math.equations.equation_degree()},
                          "biquadratic": {"name": "Биквадратные", "gen": lambda: generators.math.equations.equation_degree_bi()}},
            "progression": {"arithmetic": {"name": "Арифметическая", "gen": lambda: generators.math.progression.arithmetic()},
                            "geometric": {"name": "Геометрическая", "gen": lambda: generators.math.progression.geometric()}}
        }
    }
}
    # subject_name = MENU["subjects"][path[0]]
    # topic_name = MENU["topics"][task.split(":")[0]][task.split(":")[1]]
    # task_name = MENU["tasks"][task.split(":")[0]][task.split(":")[1]][task_id]
    # print(path, task_id)
    # user_data[user_id]["selected_tasks"].append(f"{subject_name} - {topic_name} - {task_name['name']}")
def format_selected(selected):
    # print(selected)
    selected = [f"{MENU["subjects"][task.split(":")[0]]} - {MENU["topics"][task.split(":")[0]][task.split(":")[1]]} - {MENU["tasks"][task.split(":")[0]][task.split(":")[1]][task.split(":")[2]]['name']}" for task in selected]
    return "\n".join([f"{i+1}. {task}" for i, task in enumerate(selected)]) or "No tasks selected"

def build_control_buttons(selected):
    builder = InlineKeyboardBuilder()
    if selected:
        # builder.row(InlineKeyboardButton(text="➖ Delete last", callback_data="remove_last"))
        # builder.row(InlineKeyboardButton(text="✅ Finish", callback_data="finish"))
        builder.row(InlineKeyboardButton(text="➖ Удалить последнее", callback_data="remove_last"))
        builder.row(InlineKeyboardButton(text="✅ Готово", callback_data="finish"))
    return builder

def build_number_keyboard():
    builder = InlineKeyboardBuilder()
    
    # Create 12 rows of 5 numbers each
    for row in range(12):
        for col in range(1, 6):
            number = row * 5 + col
            builder.add(InlineKeyboardButton(
                text=str(number),
                callback_data=f"number:{number}"
            ))
        builder.adjust(5)
    
    # Add back button
    # builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="number_back"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="number_back"))
    
    return builder.as_markup()

async def show_current_menu(message: types.Message, user_id: int):
    path = user_data[user_id]["current_path"]
    selected = user_data[user_id]["selected_tasks"]
    
    if len(path) == 0:
        await show_subjects(message, user_id)
    elif len(path) == 1:
        await show_topics(message, user_id, path[0])
    elif len(path) == 2:
        await show_tasks(message, user_id, path[0], path[1])

async def show_subjects(message: types.Message, user_id: int):
    builder = InlineKeyboardBuilder()
    for sid, sname in MENU["subjects"].items():
        builder.add(InlineKeyboardButton(text=sname, callback_data=f"subject:{sid}"))
    
    control = build_control_buttons(user_data[user_id]["selected_tasks"])
    if control._markup:
        builder.attach(control)
    
    # text = f"Selected tasks:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nChoose subject:"
    text = f"Выбранные задания:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nВыберите предмет:"
    # print(message.from_user.id, message.chat.id)
    if message.from_user.id==message.chat.id:
        await message.answer(text, reply_markup=builder.as_markup())
    else:
        await message.edit_text(text, reply_markup=builder.as_markup())

async def show_topics(message: types.Message, user_id: int, subject: str):
    builder = InlineKeyboardBuilder()
    for tid, tname in MENU["topics"][subject].items():
        builder.add(InlineKeyboardButton(text=tname, callback_data=f"topic:{tid}"))
    
    # builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    control = build_control_buttons(user_data[user_id]["selected_tasks"])
    if control._markup:
        builder.attach(control)
    
    # text = f"Selected tasks:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nChoose topic:"
    text = f"Выбранные задания:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nВыберите тему:"
    await message.edit_text(text, reply_markup=builder.as_markup())

async def show_tasks(message: types.Message, user_id: int, subject: str, topic: str):
    builder = InlineKeyboardBuilder()
    for task_id, task_info in MENU["tasks"][subject][topic].items():
        # print(task_info, user_data[user_id]['selected_tasks'])
        builder.add(InlineKeyboardButton(text=task_info["name"], callback_data=f"task:{task_id}"))
    
    # builder.row(InlineKeyboardButton(text="🔙 Back", callback_data="back"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back"))
    control = build_control_buttons(user_data[user_id]["selected_tasks"])
    if control._markup:
        builder.attach(control)
    
    # text = f"Selected tasks:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nChoose task type:"
    text = f"Выбранные задания:\n{format_selected(user_data[user_id]['selected_tasks'])}\n\nВыберите тип задания:"
    await message.edit_text(text, reply_markup=builder.as_markup())

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, который поможет тебе в создании заданий!\nпо команде /create появится окно с созданием твоего варианта.")

@dp.message(Command('create'))
async def cmd_create(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id].clear()
    user_data[user_id] = {"selected_tasks": [], "current_path": []}
    await show_subjects(message, user_id)

@dp.callback_query(F.data.startswith("subject:"))
async def select_subject(callback: CallbackQuery):
    user_id = callback.from_user.id
    subject = callback.data.split(":")[1]
    user_data[user_id]["current_path"] = [subject]
    await show_topics(callback.message, user_id, subject)

@dp.callback_query(F.data.startswith("topic:"))
async def select_topic(callback: CallbackQuery):
    user_id = callback.from_user.id
    topic = callback.data.split(":")[1]
    user_data[user_id]["current_path"].append(topic)
    subject = user_data[user_id]["current_path"][0]
    await show_tasks(callback.message, user_id, subject, topic)

@dp.callback_query(F.data.startswith("task:"))
async def select_task(callback: CallbackQuery):
    user_id = callback.from_user.id
    path = user_data[user_id]["current_path"]
    task_id = callback.data.split(":")[1]
    # subject_name = MENU["subjects"][path[0]]
    # topic_name = MENU["topics"][path[0]][path[1]]
    # task_name = MENU["tasks"][path[0]][path[1]][task_id]
    # print(path, task_id)
    # user_data[user_id]["selected_tasks"].append(f"{subject_name} - {topic_name} - {task_name['name']}")
    user_data[user_id]["selected_tasks"].append(f"{path[0]}:{path[1]}:{task_id}")
    # user_data[user_id]["current_path"] = []
    # MENU["tasks"][subject][topic]
    # print(path)
    await show_tasks(callback.message, user_id, path[0], path[1])

@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    path = user_data[user_id]["current_path"]
    
    if len(path) > 0:
        user_data[user_id]["current_path"].pop()
    
    await show_current_menu(callback.message, user_id)

@dp.callback_query(F.data == "remove_last")
async def remove_last_task(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_data[user_id]["selected_tasks"]:
        user_data[user_id]["selected_tasks"].pop()
    await show_current_menu(callback.message, user_id)

@dp.callback_query(F.data == "finish")
async def finish_selection(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        # "Select number of options:",
        "Выберите количество вариантов:",
        reply_markup=build_number_keyboard()
    )

@dp.callback_query(F.data.startswith("number:"))
async def handle_number_selection(callback: CallbackQuery):
    user_id = callback.from_user.id
    number = int(callback.data.split(":")[1])
    
    selected = user_data[user_id]["selected_tasks"]
    # print(selected)
    response = (
        # f"Final selection:\n{format_selected(selected)}"
        # f"\n\nNumber of options: {number}"
        f"Выбранные задания:\n{format_selected(selected)}"
        f"\n\nКоличество вариантов: {number}"
    )
    await callback.message.edit_text(response)

    tasks = [[MENU["tasks"][task.split(":")[0]][task.split(":")[1]][task.split(":")[2]]['gen']() for task in selected] for n in range(number)]
    tasks_pdf, answers_pdf = generate_files(tasks)
    tasks_file = BufferedInputFile(tasks_pdf, filename="tasks.pdf")
    answers_file = BufferedInputFile(answers_pdf, filename="answers.pdf")
    await callback.message.reply_document(tasks_file)
    await callback.message.reply_document(answers_file)
    user_data[user_id].clear()
    await callback.answer()

@dp.callback_query(F.data == "number_back")
async def handle_number_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    await show_current_menu(callback.message, user_id)
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))