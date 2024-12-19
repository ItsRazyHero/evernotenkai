from aiogram.filters.callback_data import CallbackData
import aiogram


class CategoryCallback(CallbackData, prefix="cat"):
    category: str | None
    from_where: str


class ItemCallback(CallbackData, prefix="item"):
    item: str
    category: str
    action: str


class PurchaseCallback(CallbackData, prefix="purchase"):
    payment_type: str


class PaymentCallback(CallbackData, prefix="return"):
    return_type: str


class AdminCallback(CallbackData, prefix='admin'):
    action: str


class OrderCallback(CallbackData, prefix="order"):
    order: str
