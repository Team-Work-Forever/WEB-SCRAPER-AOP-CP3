import re

texts = ["m2", "m\n2"]

area = "AreaM2"
landArea = "LandAreaM2"
privateArea = "PrivateAreaM2"
bathRoom = "BathRoom"
bedRoom = "BedRoom"
parking = "Parking"
floor = "Floor"
energeticCertificate = "EnergeticCertificate"
lift = "Lift"

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
                value = value.replace(text, "").strip()

        if key == parking or key == energeticCertificate or key == lift:
            return True
        elif '--' in value:
            return 0
        elif '-' in value:
            return [int(num.strip()) for num in value.split('-')]
        elif value.isdigit():
            return int(value)
        else:
            return value

    def __str__(self) -> str:
        return f"House Type: {self.type}\nDetails: {self.details}\n"