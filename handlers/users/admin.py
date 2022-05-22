import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.praduct import Category,Praduct
from aiogram.dispatcher import FSMContext
from datetime import date, datetime



@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       

@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")

@dp.message_handler(text="/cleancart", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_cart()
    await message.answer("Savat tozalandi!")

@dp.message_handler(commands=["category"], user_id=ADMINS)
async def add_category(message: types.Message):
    await message.answer("Qoshmoqchi bolgan katigorya nomini kiriting!")
    await Category.title.set()

@dp.message_handler(state=Category.title, user_id=ADMINS)
async def add_cat(message: types.Message, state: FSMContext):
    category = message.text
    await message.answer(f"{category} bazaga qoshildi")
    db.add_category_title(title=str(category))
    await state.finish()

@dp.message_handler(commands=["product"], user_id=ADMINS)
async def add_product(message: types.Message):
    await message.answer("Qoshmoqchi bolgan maxsulotingiz nomini kiriting!")
    await Praduct.title.set()

@dp.message_handler(state=Praduct.title, user_id = ADMINS)
async def get_name(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(
        {"title": title}
    )
    await message.answer("Batafsil malumot kiriting!")
    await Praduct.next()


@dp.message_handler(state=Praduct.description, user_id = ADMINS)
async def get_desc(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {"description": description}
    )
    await message.answer("Maxsulot narxini(so'mda) kiriting!")
    await Praduct.next()

@dp.message_handler(state=Praduct.price, user_id = ADMINS)
async def get_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(
        {"price": price}
    )
    await message.answer("Mahsulot rasmini yuboring")
    await Praduct.next()


@dp.message_handler(content_types=['photo'], state=Praduct.image, user_id = ADMINS)
async def get_image(message:types.Message, state: FSMContext):
    image = message.photo[-1].file_id
    await state.update_data(
        {'image': image}
    )
    cats = db.select_all_cats()
    s = ""
    for cat in cats:
        s += f"{cat[0]}. {cat[1]}\n"
    await message.answer(f"<b>Maxsulot categorya raqamini kiriting</b> \n\n{s}", parse_mode="html")
    await Praduct.next()

@dp.message_handler(state=Praduct.cat_id, user_id = ADMINS)
async def get_cat(message:types.Message, state: FSMContext):
    cat_id = int(message.text)
    data = await state.get_data()
    title = data.get('title')
    description = data.get("description")
    price = data.get("price")
    image = data.get("image")
    date1 = datetime.now()
    db.add_products(title=title, description=description, price=price, image=image, date=date1,cat_id=cat_id)
    await message.answer(f"{title} <i>mahsulotingiz muvaffaqiyatli qo'shildi!</i>", parse_mode="html")
    await state.finish()

@dp.message_handler(commands=["allpraduct"], user_id = ADMINS)
async def all_prods(message: types.Message):
        prods = db.select_all_prods()
        for prod in prods:
            await message.answer_photo(photo=prod[4], caption=f"<b>Maxsulot nomi: </b>{prod[1]}\n<b>Ma'lumot: </b> <i>{prod[2]}</i>\n\n<b>Narxi: </b>{prod[3]} so'm", parse_mode="html")
            