from ninja import Schema
import datetime
from typing import Optional

class TrackIn(Schema):
    title: str
    duration: datetime.timedelta
    order_number: int

class TrackOut(Schema):
    id: int
    title: str
    duration: datetime.timedelta
    order_number: int
    
class TrackUpdate(Schema):
    title: Optional[str] = None
    duration: datetime.timedelta | None=None