from cgitb import text
from os import stat
import data
from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from aiogram.dispatcher import FSMContext
from keyboards.default.cats import all_cats
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message_handler(text='Orqaga🔙', state=Shop.praduct)
async def home(message: types.Message):
    await message.answer("Asosiy sahifadasiz kerakli katigoryani tanlang", reply_markup=all_cats)
    await Shop.category.set()

@dp.callback_query_handler(text='back', state=Shop.amount)
async def gwt2_products(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data=await state.get_data()
    cat_id = data.get('cat_id')
    catigoriya = data.get('catigoriya')
    products = db.get_praduct_cat_id(cat_id=cat_id)
    prod = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    for p in products:
        prod.insert(KeyboardButton(text=str(p[0])))
    prod.insert(KeyboardButton(text="Orqaga🔙"))  
    await call.message.answer(f"{catigoriya} <i>katigoryasi dagi maxsulotlar</i> 🤑", reply_markup=prod, parse_mode="html")
    await Shop.praduct.set()

@dp.callback_query_handler(text='back', state=Shop.delete)
async def main_m(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Asosiy sahifadasiz kerakli katigoryani tanlang", reply_markup=all_cats)
    await Shop.category.set()

@dp.callback_query_handler(text='main', state=Shop.amount)
async def main(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Asosiy sahifadasiz kerakli katigoryani tanlang", reply_markup=all_cats)
    await Shop.category.set()



