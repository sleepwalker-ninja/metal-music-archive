import pytest
from myapp.models import Band
import json

@pytest.mark.django_db
def test_create_band_success(auth_client):
    payload = {
        "name": "Judas Priest",
        "genre": "Heavy Metal",
        "formed_year": 1969,
        "origin_country": "UK"
    }
    
    response = auth_client.post(
        "/api/band/",
        data=payload,
        content_type = "application/json"
    )
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["name"] == "Judas Priest"
    assert data["genre"] == "Heavy Metal"
    assert data["formed_year"] == 1969
    assert data["origin_country"] == "UK"
    assert "id" in data
    
    assert Band.objects.filter(name=data["name"]).exists()


@pytest.mark.django_db
def test_create_band_valid_error(auth_client):
    payload = {
        "genre": "Trash Metal",
        "formed_year": 1969,
        "origin_country": "Azerbaijan"
    }
    
    response = auth_client.post(
        "/api/band/",
        data=payload,
        content_type = "application/json"
    )
    
    assert response.status_code == 422
    
    data = response.json()
    assert data["detail"][0]["loc"][-1] == "name"


@pytest.mark.django_db
def test_get_band_by_id(auth_client):
    band = Band.objects.create(
        name="Iron Maiden",
        genre="Heavy Metal",
        formed_year=1975,
        origin_country="UK"
    )

    response = auth_client.get(
        f"/api/band/{band.id}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Iron Maiden"
    assert data["id"] == band.id


@pytest.mark.django_db
def test_get_band_by_id_failed(auth_client):
    response = auth_client.get(f"/api/band/99")
    assert response.status_code == 404



@pytest.mark.django_db
def test_update_band_success(auth_client):
    band = Band.objects.create(
        name="Kommendant",
        genre="Trash Metal",
        formed_year=2025,
        origin_country="Azerbaijan"
    )
    
    payload = {
        "formed_year": 2026
    }
    
    response = auth_client.patch(
        f"/api/band/{band.id}",
        data = payload,
        content_type="application/json"
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["formed_year"] == 2026
    assert data["name"] == "Kommendant"
    
    band.refresh_from_db()
    assert band.formed_year == 2026

@pytest.mark.django_db
def test_update_band_fail_id(auth_client):
    payload = {
        "name": "kommendadnt"
    }
    
    response = auth_client.patch(
        "/api/band/99",
        data=payload,
        content_type="application/json"
    )
    
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_band_success(auth_client):
    band = Band.objects.create(
        name="Komendant",
        genre="Trash Metal",
        formed_year=2025,
        origin_country="Azerbaijan"
    )
    
    response = auth_client.delete(f"/api/band/{band.id}")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Band deleted"}
    assert not Band.objects.filter(id=band.id).exists()


@pytest.mark.django_db
def test_delete_band_fail_id(auth_client):
    response = auth_client.delete("api/band/99")
    assert response.status_code == 404