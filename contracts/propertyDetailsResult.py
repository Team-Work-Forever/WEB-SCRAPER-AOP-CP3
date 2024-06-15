import re

texts = ["m2", "m\n2"]

area = 1.0
landArea = 2.0
privateArea = 3.0
bathRoom = 4.0
bedRoom = 5.0
parking = 6.0
floor = 7.0
energeticCertificate = 8.0
lift = 9.0
fenced = 10.0
fractions = 11.0

class Dictionary():
    labels = {
        "icon-housearea": area,
        "Área Útil (m2)": area,
        "icon-area-full": area,
        "icon-landarea": landArea,
        "Área Terreno (m2)": landArea,
        "Área Bruta Privativa (m2)": privateArea,
        "icon-bath": bathRoom,
        "Casas de Banho": bathRoom,
        "icon-wc-full": bathRoom,
        "icon-bed": bedRoom,
        "Quartos": bedRoom,
        "icon-bedroom-full": bedRoom,
        "Certificado Energético": energeticCertificate,
        "Elevador": lift,
        "Piso": floor,
        "Estacionamento": parking,
        "Vedado": fenced,
        "Frações": fractions,
        }


class PropertyDetailsResult():
    type: str
    details: {str, }

    def __init__(self, type: str, details: {str, str}):
        self.type = ''
        self.details = {}
        self.handle(type, details)

    def handle(self,type: str, details: {str, str}):        
        dictionary = Dictionary()

        for key, value in details.items():
            
            if dictionary.labels.get(key):
                key = dictionary.labels.get(key)

            cleaned_value = self.process_detail_value(key, value)
            self.details[key] = cleaned_value
        
        self.type = type

    def process_detail_value(self, key: str, value: str):
        for text in texts:
            if text in value:
                value = value.replace(text, '').strip()
                value = value.replace(',', '.')

        if key == parking or key == energeticCertificate or key == lift or key == fenced:
            return 1.0
        elif '--' in value:
            return 0.0
        elif '-' in value:
            value = re.sub(r'[^\d.]', '', value)
            return float(value.split('-')[0])
        elif not value:
            return 0.0
        else:
            value = re.sub(r'[^\d.]', '', value)
            return float(value)

    def __str__(self) -> str:
        return f"House Type: {self.type}\nDetails: {self.details}\n"