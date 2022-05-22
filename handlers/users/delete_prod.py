from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.default.cats import all_cats

@dp.callback_query_handler(text='clean', state=Shop.delete)
async def clean_cart(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get('user_id')
    db.delete_products(tg_id=user_id)
    await call.answer('♻Savat boshatildi♻')
    await call.message.answer('Asosiy sahifadasiz kerakli kategoriyani tanlang', reply_markup=all_cats)
    await Shop.category.set()



@dp.callback_query_handler(state=Shop.delete)
async def delete_products(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    title, tg_id = call.data.split(":")
    db.delete_current_products(tg_id=tg_id, title=title)
    await call.answer(f"{title} Savatdan o'chirildi 🙁")
    all = InlineKeyboardMarkup(row_width=1)
    cart = db.get_current_products(tg_id=user_id)
    all = InlineKeyboardMarkup(row_width=1)
    if len(cart) !=0:
        msg = "Sizning Savatingizda: \n\n"
        for i in cart:
            msg += f"{i[2]} ✖ {i[-1]} = {int(i[-1]) * int(i[-2])} so'm\n" 
            all.insert(InlineKeyboardButton(text=f"❌ {i[2]} ❌", callback_data=f"{i[2]}:{i[1]}"))
        all.insert(InlineKeyboardButton(text='♻Boshatish♻', callback_data=('clean')))
        all.insert(InlineKeyboardButton(text='✍️Buyurtma berish✍️', callback_data='order'))
    else:
        msg= f"**Hozirda sizning savatinggiz bosh***\nUni toldirish uchun pastdagi tugmani bosing\n  \t       👇👇👇👇👇👇👇👇"
    all.add(InlineKeyboardButton(text='⏪Orqaga', callback_data='back'))    
    await call.message.edit_text(msg,reply_markup=all)
    await Shop.delete.set()