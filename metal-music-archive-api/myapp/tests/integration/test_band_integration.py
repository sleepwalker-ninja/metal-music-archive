import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from myapp.models import Band, Album
from ninja_jwt.tokens import RefreshToken
import json

User = get_user_model()


@pytest.fixture
def auth_token(db):
    """Create a user and return authentication token."""
    user = User.objects.create_user(
        username='integrationuser',
        email='integration@test.com',
        password='integrationpass123'
    )
    
    # Generate JWT token programmatically
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    return access_token


@pytest.mark.django_db
class TestBandIntegrationWorkflow:
    """Integration tests for complete Band workflows."""
    
    def test_complete_band_crud_workflow(self, auth_token):
        """Test complete CRUD workflow for a band."""
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        
        # 1. Create a band
        band_data = {
            'name': 'Testament',
            'genre': 'Thrash Metal',
            'formed_year': 1983,
            'origin_country': 'USA'
        }
        
        create_response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        assert create_response.status_code == 200
        band_id = create_response.json()['id']
        
        # 2. Read the band
        get_response = client.get(f'/api/band/{band_id}')
        assert get_response.status_code == 200
        assert get_response.json()['name'] == 'Testament'
        
        # 3. Update the band
        update_data = {'genre': 'Technical Thrash Metal'}
        update_response = client.patch(
            f'/api/band/{band_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        assert update_response.json()['genre'] == 'Technical Thrash Metal'
        
        # 4. Delete the band
        delete_response = client.delete(f'/api/band/{band_id}')
        assert delete_response.status_code == 200
        
        # 5. Verify deletion
        get_deleted_response = client.get(f'/api/band/{band_id}')
        assert get_deleted_response.status_code == 404
    
    def test_create_multiple_bands_and_list(self, auth_token):
        """Test creating multiple bands and listing them."""
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        
        bands_data = [
            {'name': 'Anthrax', 'genre': 'Thrash Metal', 'formed_year': 1981, 'origin_country': 'USA'},
            {'name': 'Exodus', 'genre': 'Thrash Metal', 'formed_year': 1979, 'origin_country': 'USA'},
            {'name': 'Kreator', 'genre': 'Thrash Metal', 'formed_year': 1982, 'origin_country': 'Germany'},
        ]
        
        # Create multiple bands
        created_ids = []
        for band_data in bands_data:
            response = client.post(
                '/api/band/',
                data=json.dumps(band_data),
                content_type='application/json'
            )
            assert response.status_code == 200
            created_ids.append(response.json()['id'])
        
        # List all bands
        list_response = client.get('/api/band/')
        assert list_response.status_code == 200
        bands = list_response.json()
        assert len(bands) >= 3
        
        band_names = [band['name'] for band in bands]
        assert 'Anthrax' in band_names
        assert 'Exodus' in band_names
        assert 'Kreator' in band_names
    
    def test_band_with_albums_integration(self, auth_token):
        """Test creating a band and adding albums to it."""
        client = Client()
        
        # 1. Create a band
        band_data = {
            'name': 'Death',
            'genre': 'Death Metal',
            'formed_year': 1983,
            'origin_country': 'USA'
        }
        
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        create_response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        assert create_response.status_code == 200
        band_id = create_response.json()['id']
        
        # 2. Add albums directly to database (as album API would do)
        band = Band.objects.get(id=band_id)
        Album.objects.create(
            title='Scream Bloody Gore',
            about='Debut album',
            release_date=1987,
            order_number=1,
            band=band
        )
        Album.objects.create(
            title='Leprosy',
            about='Second album',
            release_date=1988,
            order_number=2,
            band=band
        )
        
        # 3. Get band and verify albums are included
        get_response = client.get(f'/api/band/{band_id}')
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data['albums']) == 2
        assert 'Scream Bloody Gore' in data['albums']
        assert 'Leprosy' in data['albums']
    
    def test_delete_band_cascades_to_albums(self, auth_token):
        """Test that deleting a band also deletes its albums."""
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        
        # 1. Create a band
        band_data = {
            'name': 'Morbid Angel',
            'genre': 'Death Metal',
            'formed_year': 1983,
            'origin_country': 'USA'
        }
        
        create_response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        band_id = create_response.json()['id']
        
        # 2. Add albums
        band = Band.objects.get(id=band_id)
        album1 = Album.objects.create(
            title='Altars of Madness',
            about='Debut album',
            release_date=1989,
            order_number=1,
            band=band
        )
        album2 = Album.objects.create(
            title='Blessed Are the Sick',
            about='Second album',
            release_date=1991,
            order_number=2,
            band=band
        )
        
        album1_id = album1.id
        album2_id = album2.id
        
        # 3. Delete the band
        delete_response = client.delete(f'/api/band/{band_id}')
        assert delete_response.status_code == 200
        
        # 4. Verify albums are also deleted
        assert Album.objects.filter(id=album1_id).count() == 0
        assert Album.objects.filter(id=album2_id).count() == 0
    
    def test_update_band_does_not_affect_albums(self, auth_token):
        """Test that updating band info doesn't affect its albums."""
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        
        # 1. Create band with albums
        band_data = {
            'name': 'Carcass',
            'genre': 'Grindcore',
            'formed_year': 1985,
            'origin_country': 'UK'
        }
        
        create_response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        band_id = create_response.json()['id']
        
        band = Band.objects.get(id=band_id)
        Album.objects.create(
            title='Reek of Putrefaction',
            about='Debut album',
            release_date=1988,
            order_number=1,
            band=band
        )
        
        # 2. Update band
        update_data = {'genre': 'Melodic Death Metal'}
        update_response = client.patch(
            f'/api/band/{band_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        
        # 3. Verify albums still exist
        get_response = client.get(f'/api/band/{band_id}')
        data = get_response.json()
        assert data['genre'] == 'Melodic Death Metal'
        assert len(data['albums']) == 1
        assert 'Reek of Putrefaction' in data['albums']
    
    def test_authentication_workflow(self, db):
        """Test authentication is required for write operations."""
        client = Client()
        
        # Create a band without authentication - should fail
        band_data = {
            'name': 'Test Band',
            'genre': 'Metal',
            'formed_year': 1980,
            'origin_country': 'USA'
        }
        
        response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        assert response.status_code == 401
        
        # Create user and generate token programmatically
        user = User.objects.create_user(
            username='authtest',
            password='authpass123'
        )
        
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        
        # Now create with authentication - should succeed
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        response = client.post(
            '/api/band/',
            data=json.dumps(band_data),
            content_type='application/json'
        )
        assert response.status_code == 200
    
    def test_concurrent_band_operations(self, auth_token):
        """Test multiple operations on different bands."""
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {auth_token}'
        
        # Create first band
        band1_response = client.post(
            '/api/band/',
            data=json.dumps({
                'name': 'Sepultura',
                'genre': 'Thrash Metal',
                'formed_year': 1984,
                'origin_country': 'Brazil'
            }),
            content_type='application/json'
        )
        band1_id = band1_response.json()['id']
        
        # Create second band
        band2_response = client.post(
            '/api/band/',
            data=json.dumps({
                'name': 'Soulfly',
                'genre': 'Groove Metal',
                'formed_year': 1997,
                'origin_country': 'USA'
            }),
            content_type='application/json'
        )
        band2_id = band2_response.json()['id']
        
        # Update first band
        client.patch(
            f'/api/band/{band1_id}',
            data=json.dumps({'genre': 'Death Metal'}),
            content_type='application/json'
        )
        
        # Get both bands and verify
        band1 = client.get(f'/api/band/{band1_id}').json()
        band2 = client.get(f'/api/band/{band2_id}').json()
        
        assert band1['genre'] == 'Death Metal'
        assert band2['genre'] == 'Groove Metal'
        assert band1['name'] == 'Sepultura'
        assert band2['name'] == 'Soulfly'
