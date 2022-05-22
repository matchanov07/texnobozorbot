from subprocess import call
from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message_handler(state=Shop.category, text="🛒Savat")
async def get_product(message: types.Message):
    cart = db.get_current_products(tg_id=str(message.from_user.id))
    all = InlineKeyboardMarkup(row_width=1)
    if len(cart) !=0:
        msg = "Sizning Savatingizda: \n\n"
        for i in cart:
            msg += f"{i[2]} ✖ {i[-1]} = {int(i[-1]) * int(i[-2])} so'm\n" 
            all.insert(InlineKeyboardButton(text=f"❌ {i[2]} ❌", callback_data=f"{i[2]}:{i[1]}"))
        all.insert(InlineKeyboardButton(text='♻Boshatish♻', callback_data=('clean')))
        all.insert(InlineKeyboardButton(text='✍️Buyurtma berish✍️', callback_data='order'))
    else:
        msg= f"**Hozirda sizning savatinggiz bosh***\nUni toldirish uchun pastdagi tugmani bosing\n     \t    👇👇👇👇👇👇👇👇"
    all.add(InlineKeyboardButton(text='⏪Orqaga', callback_data='back'))
    await message.answer(msg, reply_markup=all)
    await Shop.delete.set()

@dp.callback_query_handler(text='cart', state=Shop.amount)
async def get_cart(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get('user_id')
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
    await call.message.answer(msg, reply_markup=all)
    await Shop.delete.set()