import pytest
from pydantic import ValidationError
from myapp.bands.band_schemas import BandIn, BandOut, BandUpdate


class TestBandSchemas:
    """Unit tests for Band schemas."""
    
    def test_band_in_valid_data(self):
        """Test BandIn schema with valid data."""
        data = {
            'name': 'Opeth',
            'genre': 'Progressive Metal',
            'formed_year': 1989,
            'origin_country': 'Sweden'
        }
        
        band_in = BandIn(**data)
        assert band_in.name == 'Opeth'
        assert band_in.genre == 'Progressive Metal'
        assert band_in.formed_year == 1989
        assert band_in.origin_country == 'Sweden'
    
    def test_band_in_year_validation_valid(self):
        """Test BandIn year validation with valid year."""
        data = {
            'name': 'Black Sabbath',
            'genre': 'Heavy Metal',
            'formed_year': 1968,
            'origin_country': 'UK'
        }
        
        band_in = BandIn(**data)
        assert band_in.formed_year == 1968
    
    def test_band_in_year_validation_invalid(self):
        """Test BandIn year validation with year before 1960."""
        data = {
            'name': 'Invalid Band',
            'genre': 'Heavy Metal',
            'formed_year': 1959,
            'origin_country': 'USA'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            BandIn(**data)
        
        assert "Metal music didn't exist before 1960!" in str(exc_info.value)
    
    def test_band_in_missing_required_fields(self):
        """Test BandIn schema with missing required fields."""
        data = {
            'name': 'Incomplete Band',
            'genre': 'Heavy Metal'
            # Missing formed_year and origin_country
        }
        
        with pytest.raises(ValidationError):
            BandIn(**data)
    
    def test_band_update_all_fields_optional(self):
        """Test BandUpdate schema allows all fields to be optional."""
        # Empty update should be valid
        band_update = BandUpdate()
        assert band_update.name is None
        assert band_update.genre is None
        assert band_update.formed_year is None
        assert band_update.origin_country is None
    
    def test_band_update_partial_update(self):
        """Test BandUpdate schema with partial data."""
        data = {
            'name': 'Updated Name',
            'genre': 'Updated Genre'
        }
        
        band_update = BandUpdate(**data)
        assert band_update.name == 'Updated Name'
        assert band_update.genre == 'Updated Genre'
        assert band_update.formed_year is None
        assert band_update.origin_country is None
    
    def test_band_update_single_field(self):
        """Test BandUpdate schema with single field."""
        data = {'formed_year': 1985}
        
        band_update = BandUpdate(**data)
        assert band_update.formed_year == 1985
        assert band_update.name is None
    
    def test_band_out_serialization(self, band_with_albums):
        """Test BandOut schema serialization with albums."""
        band_out = BandOut.from_orm(band_with_albums)
        
        assert band_out.id == band_with_albums.id
        assert band_out.name == 'Dio'
        assert band_out.genre == 'Heavy Metal'
        assert band_out.formed_year == 1982
        assert band_out.origin_country == 'USA'
        assert len(band_out.albums) == 2
        assert 'Holy Diver' in band_out.albums
        assert 'The Last in Line' in band_out.albums
    
    def test_band_out_resolve_albums_empty(self, band):
        """Test BandOut with band that has no albums."""
        band_out = BandOut.from_orm(band)
        
        assert band_out.albums == []
    
    def test_band_in_string_type_validation(self):
        """Test BandIn validates string types."""
        data = {
            'name': 123,  # Should be string
            'genre': 'Metal',
            'formed_year': 1980,
            'origin_country': 'USA'
        }
        
        # Pydantic V2 is strict about types and won't coerce int to string
        with pytest.raises(ValidationError) as exc_info:
            BandIn(**data)
        
        assert 'string_type' in str(exc_info.value)
    
    def test_band_in_int_type_validation(self):
        """Test BandIn validates integer types."""
        data = {
            'name': 'Test Band',
            'genre': 'Metal',
            'formed_year': '1980',  # String that can be coerced
            'origin_country': 'USA'
        }
        
        band_in = BandIn(**data)
        assert isinstance(band_in.formed_year, int)
        assert band_in.formed_year == 1980
