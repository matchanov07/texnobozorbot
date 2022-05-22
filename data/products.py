from aiogram import types
from aiogram.types import LabeledPrice
from utils.misc.product import Product
from loader import db


def user_order(tg_id):
    products = db.get_current_products(tg_id=tg_id )
    msg = "Sizning Savatingizda: \n\n"
    total_price = 0
    prices = []
    for i in products:
        total_price += int(i[-1]) * int(i[-2])
        msg += f"{i[2]} ✖ {i[-1]} = {int(i[-1]) * int(i[-2])} so'm\n" 
        prices.append( LabeledPrice(
                label=i[2],
                amount=i[-1] * i[-2]* 100, 
            ))
    buyurtma = Product(
        title="Tolov qilish uchun chek✅",
        description=msg,
        currency="UZS",
        prices=prices,
        start_parameter="create_invoice_products",
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
        is_flexible=True,
    )
    return buyurtma

macbook = Product(
    title="Ноутбук Apple MacBook Air 2020 (2560x1600, Apple M1 3.2 ГГц, RAM 8 ГБ, SSD 256 ГБ, Apple graphics 7-core)",
    description="To'lov qilish uchun quyidagi tugmani bosing.",
    currency="UZS",
    prices=[
        LabeledPrice(
            label='MacBook Air',
            amount=1160850000, # 11 608 500.00 so'm
        ),
        LabeledPrice(
            label='Yetkazib berish (7 kun)',
            amount=700000,# 20 000.00 so'm
        ),
    ],
    start_parameter="create_invoice_macbook",
    photo_url='https://bit.ly/3pYG7eV',
    photo_width=1280,
    photo_height=724,
    # photo_size=600,
    need_email=True,
    need_name=True,
    need_phone_number=True,
    need_shipping_address=True, # foydalanuvchi manzilini kiritishi shart
    is_flexible=True,
)

REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title="Fargo (3 kun)",
    prices=[
        LabeledPrice(
            'Maxsus quti', 800000),
        LabeledPrice(
            '3 ish kunida yetkazish', 4500000),
    ]
)
FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Express pochta (1 kun)',
    prices=[
        LabeledPrice(
            '1 kunda yetkazish', 70000000),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(id='pickup',
                                       title="Do'kondan olib ketish",
                                       prices=[
                                           LabeledPrice("Yetkazib berishsiz", -4500000)
                                       ])