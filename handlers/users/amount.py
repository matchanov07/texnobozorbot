from keyboards.default.cats import all_cats
from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(state=Shop.amount)
async def get_amount(call: types.CallbackQuery, state: FSMContext):
    amuount=call.data
    data = await state.get_data()
    title = data.get('title')
    price = data.get('price')
    user_id = data.get('user_id')
    await call.answer(f"{amuount} ta {title} Savatga qoshildi", show_alert=True) 
    await call.message.answer("Asosiy sahifa",parse_mode="html",reply_markup=all_cats)
    db.add_product_cart(tg_id=user_id, title=title, price=price, amuount=amuount)
    await call.message.delete()
    await Shop.category.set()