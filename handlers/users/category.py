from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@dp.message_handler(state=Shop.category)
async def get_cat(message: types.Message, state: FSMContext):
    
    cat_id = db.product_by_cat_id(title=message.text)
    await state.update_data(
        {"cat_id" : cat_id, 'catigoriya': message.text}
    )
    products = db.get_praduct_cat_id(cat_id=cat_id)
    prod = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    for p in products:
        prod.insert(KeyboardButton(text=str(p[0])))
    prod.insert(KeyboardButton(text="Orqaga🔙"))  
    await message.answer(f"{message.text} <i>katigoryasi dagi maxsulotlar</i> 🤑", reply_markup=prod, parse_mode="html")
    await Shop.next()         
