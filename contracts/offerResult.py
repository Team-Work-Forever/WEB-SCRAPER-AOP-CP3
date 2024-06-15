import re

labels = {
    "€": 1.0,
    "$": 2.0,
}

type_offer_labels = {
    "comprar": 1.0,
    "arrenda": 2.0,
}

class OfferResult():
    price: float
    currency: str = ''
    typeOffer: str

    def __init__(self, price: str, typeOffer: str):
        self.price = 0.0
        self.typeOffer = ''
        self.handle(price, typeOffer)

    def handle(self, price: str, typeOffer: str):
        
        for key in labels:
            if key in price:
                self.currency = labels.get(key)
            
            price = re.sub(r'[^\d.,]', '', price)
            
            if not price:
                self.currency = 0.0

            self.currency = list(labels.values())[0]


        if price.count(',') > 1 and price.count('.') > 1:
            raise Exception("Incorrect price format!")

        if price.count(',') == 1 and price.count('.') == 1:
            if price.find(',') > price.find('.'):
                # Formato '1.234,56'
                price = price.replace('.', '').replace(',', '.')
            else:
                # Formato '1,234.56'
                price = price.replace(',', '')
        else:
            if price.count(',') == 1:
                if len(price) > 3 and price[-3] == ',':
                    # Provavelmente é '1.000,00' (formato europeu)
                    price = price.replace('.', '').replace(',', '.')
                else:
                    # Pode ser algo como '1,234' (formato americano)
                    price = price.replace(',', '')
            elif price.count('.') == 1:
                if len(price) > 3 and price[-3] == '.':
                    # Provavelmente é '1,000.00' (formato americano)
                    price = price.replace(',', '')
                else:
                    # Pode ser algo como '1.234' (formato europeu)
                    price = price.replace('.', '')
            elif price.count('.') > 1:
                price = price.replace('.', '')

        if price.strip():
            self.price = price
        else:
            self.price = 0.0

        for key in type_offer_labels:
            if key in typeOffer.lower():
                self.typeOffer = type_offer_labels.get(key)
                break
            else:
                self.typeOffer = 0.0

    def __str__(self) -> str:
        return f"Price: {self.price}\nCurrency: {self.currency}\nType Offer: {self.typeOffer}\n"