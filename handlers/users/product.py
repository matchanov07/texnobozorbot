from loader import dp, db 
from aiogram import types
from states.praduct import Shop
from keyboards.inline.amount import number
from aiogram.dispatcher import FSMContext

@dp.message_handler(state=Shop.praduct)
async def get_prod(message: types.Message, state: FSMContext):
    prod_name = message.text
    data = await state.get_data()
    cat_id = data.get("cat_id")
    info = db.get_product_title_id(title=prod_name, cat_id=cat_id)
    await state.update_data(
        {'title': str(info[1]), 'price': info[3], 'user_id': message.from_user.id}
    )
    await message.answer_photo(photo=info[4], caption=f"<b>{info[1]}</b><b>\n\n🤑Narxi: {info[3]} so'm\n📖Batafsil malumot: {info[2]}</b>", parse_mode="html", reply_markup=number)
    await Shop.next()