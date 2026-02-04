from ninja import Router
from myapp.models import  Album, Track 
from .track_schemas import TrackIn, TrackOut, TrackUpdate
from typing import List
import logging
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth


logger = logging.getLogger(__name__)

router = Router(tags=["Track"])


@router.post("", auth=JWTAuth(), response=TrackOut)
def create_track(request, album_id: int, track_data: TrackIn):
    found_album = get_object_or_404(Album, id=album_id)
    track = Track.objects.create(
        title=track_data.title,
        duration=track_data.duration,
        album=found_album,
        order_number=track_data.order_number
    )
    return track

@router.get("", response=List[TrackOut])
def get_tracks_by_album(request, album_id: int):
    album = get_object_or_404(Album, id=album_id)
    tracks = album.tracks.all()
    
    return tracks

@router.patch("/{track_id}", auth=JWTAuth(), response=TrackOut)
def edit_track(request, track_id: int, data: TrackUpdate):
    track = get_object_or_404(Track, id=track_id)
    
    for attr, value in data.dict(exclude_unset=True).items():
        logger.debug(f'attr-{attr} and value-{value}')
        setattr(track, attr, value)

    track.save()
    logger.debug(f"track save")

    return track

@router.delete("/{track_id}", auth=JWTAuth())
def delete_track(request, track_id: int):
    track = get_object_or_404(Track, id=track_id)
    track.delete()
    return {"message": "Track deleted"}