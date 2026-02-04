from ninja import Schema
import datetime
from typing import Optional, List
from pydantic import field_validator

class AlbumIn(Schema):
    title: str
    about: str
    release_date: int | None
    order_number: int


class AlbumOut(Schema):
    id: int
    title: str
    about: str
    release_date: int | None
    order_number: int
    
class AlbumUpdate(Schema):
    title: str | None=None
    about: str | None=None
    release_date: int | None=None