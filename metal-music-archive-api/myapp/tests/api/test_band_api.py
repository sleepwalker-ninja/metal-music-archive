import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken
import json

User = get_user_model()


@pytest.fixture
def api_client():
    """Return a Django test client."""
    return Client()


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client with JWT token."""
    # Generate JWT token programmatically
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Create a new client with authorization header
    client = Client()
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return client


@pytest.mark.django_db
class TestBandAPIEndpoints:
    """API tests for Band endpoints."""
    
    def test_list_bands_empty(self, api_client):
        """Test listing bands when database is empty."""
        response = api_client.get('/api/band/')
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_bands(self, api_client, multiple_bands):
        """Test listing all bands."""
        response = api_client.get('/api/band/')
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Check that response contains expected fields
        band_names = [band['name'] for band in data]
        assert 'Black Sabbath' in band_names
        assert 'Slayer' in band_names
        assert 'Megadeth' in band_names
    
    def test_create_band_authenticated(self, authenticated_client, band_data):
        """Test creating a band with authentication."""
        response = authenticated_client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Iron Maiden'
        assert data['genre'] == 'Heavy Metal'
        assert data['formed_year'] == 1975
        assert data['origin_country'] == 'UK'
        assert 'id' in data
    
    def test_create_band_unauthenticated(self, api_client, band_data):
        """Test creating a band without authentication fails."""
        response = api_client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_create_band_invalid_year(self, authenticated_client):
        """Test creating a band with invalid year."""
        data = {
            'name': 'Invalid Band',
            'genre': 'Heavy Metal',
            'formed_year': 1959,
            'origin_country': 'USA'
        }
        
        response = authenticated_client.post(
            '/api/band/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_create_band_missing_fields(self, authenticated_client):
        """Test creating a band with missing required fields."""
        data = {
            'name': 'Incomplete Band',
            'genre': 'Heavy Metal'
            # Missing formed_year and origin_country
        }
        
        response = authenticated_client.post(
            '/api/band/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 422
    
    def test_get_band_by_id(self, api_client, band):
        """Test getting a specific band by ID."""
        response = api_client.get(f'/api/band/{band.id}')
        
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == band.id
        assert data['name'] == 'Metallica'
        assert data['genre'] == 'Thrash Metal'
    
    def test_get_band_by_id_not_found(self, api_client):
        """Test getting a non-existent band."""
        response = api_client.get('/api/band/9999')
        
        assert response.status_code == 404
    
    def test_get_band_with_albums(self, api_client, band_with_albums):
        """Test getting a band that has albums."""
        response = api_client.get(f'/api/band/{band_with_albums.id}')
        
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Dio'
        assert len(data['albums']) == 2
        assert 'Holy Diver' in data['albums']
        assert 'The Last in Line' in data['albums']
    
    def test_update_band_authenticated(self, authenticated_client, band):
        """Test updating a band with authentication."""
        update_data = {
            'name': 'Metallica Updated',
            'genre': 'Heavy Metal'
        }
        
        response = authenticated_client.patch(
            f'/api/band/{band.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Metallica Updated'
        assert data['genre'] == 'Heavy Metal'
        assert data['formed_year'] == 1981  # Unchanged
    
    def test_update_band_unauthenticated(self, api_client, band):
        """Test updating a band without authentication fails."""
        update_data = {'name': 'Updated Name'}
        
        response = api_client.patch(
            f'/api/band/{band.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_update_band_not_found(self, authenticated_client):
        """Test updating a non-existent band."""
        update_data = {'name': 'Updated Name'}
        
        response = authenticated_client.patch(
            '/api/band/9999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_band_partial(self, authenticated_client, band):
        """Test partial update of band."""
        response = authenticated_client.patch(
            f'/api/band/{band.id}',
            data=json.dumps({'origin_country': 'United States'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['origin_country'] == 'United States'
        assert data['name'] == 'Metallica'  # Unchanged
    
    def test_delete_band_authenticated(self, authenticated_client, api_client, band):
        """Test deleting a band with authentication."""
        band_id = band.id
        
        response = authenticated_client.delete(f'/api/band/{band_id}')
        
        assert response.status_code == 200
        assert 'message' in response.json()
        
        # Verify band is deleted
        response = api_client.get(f'/api/band/{band_id}')
        assert response.status_code == 404
    
    def test_delete_band_unauthenticated(self, api_client, band):
        """Test deleting a band without authentication fails."""
        response = api_client.delete(f'/api/band/{band.id}')
        
        assert response.status_code == 401
    
    def test_delete_band_not_found(self, authenticated_client):
        """Test deleting a non-existent band."""
        response = authenticated_client.delete('/api/band/9999')
        
        assert response.status_code == 404


@pytest.mark.django_db
class TestBandAPIValidation:
    """Test API validation for Band endpoints."""
    
    def test_create_band_extra_fields_ignored(self, authenticated_client):
        """Test that extra fields are ignored when creating a band."""
        data = {
            'name': 'Test Band',
            'genre': 'Metal',
            'formed_year': 1980,
            'origin_country': 'USA',
            'extra_field': 'should be ignored'
        }
        
        response = authenticated_client.post(
            '/api/band/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'extra_field' not in response.json()
    
    def test_band_response_structure(self, api_client, band):
        """Test that band response has correct structure."""
        response = api_client.get(f'/api/band/{band.id}')
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ['id', 'name', 'genre', 'formed_year', 'origin_country', 'albums']
        for field in required_fields:
            assert field in data
