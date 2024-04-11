from random import randint, choice


def generate_offer():
    udi_rate = 8
    has_open_fee = choice([True, False])
    udis = (
        round(randint(65, 499), -2) if has_open_fee else round(randint(500, 5000), -3)
    )
    available_products = []
    if udis >= 3000:
        available_products.append("black")
    else:
        available_products.append("green")
        available_products.append("shein")
    if has_open_fee:
        open_fee = 500
    else:
        open_fee = 0
    return {
        "product_offered": choice(available_products),
        "credit_line_udis": udis,
        "credit_line": udis * udi_rate,
        "open_fee": open_fee,
    }
