from turtle import title
from unicodedata import category
from aiogram.dispatcher.filters.state import StatesGroup, State

class Category(StatesGroup):
    title = State()
    

class Praduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    image = State()
    cat_id = State()

class Shop(StatesGroup):
    category = State()
    praduct = State()
    amount = State()
    delete = State()
    