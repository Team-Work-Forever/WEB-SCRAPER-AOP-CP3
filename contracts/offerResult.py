import re

class OfferResult():
    price: float
    typeOffer: str

    def __init__(self, price: str, typeOffer: str):
        self.price = 0
        self.typeOffer = ''
        self.handle(price, typeOffer)

    def handle(self, price: str, typeOffer: str):

        price = re.sub(r'[^\d.,]', '', price)

        if price.count(',') > 1 and price.count('.') > 1:
            raise Exception("Formato de preço incorreto.")

        if price.count(',') == 1 and price.count('.') == 1:
            # Se há um ponto e uma vírgula, detetar o formato
            if price.find(',') > price.find('.'):
                # '1.234,56' -> '1234.56'
                price = price.replace('.', '').replace(',', '.')
            else:
                # '1,234.56' -> '1234.56'
                price = price.replace(',', '')
        else:
            if price.count(',') == 1:
                if price[-3] == ',':
                    # Provavelmente é '1.000,00' (formato europeu)
                    price = price.replace('.', '').replace(',', '.')
                else:
                    # Pode ser algo como '1,234' (formato americano)
                    price = price.replace(',', '')
            elif price.count('.') == 1:
                if price[-3] == '.':
                    # Provavelmente é '1,000.00' (formato americano)
                    price = price.replace(',', '')
                else:
                    # Pode ser algo como '1.234' (formato europeu)
                    price = price.replace('.', '')

        if price.strip():
            self.price = float(price)
        else:
            self.price = 0.0
        self.typeOffer = typeOffer.strip()

    def __str__(self) -> str:
        return f"Price: {self.price}\nType Offer: {self.typeOffer}\n"