
from ninja import Router
from myapp.models import Band, Album, Track 
from .album_schemas import AlbumIn, AlbumOut, AlbumUpdate
from typing import List
from ninja.errors import HttpError
from datetime import timedelta
import logging
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth

logger = logging.getLogger(__name__)

router = Router(tags=["Album"])

@router.post('/', auth=JWTAuth(), response=AlbumOut)
def create_album(request, band_id: int,  album_data: AlbumIn):
    found_band = get_object_or_404(Band, id=band_id)
    album = Album.objects.create(
        title=album_data.title,
        about=album_data.about,
        release_date=album_data.release_date,
        band=found_band,
        order_number=album_data.order_number
    )
    return album

@router.get('/', response=List[AlbumOut])
def get_album_by_band(request, band_id: int):
    found_band = get_object_or_404(Band, id=band_id)
    albums = found_band.albums.all()
    
    return albums

@router.patch("/{album_id}", auth=JWTAuth(), response=AlbumOut)
def update_album(request, album_id, data: AlbumUpdate):
    album = get_object_or_404(Album, id=album_id)
    
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(album, attr, value)
    album.save()
    return album

@router.delete("/{album_id}", auth=JWTAuth())
def delete_album(request, album_id: int):
    album = get_object_or_404(Album, id=album_id)
    album.delete()
    return {"message": "Album deleted"}