from ninja import Schema
from typing import List
from pydantic import field_validator

class BandIn(Schema):
    name: str
    genre: str
    formed_year: int
    origin_country: str
    
    @field_validator('formed_year')
    def check_year(cls, value):
        if value < 1960:
            raise ValueError("Metal music didn't exist before 1960!")
        return value

class BandOut(Schema):
    id: int
    name: str
    genre: str
    formed_year: int
    origin_country: str
    albums: List[str]
    
    @staticmethod
    def resolve_albums(obj):
        return [album.title for album in obj.albums.all()]

class BandUpdate(Schema):
    name: str | None=None
    genre: str | None=None
    formed_year: int | None=None
    origin_country: str | None=None