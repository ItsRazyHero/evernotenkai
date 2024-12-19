import json


def load_placeholders() -> dict:
    with open('placeholders.json', 'r') as file:
        return json.load(file)


def add_text_field() -> None:
    with open('placeholders.json', 'r') as file:
        placeholders = json.load(file)

#📕 Меню
    text = '🍨 На нашей странице о нас вы узнаете больше о нашем прекрасном магазине сладостей: его истории, наших сотрудниках и их страсти к кондитерскому искусству.\n\n🍰 Мы гордимся тем, что создаем уникальные и вкусные десерты, используя только натуральные ингредиенты. Наша команда опытных кондитеров вкладывает душу в каждый десерт, чтобы гарантировать, что вы получите максимальное удовольствие от нашей продукции. 🍧\n\n🍰 Мы стремимся предложить вам лучшее, что может предложить «Десертная симфония», и уверены, что наши товары не оставят вас равнодушными!'
    placeholders['text_fields']['🔎 О нас'] = text
    with open('placeholders.json', 'w') as file:
        json.dump(placeholders, file)


def main() -> None:
    add_text_field()


if __name__ == "__main__":
    main()
