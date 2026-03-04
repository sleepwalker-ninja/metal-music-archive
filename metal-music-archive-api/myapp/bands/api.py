from myapp.models import Band
from .band_schemas import BandIn, BandOut, BandUpdate
from typing import List
import logging
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from ninja_extra import api_controller, http_post, http_get, http_patch, http_delete
from core.errors import DefaultError


logger = logging.getLogger(__name__)

@api_controller("/band", tags=['Band'])
class BandController: 
    @http_get('/', response=List[BandOut])
    def list_band(self):
        bands = Band.objects.all()
        return bands
    
    @http_post('/', auth=JWTAuth(), response=BandOut)
    def create_band(self, data: BandIn): 
        band = Band.objects.create(
            name=data.name,
            genre=data.genre,
            formed_year=data.formed_year,
            origin_country=data.origin_country
        )
        return band
    
    @http_get('/{band_id}', response=BandOut)
    def get_band_by_id(self, band_id: int):
        band = get_object_or_404(Band, id=band_id)
        return band
    
    @http_patch('/{band_id}', auth=JWTAuth(), response=BandOut)
    def update_band(self, band_id: int, data: BandUpdate):
        band = get_object_or_404(Band, id=band_id)
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(band, attr, value)
            
        band.save()
        return band
    
    @http_delete('/{band_id}', auth=JWTAuth())
    def delete_band(self, band_id: int):
        band = get_object_or_404(Band, id=band_id)
        band.delete()
        return {"message": "Band delete successfully"}


# Router-based reference (learning only, not active)
# from ninja import Router
#
# router = Router(tags=["Band"])
#
# @router.get('/', response=List[BandOut])
# def all_bands(request):
#     bands = Band.objects.all()
#     return bands
#
# @router.post('/', auth=JWTAuth(), response=BandOut)
# def create_band_router(request, band_data: BandIn):
#     band = Band.objects.create(
#         name=band_data.name,
#         genre=band_data.genre,
#         formed_year=band_data.formed_year,
#         origin_country=band_data.origin_country,
#     )
#     return band
#
# @router.get('/{band_id}', response=BandOut)
# def get_band_by_id_router(request, band_id: int):
#     band = get_object_or_404(Band, id=band_id)
#     return band
#
# @router.patch('/{band_id}', auth=JWTAuth(), response=BandOut)
# def update_band_router(request, band_id: int, data: BandUpdate):
#     band = get_object_or_404(Band, id=band_id)
#     for attr, value in data.dict(exclude_unset=True).items():
#         setattr(band, attr, value)
#     band.save()
#     return band
#
# @router.delete('/{band_id}', auth=JWTAuth())
# def delete_band_router(request, band_id: int):
#     band = get_object_or_404(Band, id=band_id)
#     band.delete()
#     return {"message": "Band deleted"}