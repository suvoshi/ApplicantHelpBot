from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from bot.__main__ import dp, bot
from bot.messages import general

from bot.services.edu_db import edu_sql
from bot.services.users_db import users_sql

# set CallbackData for all types
city_callback = CallbackData("city", "id_city", "del_before", "del_after")
HI_callback = CallbackData("HI", "id_HI", "del_before", "del_after")
program_callback = CallbackData("program", "id_program", "del_before", "del_after")

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


@dp.message_handler(commands=["search_hi"])
async def search_HI(message: Message):
    users_sql.update(message.chat.id, "search_HI")

    await message.answer(general.search_HI_mes)


@dp.message_handler(commands=["search_program"])
async def search_program(message: Message):
    users_sql.update(message.chat.id, "search_program")

    await message.answer(general.search_program_mes)


@dp.message_handler()
async def dialog(message: Message):
    user_session = users_sql.select(message.chat.id).session

    if user_session == "search_city":
        result = edu_sql.select(
            "City", f"City.keywords.like('%{message.text.lower()}%')"
        )

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            if len(result) > 5:
                await message.answer(general.search_very_long_ans_mes)
            else:
                await message.answer(general.search_found_mes)

                ind = 0
                for city in result:
                    callback = city_callback.new(id_city=city.id, del_before=(ind + 1), del_after=(len(result[ind + 1:])))
                    button = InlineKeyboardButton(text="К городу", callback_data=callback)
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(button)

                    await message.answer(
                        general.search_found_city_mes.format(city.name, city.subject),
                        reply_markup=keyboard,
                        parse_mode="html",
                    )

                    ind += 1

    elif user_session == "search_HI":
        result = edu_sql.select("HI", f"HI.keywords.like('%{message.text.lower()}%')")

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            if len(result) > 5:
                await message.answer(general.search_very_long_ans_mes)
            else:
                await message.answer(general.search_found_mes)

                ind = 0
                for HI in result:
                    city_name = edu_sql.select(
                        "City", f"City.id == {HI.id_city}", "one"
                    ).name

                    callback = HI_callback.new(id_HI=HI.id, del_before=(ind + 1), del_after=(len(result[ind + 1:])))
                    button = InlineKeyboardButton(text="К вузу", callback_data=callback)
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(button)

                    await message.answer(
                        general.search_found_HI_mes.format(HI.name, city_name),
                        reply_markup=keyboard,
                        parse_mode="html",
                    )

                    ind += 1

    elif user_session == "search_program":
        result = edu_sql.select(
            "Program", f"Program.keywords.like('%{message.text.lower()}%')"
        )

        if result == []:
            await message.answer(general.search_not_found_mes)
        else:
            if len(result) > 5:
                await message.answer(general.search_very_long_ans_mes)
            else:
                await message.answer(general.search_found_mes)

                ind = 0
                for program in result:
                    HI_name = edu_sql.select("HI", f"HI.id == {program.id_HI}", "one").name
                    program_name = edu_sql.select(
                        "ProgramCode", f"ProgramCode.code == {program.code}", "one"
                    ).name

                    callback = program_callback.new(id_program=program.id, del_before=(ind + 1), del_after=(len(result[ind + 1:])))
                    button = InlineKeyboardButton(
                        text="К направлению", callback_data=callback
                    )
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(button)

                    await message.answer(
                        general.search_found_program_mes.format(program_name, HI_name),
                        reply_markup=keyboard,
                        parse_mode="html",
                    )

                    ind += 1

    else:
        await message.answer(general.miss_mes)

    users_sql.update(message.chat.id, "ok")


@dp.callback_query_handler()
async def query_cb(call: CallbackQuery):
    receive_data = call.data.split(":")

    prefix = receive_data[0]
    args = receive_data[1:]

    if prefix == "city":
        del_bef = (-1) * int(args[1])
        del_aft = int(args[2])

        for i in range(del_bef, del_aft + 1):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id + i))
        
        city = edu_sql.select("City", f"City.id == {int(args[0])}", "one")

        callback = HIs_callback.new(id_city=city.id)
        button1 = InlineKeyboardButton(
            text="Посмотреть на карте",
            url="https://www.google.com/maps/place/" + city.name + " " + city.subject,
        )
        button2 = InlineKeyboardButton(text="Вузы", callback_data=callback)

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(button1, button2)

        await bot.send_message(
            call.message.chat.id,
            general.city_mes.format(city.name, city.subject, city.info),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "HI":
        del_bef = (-1) * int(args[1])
        del_aft = int(args[2])

        for i in range(del_bef, del_aft + 1):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id + i))
        
        HI = edu_sql.select("HI", f"HI.id == {int(args[0])}", "one")

        city = edu_sql.select("City", f"City.id == {HI.id_city}", "one")

        callback3 = programs_callback.new(id_HI=HI.id)
        callback4 = city_callback.new(id_city=city.id, del_before=0, del_after=0)
        button1 = InlineKeyboardButton(
            text="Посмотреть на карте",
            url="https://www.google.com/maps/place/" + HI.name,
        )
        button2 = InlineKeyboardButton(text="Сайт", url=HI.url)
        button3 = InlineKeyboardButton(text="Направления", callback_data=callback3)
        button4 = InlineKeyboardButton(text="⬅️ К городу", callback_data=callback4)

        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(button1, button2, button3, button4)

        await bot.send_message(
            call.message.chat.id,
            general.HI_mes.format(HI.name, city.name, HI.info),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "program":
        del_bef = (-1) * int(args[1])
        del_aft = int(args[2])

        for i in range(del_bef, del_aft + 1):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=(call.message.message_id + i))
        
        program = edu_sql.select("Program", f"Program.id == {int(args[0])}", "one")

        HI_name = edu_sql.select("HI", f"HI.id == {program.id_HI}", "one").name

        program_name = edu_sql.select(
            "ProgramCode", f"ProgramCode.code == '{program.code}'", "one"
        ).name

        callback2 = HI_callback.new(id_HI=program.id_HI, del_before=0, del_after=0)

        button1 = InlineKeyboardButton(text="Подробнее", url=program.url)
        button2 = InlineKeyboardButton(text="⬅️ К вузу", callback_data=callback2)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(button1, button2)

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
                program.cost_ed,
                program.period,
                program.last_update,
            ),
            parse_mode="html",
            reply_markup=keyboard,
        )

    elif prefix == "HIs":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        city = edu_sql.select("City", f"City.id == {int(args[0])}", "one")

        result = edu_sql.select("HI", f"HI.id_city == {city.id}")

        await bot.send_message(call.message.chat.id, general.HIs_mes.format(city.name), parse_mode="html")
        
        if result == []:
            callback = city_callback.new(id_city=city.id, del_before=1, del_after=0)
            button = InlineKeyboardButton("⬅️ К городу", callback_data=callback)
            keyboard = InlineKeyboardMarkup()
            keyboard.add(button)

            await bot.send_message(call.message.chat.id, general.search_HIs_not_found_mes, reply_markup=keyboard)
        else:
            ind = 0
            for HI in result:
                keyboard = InlineKeyboardMarkup()
                callback = HI_callback.new(id_HI=HI.id, del_before=(ind + 1), del_after=(len(result[ind + 1:])))
                button = InlineKeyboardButton("К вузу", callback_data=callback)
                keyboard.add(button)

                if ind == len(result) - 1:
                    callback = city_callback.new(id_city=city.id, del_before=(ind + 1), del_after=0)
                    button = InlineKeyboardButton("⬅️ К городу", callback_data=callback)
                    keyboard.add(button)
                
                await bot.send_message(call.message.chat.id, general.search_found_HI_mes.format(HI.name, city.name), reply_markup=keyboard, parse_mode="html")

                ind += 1


    elif prefix == "programs":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        HI = edu_sql.select("HI", f"HI.id == {int(args[0])}", "one")

        result = edu_sql.select("Program", f"Program.id_HI == {int(args[0])}")

        await bot.send_message(call.message.chat.id, general.programs_mes.format(HI.name), parse_mode="html")

        if result == []:
            callback = program_callback.new(id_HI=HI.id, del_before=1, del_after=0)
            back_button = InlineKeyboardButton("⬅️ К вузу", callback_data=callback)
            keyboard = InlineKeyboardMarkup()
            keyboard.add(back_button)

            await bot.send_message(call.message.chat.id, general.search_programs_not_found_mes, reply_markup=keyboard)
        else:
            ind = 0
            for program in result:
                program_name = edu_sql.select("ProgramCode", f"ProgramCode.code == '{program.code}'", "one").name
                HI_name = edu_sql.select("HI", f"HI.id == {program.id_HI}", "one").name

                keyboard = InlineKeyboardMarkup()
                callback = program_callback.new(id_program=program.id, del_before=(ind + 1), del_after=(len(result[ind + 1:])))
                button = InlineKeyboardButton("К направлению", callback_data=callback)
                keyboard.add(button)

                if ind == len(result) - 1:
                    callback = HI_callback.new(id_HI=program.id_HI, del_before=(ind + 1), del_after=0)
                    button = InlineKeyboardButton("⬅️ К вузу", callback_data=callback)
                    keyboard.add(button)

                await bot.send_message(call.message.chat.id, general.search_found_program_mes.format(program_name, HI_name), reply_markup=keyboard, parse_mode="html")

                ind += 1
