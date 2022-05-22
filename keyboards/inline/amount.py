from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


number = InlineKeyboardMarkup()
for i in range(1, 10):
    number.insert(InlineKeyboardButton(text=f"+{i}", callback_data=(str(i))))
number.insert(InlineKeyboardButton(text="🔙Orqaga", callback_data=("back")))
number.insert(InlineKeyboardButton(text="🏡Asosiy sahifa ", callback_data=("main")))
number.add(InlineKeyboardButton(text="🛒Savat", callback_data=("cart")))
 