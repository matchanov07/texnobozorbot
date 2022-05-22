from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db



all_cats = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

cats = db.select_all_cats()
for cat in cats:
    cat_id= db.product_by_cat_id(title=cat[1])
    products=db.get_praduct_cat_id(cat_id=cat_id)
    if len(products) != 0:
        all_cats.insert(KeyboardButton(text=cat[1]))

all_cats.add(KeyboardButton(text="🛒Savat"))