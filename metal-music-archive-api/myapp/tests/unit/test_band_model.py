import pytest
from myapp.models import Band, Album


@pytest.mark.django_db
class TestBandModel:
    """Unit tests for Band model."""
    
    def test_create_band(self):
        """Test creating a band with valid data."""
        band = Band.objects.create(
            name='Judas Priest',
            genre='Heavy Metal',
            formed_year=1969,
            origin_country='UK'
        )
        
        assert band.id is not None
        assert band.name == 'Judas Priest'
        assert band.genre == 'Heavy Metal'
        assert band.formed_year == 1969
        assert band.origin_country == 'UK'
    
    def test_band_str_representation(self):
        """Test band string representation."""
        band = Band.objects.create(
            name='Pantera',
            genre='Groove Metal',
            formed_year=1981,
            origin_country='USA'
        )
        
        assert str(band) == 'Pantera'
    
    def test_band_albums_relationship(self, band):
        """Test band-album relationship."""
        album1 = Album.objects.create(
            title='Master of Puppets',
            about='Thrash metal masterpiece',
            release_date=1986,
            order_number=1,
            band=band
        )
        album2 = Album.objects.create(
            title='Ride the Lightning',
            about='Second studio album',
            release_date=1984,
            order_number=2,
            band=band
        )
        
        assert band.albums.count() == 2
        assert album1 in band.albums.all()
        assert album2 in band.albums.all()
    
    def test_band_cascade_delete(self, band):
        """Test that deleting a band deletes its albums."""
        Album.objects.create(
            title='Test Album',
            about='Test description',
            release_date=2000,
            order_number=1,
            band=band
        )
        
        band_id = band.id
        band.delete()
        
        assert Band.objects.filter(id=band_id).count() == 0
        assert Album.objects.filter(band_id=band_id).count() == 0
    
    def test_update_band_fields(self, band):
        """Test updating band fields."""
        band.name = 'Updated Name'
        band.genre = 'Updated Genre'
        band.save()
        
        updated_band = Band.objects.get(id=band.id)
        assert updated_band.name == 'Updated Name'
        assert updated_band.genre == 'Updated Genre'
    
    def test_multiple_bands(self, multiple_bands):
        """Test querying multiple bands."""
        assert Band.objects.count() == 3
        
        thrash_bands = Band.objects.filter(genre='Thrash Metal')
        assert thrash_bands.count() == 2
        
        uk_bands = Band.objects.filter(origin_country='UK')
        assert uk_bands.count() == 1
