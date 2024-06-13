from contracts.locationResult import LocationResult
from contracts.offerResult import OfferResult
from contracts.propertyDetailsResult import PropertyDetailsResult
from contracts.urlResult import UrlResult


class PropertyResult():
    url: UrlResult
    location: LocationResult
    offer: OfferResult
    property_details: PropertyDetailsResult

    def __init__(self, url: UrlResult, location: LocationResult, offer: OfferResult, property_details: PropertyDetailsResult):
        self.url = url
        self.location = location
        self.offer = offer
        self.property_details = property_details

    def __str__(self) -> str:
        return f"Property: {self.url}{self.location}{self.offer}{self.property_details}\n\n"