import pytest
from myapp.models import Album, Band

@pytest.mark.django_db
def test_create_album_success(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash",
        formed_year=2003,
        origin_country="Azerbaijan"
    )
    
    payload = {
        "title": "Burn",
        "about": "First Album",
        "release_date": 2003,
        "order_number": 1
    }
    
    url = f"/api/album/?band_id={band.id}"
    
    response = auth_client.post(
        url,
        data=payload,
        content_type="application/json"
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Burn"

@pytest.mark.django_db
def test_create_album_failed(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash",
        formed_year=2003,
        origin_country="Azerbaijan"
    )
    
    payload = {
        "title": "Burn",
        "about": "First Album",
        "release_date": 2003,
        "order_number": 1
    }
    
    url = "/api/album/?band_id=99"
    
    response = auth_client.post(
        url, 
        data=payload,
        content_type = "application/json"
    )
    
    assert response.status_code == 404
    
@pytest.mark.django_db
def test_create_album_less_data(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash",
        formed_year=2003,
        origin_country="Azerbaijan"
    )
    
    payload = {
        "title": "Burn",
        "about": "First Album",
        "release_date": 2003
    }
    
    url = f"/api/album/?band_id={band.id}"
    
    response = auth_client.post(
        url,
        data=payload,
        content_type = "application/json"
    )

    assert response.status_code == 422

@pytest.mark.django_db
def test_create_album_unauthorized(client):
    url="/api/album/?band_id=1"
    payload = {
        "title": "Burn",
        "about": "First Album",
        "release_date": 2003,
        "order_number": 1
    }
    
    response = client.post(
        url,
        data=payload,
        content_type="application/json"
    )
    
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_album_invalid_types(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash",
        formed_year=2003,
        origin_country="Azerbaijan"
    )
    
    url="/api/album/?band_id=1"
    payload = {
        "title": 34354,
        "about": 2,
        "release_date": "2003",
        "order_number": "1"
    }
    
    response = auth_client.post(
        url,
        data=payload,
        content_type="application/json"
    )
    
    assert response.status_code == 422


@pytest.mark.django_db
def test_create_album_empty_data(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash",
        formed_year=2003,
        origin_country="Azerbaijan"
    )
    
    url="/api/album/?band_id=1"
    payload = {}
    
    response = auth_client.post(
        url,
        data=payload,
        content_type="application/json"
    )
    
    assert response.status_code == 422

@pytest.mark.django_db
def test_create_album_missing_query_param(auth_client):
    payload = {"title": "Title", "about": "About", "release_date": 2024, "order_number": 1}
    url = "/api/album/"
    response = auth_client.post(url, data=payload, content_type="application/json")
    assert response.status_code == 422
