import pytest
from ninja_extra.testing import TestClient
from core.api import api
from django.contrib.auth import get_user_model
from ninja_jwt.tokens import RefreshToken

User = get_user_model()

# @pytest.fixture
# def api_client():
#     return TestClient(api)

@pytest.fixture
def auth_header(client, db):
    
    username = "TestUser000"
    password = "test1234"
    
    user = User.objects.create_user(username=username, password=password)
    user.is_active = True
    user.save()
    
    # 2. Token Generasiyası (Manual)
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    
    # 3. Header Formatı (Standart Django Client üçün "HTTP_" vacibdir)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

@pytest.fixture
def create_band(client, auth_header):
    payload = {
        "name": "testBand001",
        "genre": "Metal",
        "formed_year": 1986,
        "origin_country": "USA"
    }
    
    response = client.post("/api/band/", data=payload, content_type="application/json", **auth_header)
    return response.json().get("id")

@pytest.mark.django_db
class TestBandCreate:
    def test_create_band_success(self, client, auth_header):
        payload = {
            "name": "Testband",
            "genre": "Rock",
            "formed_year": 1973,
            "origin_country": "USA"
        }
          
        response = client.post("/api/band/", data=payload, content_type="application/json", **auth_header)
        assert response.status_code == 200, f"Create band ugursuz oldu: {response.content}"

    
    def test_update_band(self, client, auth_header, create_band):
        band_id = create_band
        new_payload = {
            "name": "EditName"
        }
        
        update_response = client.patch(f"/api/band/{band_id}", data=new_payload, content_type="application/json", **auth_header)
        assert update_response.status_code == 200
        assert update_response.json().get("name") == new_payload["name"]
    
    def test_delete_band(self, client, auth_header, create_band):
        band_id = create_band
        delete_reponse = client.delete(f"/api/band/{band_id}", **auth_header)
        assert delete_reponse.status_code == 200
        assert delete_reponse.json().get("message") == "Band deleted"
