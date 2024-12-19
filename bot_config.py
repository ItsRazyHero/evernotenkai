import asyncio
import logging
import datetime
from aiogram.fsm.state import State, StatesGroup
from models import *
from keyboards import *
from config_database import get_elements_by_name, get_user_by_user_id, create_user, set_user_bday_by_user_id, create_order, get_first_9_orders, get_order_by_tag, delete_order_by_tag, update_user
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from callbacks import *
from random import randint


logging.basicConfig(level=logging.INFO, filename='InternalLogs.log')
logger = logging.getLogger('Logger')
bot = Bot(token="6981741347:AAGxJEdy2WKeaPheV3kr5mNUCdcnLVvrTGE")
cart = UsersCart()
dp = Dispatcher()
trustedUser = '1439042957,6474105213'

logger.info(f'[{datetime.datetime.now().strftime("%d.%m | %H:%M")}] Приложение запущено!')


class Form(StatesGroup):
    address = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    photo = types.FSInputFile("imgs/cake.jpg")
    print(message.from_user.id)
    user_data = get_user_by_user_id(message.from_user.id)
    if user_data is None:
        create_user(message.from_user.id)
    if str(message.from_user.id) in trustedUser:
        print('admin')
        await message.answer_photo(photo=photo, caption=placeholders['text_fields']['greetings'],
                                   reply_markup=main_admin())
    else:
        await message.answer_photo(photo=photo, caption=placeholders['text_fields']['greetings'],
                               reply_markup=main_markup())


@dp.message()
async def on_message(message: types.Message):

    if message.text in placeholders['text_fields']['buttons']:
        await message.delete()
        photo = types.FSInputFile(f"imgs/{message.text}.png")
        if message.text == '🛒 Корзина':
            await message.answer_photo(photo=photo, caption=cart.pack_cart(message.from_user.id), reply_markup=cart_markup())
        elif message.text == '📙 Админ Панель' and str(message.from_user.id) in trustedUser:
            caption = '''🔷 Инструкция по использованию админки:
                1⃣ Информация о заказах
                2⃣  Информация об акциях'''
            await message.answer(text=caption, reply_markup=admin_markup())
        elif message.text == '🎁 Акции':
            print(message.from_user.id)
            await message.answer_photo(photo=photo, caption=placeholders['text_fields'][message.text], reply_markup=default_markup())
        elif message.text == '🔎 О нас':
            await message.answer_photo(photo=photo, caption=placeholders['text_fields'][message.text], reply_markup=default_markup())
        elif message.text == '📥 Оформить заказ':
            reply = cart.pack_cart(message.from_user.id) + "\n" + "После оформления с вами свяжутся наши менеджеры для уточнения деталей!"
            await message.answer(reply, reply_markup=purchase_markup())
            ...
            # await message.answer_photo(photo=photo, caption=placeholders['text_fields'][message.text], reply_markup=default_markup())
        elif message.text == '👤 Профиль':
            profile_pictures = await bot.get_user_profile_photos(message.from_user.id, 1, 1)

            if profile_pictures.total_count > 0:
                user_photo = types.FSInputFile("imgs/👤 Профиль.png")
            else:
                user_photo = types.FSInputFile("imgs/👤 Профиль.png")

            user_data = get_user_by_user_id(message.from_user.id)
            if user_data is None:
                create_user(message.from_user.id)
                user_data = (0, message.from_user.id, '')

            string = f'''📔 Ваш профиль:

⭐ Имя пользователя: {message.from_user.username}

⭐ Ваш уникальный ID: {user_data[1]}

⭐ Общая сумма заказов: {user_data[2]} / {(2 ** user_data[3]) * 1000}

⭐ Уровень скидки: {user_data[3] * 2}%
'''
            await message.answer_photo(photo=user_photo, caption=string, reply_markup=profile_markup())
        else:
            await message.answer_photo(photo=photo, caption=placeholders['text_fields'][message.text], reply_markup=menu_markup())


@dp.callback_query(CategoryCallback.filter())
async def on_category(query: types.CallbackQuery, callback_data: CategoryCallback):
    if "Закрыть" in callback_data.category:
        await query.message.delete()
    elif "Назад" in callback_data.category:
        await query.message.delete()

        if callback_data.from_where == '':
            await query.message.answer_photo(photo=types.FSInputFile("imgs/📕 Меню.png"), caption=placeholders['text_fields']['📕 Меню'], reply_markup=menu_markup())
        else:
            await query.message.answer_photo(photo=types.FSInputFile(f"imgs/{callback_data.from_where}.png"), caption=placeholders['text_fields'][callback_data.from_where], reply_markup=category_markup(callback_data.from_where))
        print(callback_data.from_where)
    else:
        await query.message.delete()
        await query.message.answer_photo(photo=types.FSInputFile(f"imgs/{callback_data.category}.png"), caption=placeholders['text_fields'][callback_data.category],
                                         reply_markup=category_markup(callback_data.category))


@dp.callback_query(ItemCallback.filter(F.action == "check"))
async def on_item_check(query: types.CallbackQuery, callback_data: ItemCallback):
    await query.message.delete()
    price, rating, description, image = get_elements_by_name(callback_data.item)[0]
    photo = types.FSInputFile(image.split('.')[0] + '.jpg')
    string = f'''✨ Представляем вашему вниманию: {callback_data.item}

{description}

💸 Цена: {price}₽
⭐️ Рейтинг: {rating} / 5

✅ C полным описанием и составом вы можете ознакомится на нашем сайте!
'''

    await query.message.answer_photo(photo=photo, caption=string, reply_markup=item_markup(callback_data.item, callback_data.category))


@dp.callback_query(ItemCallback.filter(F.action != "check"))
async def on_item_interact(query: types.CallbackQuery, callback_data: ItemCallback):
    if query.from_user.id not in cart.main_cart.keys():
        cart.add_user(query.from_user.id)
    if callback_data.action == "add":
        act = cart.add_item(query.from_user.id, callback_data.item)
        if act:
            await bot.answer_callback_query(query.id, text=f"Товар {callback_data.item} x1 успешно добавлен в корзину!", show_alert=True)
        else:
            await bot.answer_callback_query(query.id, text="Произошла непредвиденная ошибка. Попробуйте ещё раз.", show_alert=True)
        print(cart.main_cart[query.from_user.id])
    else:
        act = cart.remove_item(query.from_user.id, callback_data.item)
        if act:
            await bot.answer_callback_query(query.id, text=f"Товар {callback_data.item} x1 успешно удален из корзины!", show_alert=True)
        else:
            await bot.answer_callback_query(query.id, text="Произошла непредвиденная ошибка. Попробуйте ещё раз.", show_alert=True)
        print(cart.main_cart[query.from_user.id])


@dp.callback_query(PurchaseCallback.filter(F.payment_type != "cancel"))
async def on_purchase(query: types.CallbackQuery, callback_data: PurchaseCallback):
    await query.message.delete()
    if callback_data.payment_type == "to_buy":
        #photo = types.FSInputFile(f"imgs/🛒 Корзина.png")
        reply = cart.pack_cart(query.from_user.id) + "\n" + "После оформления с вами свяжутся наши менеджеры для уточнения деталей!"
        await query.message.answer(reply, reply_markup=purchase_markup())


        # await query.message.answer_photo(cart.pack_cart(query.from_user.id), reply_markup=cart_markup())
    else:
        photo = types.FSInputFile(f"imgs/📕 Меню.png")
        await query.message.answer_photo(photo=photo, caption=placeholders['text_fields']['📕 Меню'],
                                   reply_markup=menu_markup())


@dp.callback_query(PaymentCallback.filter(F.return_type != "cancel"))
async def on_buy(query: types.CallbackQuery, callback_data: PaymentCallback):
    tag = randint(100000, 999999)
    create_order(tag, f'@{query.from_user.username}/{query.message.chat.id}', cart.get_cart_price(query.from_user.id), cart.pack_cart(query.from_user.id))
    await query.message.delete()
    await query.message.answer(text=f"Ваш заказ #{tag} оформлен. Спасибо за покупку!")


@dp.callback_query(AdminCallback.filter(F.action != ''))
async def on_admin(query: types.CallbackQuery, callback_data: AdminCallback):
    await query.message.delete()
    if callback_data.action == 'order':
        orders = get_first_9_orders()
        reply = ''.join([f'Тэг заказа: {order[1]}\n Заказал: {order[2].split('/')[0]}\n Цена: {order[3]}\n\n' for order in orders])
        await query.message.answer(reply, reply_markup=order_markup([str(order[1]) for order in orders]))
    if callback_data.action.startswith('delete'):
        order = get_order_by_tag(int(callback_data.action.split('delete')[-1]))
        delete_order_by_tag(int(callback_data.action.split('delete')[-1]))
        await bot.send_message(int(order[2].split('/')[-1]), f"❎ Ваш заказ #{callback_data.action.split('delete')[-1]} был удален.\n\n📕 Если это не так, уточните запрос в тех.поддержке.")
    elif callback_data.action.startswith('done'):
        order = get_order_by_tag(int(callback_data.action.split('done')[-1]))
        delete_order_by_tag(int(callback_data.action.split('done')[-1]))
        print(get_user_by_user_id(int(order[2].split('/')[-1])))
        user_data = list(get_user_by_user_id(int(order[2].split('/')[-1])))
        user_data[2] = int(user_data[2]) + int(order[3])
        if user_data[2] > (2 ** user_data[3]) * 1000:
            user_data[3] += 1
        print(user_data)
        update_user(int(user_data[1]), user_data[2], user_data[3])
        await bot.send_message(int(order[2].split('/')[-1]), f"✅ Ваш заказ #{callback_data.action.split('done')[-1]} был выполнен.\n\n📕 Если это не так, уточните запрос в тех.поддержке.")


@dp.callback_query(OrderCallback.filter(F.order != ''))
async def on_order(query: types.CallbackQuery, callback_data: OrderCallback):
    await query.message.delete()
    order = get_order_by_tag(int(callback_data.order))
    reply = f'Тэг заказа: {order[1]}\n Заказал: {order[2]}\n Цена: {order[3]}\n\n {order[4]}\n'
    await query.message.answer(reply, reply_markup=orderview_markup(str(order[1])))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# create a function that takes message from user and replies with his photo
