from config_database import get_elements
from accessory_functions import *


class UsersCart:
    def __init__(self):
        self.main_cart = {}
        self.products = {el[1]: el[3] for el in get_elements()}

    def add_user(self, uid: int) -> None:
        self.main_cart[uid] = {}

    def add_item(self, uid: int, product: str) -> bool:
        try:
            quantity = self.main_cart[uid].setdefault(product, 0)
            self.main_cart[uid][product] = quantity + 1
            return True
        except Exception as e:
            print(e, e.__class__.__name__)
            return False

    def remove_item(self, uid: int, product: str) -> bool:
        try:
            quantity = self.main_cart[uid].setdefault(product, 0)
            self.main_cart[uid][product] -= 1
            if (quantity - 1) <= 0:
                del self.main_cart[uid][product]
                print('deleted')
                return True
            else:
                return True
        except Exception as e:
            print(e, e.__class__.__name__)
            return False

    def get_cart_price(self, uid: int) -> int:
        price = 0
        for key, value in self.main_cart[uid].items():
            price += self.products[key] * value
        return price

    def pack_cart(self, uid: int, ) -> str:
        output, max_length = '', 0

        if self.main_cart.get(uid, None) is None or len(self.main_cart[uid]) == 0:
            return 'Ваша корзина пуста'

        output += f'{"_" * (max_length + 1)}\n'
        for key, value in self.main_cart[uid].items():
            if value > 0: current_sting = f'{key} x{value} | {self.products[key] * value}'
            else: continue
            if len(current_sting) > max_length:
                max_length = len(current_sting)
            output += f'{current_sting}\n'

        output += f'{"_" * (max_length + 1)}\n'
        output += f'Итого: {self.get_cart_price(uid)}₽💵\n'

        return output


def main() -> None:
    test_cart = UsersCart()
    test_cart.add_user(1)
    test_cart.add_item(1, '🎂 Маковый')
    test_cart.add_item(1, '🎂 Маковый')
    test_cart.add_item(1, '🎂 Маковый')
    test_cart.add_item(1, '🌰 Эклер')
    print(test_cart.pack_cart(1))


if __name__ == '__main__':
    main()
else:
    placeholders = load_placeholders()
