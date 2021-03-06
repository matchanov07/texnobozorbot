from loader import dp,bot, db
from aiogram import types
from states.praduct import Shop
# from aiogram.dispatcher import FSMContext
from data.products import user_order
from data.products import FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING
from data.config import ADMINS


@dp.callback_query_handler(text='order', state=Shop.delete)
async def get_invoice(call: types.CallbackQuery):
    invoice = user_order(tg_id=call.from_user.id)
    cart = db.get_current_products(tg_id=str(call.message.from_user.id))
    await call.message.delete()
    await bot.send_invoice(chat_id=call.from_user.id, **invoice.generate_invoice(), payload="payload:products")
    await call.answer("CHek jonatildi✅")
    await Shop.category.set()

@dp.shipping_query_handler(state=Shop.delete)
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib bera olmaymiz")
    elif query.shipping_address.city.lower() == "urganch":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)    
    await Shop.category.set()


@dp.pre_checkout_query_handler(state=Shop.delete)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!")
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}" )   
    await Shop.category.set()               