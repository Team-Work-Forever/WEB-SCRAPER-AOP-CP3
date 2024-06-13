class LocationResult():
    location: str
    district: str

    def __init__(self, location: str):
        self.location = ''
        self.district = ''
        self.handle(location)

    def handle(self, location: str):
        if location:
            if ',' in location:
                parts = location.rsplit(',', 1)
                if len(parts) == 2:
                    self.location = parts[0].strip()
                    self.district = parts[1].strip()
                    return
                
            self.location = location
            self.district = location
        else:
            raise Exception(f"Formato inválido de localização. Esperado: 'Localização, Distrito'. ({location})" )
        
    def __str__(self) -> str:
        return f"Location: {self.location}\nDistrict: {self.district}\n"