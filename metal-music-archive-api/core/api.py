# Fayl: core/api.py

from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from myapp.users.api import router as auth_router
from myapp.bands.api import router as band_router
from myapp.albums.api import router as album_router
from myapp.tracks.api import router as track_router

# API obyekti burada yaradılır
api = NinjaExtraAPI(
    title="Metal Music Archive"
)

# Routerlər burada əlavə olunur
api.add_router("/auth", auth_router)
api.add_router("/band", band_router)
api.add_router("/album", album_router)
api.add_router("/track", track_router)
api.register_controllers(NinjaJWTDefaultController)