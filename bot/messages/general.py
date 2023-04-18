emoji = {
    "city": "🏙️",
    "HI": "🏫",
    "program": "📚",
    "srch": "🔍",
    "compas": "🧭",
    "desc": "🔻",
    "subj": "📍",
    "back": "⬅️"
}

# base messages
start_mes = f"""
Приветствую!
Я - @AplicantHelpBot, ваш ассистент в поиске информации для поступающих.
Попробуйте узнать у меня что-нибудь {emoji['srch']}{emoji['compas']}

P.S. Если вы здесь в первый раз, то советую прочитать подсказки по использованию:
/help"""

help_mes = """
@ApplicantHelpBot: FAQ и Поддержка

<b>Как это работает?</b>

Интерфейс бота позволяет вам находить вузы и направления. Для реализации этих функций бот имеет следующие команды:
/search_city  -  Найдет город
/search_hi  -  Найдет вуз
/search_program  -  Найдет направление

После вызова каждой из этих команд, следуйте иструкциям для получения результата.

По остальным вопросам обращаться: <b>~ пока не добавлено ~</b>
"""

# search messages (which are working as dialogs with user)
search_found_mes = """По вашему запросу нашлось:"""
search_not_found_mes = """По вашему запросу ничего не найдено :("""
search_very_long_ans_mes = """Слишком обобщенный запрос.\nПопробуйте сузить круг поиска"""

search_HIs_not_found_mes = """Вузов не найдено :("""
search_programs_not_found_mes = """Направлений не найдено :("""

search_city_mes = """Хорошо, напишите название города"""
search_HI_mes = """Хорошо, напишите название вуза"""
search_program_mes = """Хорошо, напишите название направления"""

search_HIs_mes = f"""{emoji['city']} <b>Город:</b> {{}}\n<b>{emoji['HI']} Университеты{emoji['desc']}</b>"""

search_found_city_mes = (
    f"""<b>{emoji['city']} Город:</b> {{}}\n<b>{emoji['subj']} Субъект:</b> {{}}"""
)
search_found_HI_mes = (
    f"""<b>{emoji['HI']} Название:</b> {{}}\n<b>{emoji['city']} Город:</b> {{}}"""
)
search_found_program_mes = (
    f"""<b>{emoji['program']} Название:</b> {{}}\n<b>{emoji['HI']} Вуз:</b> {{}}"""
)

# answer messages (which are working with db)
city_mes = f"""
{emoji['city']} <b>Город:</b> {{}}
{emoji['subj']} <b>Субъект:</b> {{}}

<b>Описание города {emoji['desc']}</b>
{{}}
"""

HI_mes = f"""
{emoji['HI']} <b>Название:</b> {{}}
{emoji['city']} <b>Город:</b> {{}}

<b>Описание Вуза {emoji['desc']}</b>
{{}}
"""

program_mes = f"""
{emoji['program']} <b>Название:</b> {{}}
{emoji['HI']} <b>Университет:</b> {{}}

<b>Описание направления {emoji['desc']}</b>
{{}}

<b>Профили обучения:</b> {{}}

<b>Предметы для сдачи:</b>
{{}}

<b>Форма обучения:</b> {{}}

<b>Бюджетные места:</b> {{}}

<b>Стоимость обучения:</b> {{}}

<b>Время обучения:</b> {{}}

*Данные за {{}} год.
"""

HIs_mes = f"""
{emoji['city']} <b>Город:</b> {{}}
<b>Вузы</b>{emoji['desc']}
"""

programs_mes = f"""
{emoji['HI']} <b>Вуз:</b> {{}}
<b>Направления</b>{emoji['desc']}
"""

# other
miss_mes = """Простите, не понимаю вас."""
