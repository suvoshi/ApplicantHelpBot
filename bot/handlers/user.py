from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from bot.__main__ import dp, bot
from bot.messages import general

from bot.services.edu_db import edu_sql
from bot.services.users_db import users_sql

# set CallbackData for all types
city_callback = CallbackData("city", "id_city")
HI_callback = CallbackData("HI", "id_HI")
program_callback = CallbackData("program", "id_program")
type_callback = CallbackData("type", "id_type", "id_HI")
subtype_callback = CallbackData("subtype", "id_subtype", "id_HI")

HIs_callback = CallbackData("HIs", "id_city")
programs_callback = CallbackData("programs", "id_HI")


@dp.message_handler(commands=["start"])
async def start(message: Message):
    result = users_sql.select(message.chat.id)

    if result == []:
        users_sql.insert(message.chat.id, "ok")
    else:
        users_sql.update(message.chat.id, "ok")

    await message.answer(general.start_mes)


@dp.message_handler(commands=["help"])
async def help(message: Message):
    await message.answer(general.help_mes, parse_mode="html")


@dp.message_handler(commands=["search_city"])
async def search_city(message: Message):
    users_sql.update(message.chat.id, "search_city")

    await message.answer(general.search_city_mes)


@dp.message_handler(commands=["search_HI"])
async def search_HI(message: Message):
    users_sql.update(message.chat.id, "search_HI")

    await message.answer(general.search_HI_mes)


@dp.message_handler(commands=["search_program"])
async def search_program(message: Message):
    users_sql.update(message.chat.id, "search_program")

    await message.answer(general.search_program_mes)


@dp.message_handler(commands=["types"])
async def types(message: Message, id_HI=0):
    keyboard = InlineKeyboardMarkup(row_width=1)

    result = edu_sql.select("Type", "Type.id > 0")
    for type in result:
        callback = type_callback.new(id_type=id, id_HI=id_HI)
        button = InlineKeyboardButton(text=type.name, callback_data=callback)
        keyboard.add(button)

    if id_HI is None:
        await message.answer(
            general.search_types_0, parse_mode="html", reply_markup=keyboard
        )
    else:
        HI_name = edu_sql.select("HI", f"HI.id == {id_HI}")
        await message.answer(
            general.search_types.format(HI_name),
            parse_mode="html",
            reply_markup=keyboard,
        )


@dp.message_handler()
async def dialog(message: Message):
    user_session = users_sql.select(message.chat.id).session

    if user_session == "search_city":
        result = edu_sql.select("City", f"City.keywords.like('%{message.text}%')")

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            await message.answer(general.search_found_mes)
            for city in result:
                callback = city_callback.new(id_city=city.id)
                button = InlineKeyboardButton(text="К городу", callback_data=callback)
                keyboard = InlineKeyboardMarkup()
                keyboard.add(button)

                await message.answer(
                    general.search_found_city_mes.format(city.name, city.subject),
                    reply_markup=keyboard,
                )

    elif user_session == "search_HI":
        result = edu_sql.select("HI", f"HI.keywords.like('%{message.text}%')")

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            await message.answer(general.search_found_mes)
            for HI in result:
                city_name = edu_sql.select(
                    "City", f"City.id == {HI.id_city}", "one"
                ).name

                callback = HI_callback.new(id_HI=id)
                button = InlineKeyboardButton(text="К ВУЗу", callback_data=callback)
                keyboard = InlineKeyboardMarkup()
                keyboard.add(button)

                await message.answer(
                    general.search_found_HI_mes.format(HI.name, city_name),
                    reply_markup=keyboard,
                )

    elif user_session == "search_program":
        result = edu_sql.select("Program", f"Program.keywords.like('%{message.text}%')")

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            await message.answer(general.search_found_mes)
            for program in result:
                HI_name = edu_sql.select("HI", f"HI.id == {program.id_HI}", "one").name
                program_name = edu_sql.select(
                    "ProgramCode", f"ProgramCode.code == {program.code}", "one"
                ).name

                callback = program_callback.new(id_program=program.id)
                button = InlineKeyboardButton(
                    text="К направлению", callback_data=callback
                )
                keyboard = InlineKeyboardMarkup()
                keyboard.add(button)

                await message.answer(
                    general.search_found_program_mes.format(program_name, HI_name),
                    reply_markup=keyboard,
                )

    else:
        await message.answer(general.miss_mes)

    users_sql.update(message.chat.id, "ok")


@dp.callback_query_handler()
async def query_cb(call: CallbackQuery):
    receive_data = call.data.split(":")

    prefix = receive_data[0]
    args = receive_data[1:]

    if prefix == "city":
        city = edu_sql.select("City", f"City.id == {int(args[0])}", "one")

        callback = HIs_callback.new(id_city=city.id)
        button1 = InlineKeyboardButton(
            text="Посмотреть на карте",
            url="https://www.google.com/maps/place/" + city.name + " " + city.subject,
        )
        button2 = InlineKeyboardButton(text="Университеты", callback_data=callback)

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(button1, button2)

        await bot.send_message(
            call.message.chat.id,
            general.city_mes.format(city.name, city.subject, city.info),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "HI":
        HI = edu_sql.select("HI", f"HI.id == {int(args[0])}", "one")

        city_name = edu_sql.select("HI", f"HI.id == {int(args[0])}", "one").name

        callback = programs_callback.new(id_HI=HI.id)
        button1 = InlineKeyboardButton(
            text="Посмотреть на карте",
            url="https://www.google.com/maps/place/" + HI.name,
        )
        button2 = InlineKeyboardButton(text="Сайт", url=HI.url)
        button3 = InlineKeyboardButton(text="Направления", callback_data=callback)

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(button1, button2, button3)

        await bot.send_message(
            call.message.chat.id,
            general.HI_mes.format(HI.name, city_name, HI.info),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "program":
        program = edu_sql.select("Program", f"Program.id == {int(args[0])}", "one")

        HI_name = edu_sql.select("HI", f"HI.id == {program.id_HI}", "one").name

        program_name = edu_sql.select(
            "ProgramCode", f"ProgramCode.code == {program.code}", "one"
        ).name

        button = InlineKeyboardButton(text="Подробнее", url=program.url)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(button)

        await bot.send_message(
            call.message.chat.id,
            general.program_mes.format(
                program_name,
                HI_name,
                program.info,
                program.profiles,
                program.objs,
                program.form,
                program.budget_places,
                program.ed_cost,
                program.period,
                program.last_update,
            ),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "HIs":
        pass

    elif prefix == "programs":
        pass

    elif prefix == "type":
        pass

    elif prefix == "subtype":
        pass
