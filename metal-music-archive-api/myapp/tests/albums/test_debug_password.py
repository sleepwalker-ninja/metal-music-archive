import pytest
from ninja_extra.testing import TestClient
from core.api import api
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return TestClient(api)

@pytest.mark.django_db
def test_diagnose_registration(api_client):
    print("\n\n--- DİAQNOSTİKA BAŞLADI ---")
    
    payload = {
        "username": "DebugUser",
        "password": "secretpassword123"
    }

    # 1. Qeydiyyat sorğusu göndəririk
    response = api_client.post("/auth/register", json=payload)
    print(f"1. Register Status: {response.status_code}")
    
    # 2. Bazadan istifadəçini tapırıq
    try:
        user = User.objects.get(username="DebugUser")
        print(f"2. User tapıldı: {user.username}")
        print(f"3. Active Status: {user.is_active}")
        print(f"4. DB-dəki Şifrə: {user.password}")
        
        # Şifrənin heşlənib-heşlənmədiyini yoxlayırıq
        is_hashed = user.password.startswith("pbkdf2") or user.password.startswith("argon2")
        if is_hashed:
            print("   ✅ Şifrə heşlənib (Düzgündür)")
        else:
            print("   ❌ Şifrə heşlənməyib (Açıq mətndir)! Problem buradadır.")
            print("   HƏLL: users/api.py faylında 'User.objects.create' əvəzinə 'User.objects.create_user' işlət.")

        # 5. Login yoxlanışı
        print("5. Login cəhdi edilir...")
        login_res = api_client.post("/token/pair", json=payload)
        print(f"   Login Status: {login_res.status_code}")
        print(f"   Login Body: {login_res.content}")

    except User.DoesNotExist:
        print("❌ User bazaya düşməyib! Transaction problemi ola bilər.")
    
    print("-----------------------------\n")