from config_database import get_unique_categories, get_elements_by_category
from callbacks import CategoryCallback, ItemCallback, PurchaseCallback, PaymentCallback, AdminCallback, OrderCallback
from models import placeholders
from aiogram import types
from bot_config import trustedUser


categories = get_unique_categories()


def main_markup():
    buttons = [[types.KeyboardButton(text=text) for text in el] for el in placeholders['markups']['main_markup']]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, row_width=3)

    return keyboard


#postprod
def main_admin():
    buttons = [[types.KeyboardButton(text=text) for text in el] for el in placeholders['markups']['main_markup']]
    buttons.append([types.KeyboardButton(text="📙 Админ Панель")])
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, row_width=3)

    return keyboard


def admin_markup():
    buttons = [[types.InlineKeyboardButton(text='⬆ Акции', callback_data=AdminCallback(action='sale').pack()), types.InlineKeyboardButton(text='↕ Заказы', callback_data=AdminCallback(action='order').pack())]]
    buttons.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=2)

    return keyboard

def menu_markup():
    buttons = [types.InlineKeyboardButton(text=el[0], callback_data=CategoryCallback(category=el[0], from_where='').pack())
               for el in
               categories]
    sub_list = [buttons[n: n + 3] for n in range(0, len(buttons), 3)]
    sub_list.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=sub_list, resize_keyboard=True, row_width=3)

    return keyboard


def profile_markup():
    buttons = [[types.InlineKeyboardButton(text='📆 Указать дату рождения', callback_data=CategoryCallback(category='дата', from_where='').pack())]]
    buttons.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=3)

    return keyboard


def cart_markup():
    buttons = [[types.InlineKeyboardButton(text="✏ Изменить корзину", callback_data=PurchaseCallback(payment_type="to_edit").pack()),
               types.InlineKeyboardButton(text="📨 Перейти к оформлению", callback_data=PurchaseCallback(payment_type="to_buy").pack())]]
    buttons.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=3)

    return keyboard


def default_markup():
    button = []
    button.extend([types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text in el] for el in placeholders['markups']['menu_markup'])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button, resize_keyboard=True, row_width=3)

    return keyboard


def category_markup(category):
    for el in categories:
        if el[0] == category:
            buttons = [types.InlineKeyboardButton(text=i[0],
                                                  callback_data=ItemCallback(item=i[0], category=i[1],
                                                                             action="check").pack()) for i in
                       get_elements_by_category(category)]
            sub_list = [buttons[n: n + 3] for n in range(0, len(buttons), 3)]
            sub_list.extend([[types.InlineKeyboardButton(text=text,
                                                         callback_data=CategoryCallback(category=text, from_where='').pack())
                              for text
                              in el] for el in placeholders['markups']['category_markup']])
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=sub_list, resize_keyboard=True, row_width=3)

            return keyboard


def item_markup(item, category):
    buttons = [[types.InlineKeyboardButton(text="📥 Добавить в корзину",
                                           callback_data=ItemCallback(item=item, category=category,
                                                                      action="add").pack()),
                types.InlineKeyboardButton(text="📤 Убрать из корзины",
                                           callback_data=ItemCallback(item=item, category=category,
                                                                      action="remove").pack())]]
    buttons.extend(
        [types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where=category).pack()) for
         text in el] for
        el in placeholders['markups']['item_markup'])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=2)

    return keyboard


def purchase_markup():
    buttons = [[types.InlineKeyboardButton(text="💵 Оплата наличными",
                                           callback_data=PaymentCallback(return_type="cash").pack()),
                types.InlineKeyboardButton(text="💳 Оплата картой",
                                           callback_data=PaymentCallback(return_type="card").pack())],
               [types.InlineKeyboardButton(text="ЮКасса",
                                           callback_data=PaymentCallback(return_type="card").pack()),
                types.InlineKeyboardButton(text="QR-CБП",
                                           callback_data=PaymentCallback(return_type="card").pack())],]

    buttons.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=2)

    return keyboard


def order_markup(orderlist):
    buttons = [types.InlineKeyboardButton(text=i, callback_data=OrderCallback(order=i).pack()) for i in orderlist]
    sub_list = [buttons[n: n + 3] for n in range(0, len(buttons), 3)]
    sub_list.extend(
        [[types.InlineKeyboardButton(text=text, callback_data=CategoryCallback(category=text, from_where='').pack()) for text
          in el]
         for el in placeholders['markups']['menu_markup']])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=sub_list, resize_keyboard=True, row_width=2)
    return keyboard

def orderview_markup(ordertag):
    buttons = [[types.InlineKeyboardButton(text="✅ Выполнен", callback_data=AdminCallback(action=f"done{str(ordertag)}").pack()),
                types.InlineKeyboardButton(text="❎ Удалить", callback_data=AdminCallback(action=f"delete{str(ordertag)}").pack())]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons, resize_keyboard=True, row_width=3)
    return keyboard