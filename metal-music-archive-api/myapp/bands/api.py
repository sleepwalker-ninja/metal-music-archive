from ninja import Router
from myapp.models import Band, Album, Track 
from .band_schemas import BandIn, BandOut, BandUpdate
from typing import List
from ninja.errors import HttpError
from datetime import timedelta
import logging
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth

logger = logging.getLogger(__name__)

router = Router(tags=["Band"])

@router.get('/', response=List[BandOut])
def all_bands(request):
    bands = Band.objects.all()
    
    return bands

@router.post("/", auth=JWTAuth(), response=BandOut)
def create_band(request, band_data: BandIn):
    band = Band.objects.create(
        name=band_data.name,
        genre=band_data.genre,
        formed_year=band_data.formed_year,
        origin_country=band_data.origin_country
    )
    return band

@router.get('/{band_id}', response=BandOut)
def get_band_by_id(request, band_id: int):
    band = get_object_or_404(Band, id=band_id)
    return band

@router.patch("/{band_id}", auth=JWTAuth(), response=BandOut)
def update_band(request, band_id: int, data: BandUpdate):
    band = get_object_or_404(Band, id=band_id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(band, attr, value)
    band.save()
    return band

@router.delete("/{band_id}", auth=JWTAuth())
def delete_band(request, band_id: int):
    band = get_object_or_404(Band, id=band_id)
    band.delete()
    return {"message": "Band deleted"}