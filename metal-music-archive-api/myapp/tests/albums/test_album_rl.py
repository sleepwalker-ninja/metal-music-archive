import requests
import pytest
import string
import random


class TestAlbum:
    def test_album_lfc(self, api_base_url, auth_header):
        band_data = {
            "name": "Test_Band"+"".join(random.choices(string.ascii_letters + string.digits, k=5)),
            "genre": "Metal",
            "formed_year": 1978, 
            "origin_country": "USA"
        }
        create_band = requests.post(f"{api_base_url}/api/band/", headers=auth_header, json=band_data)
        if create_band.status_code == 200: 
            band_id = create_band.json().get("id")
        else:
            pytest.fail("Failed to create band")
        
        # post album
        album_data = {
            "title": "Test_Album_" + "".join(random.choices(string.ascii_letters + string.digits, k=5)),
            "about": "For Post Test",
            "release_date": 1981,
            "order_number": 1
        }
        album_param = {
            "band_id": band_id
        }
        create_album = requests.post(f"{api_base_url}/api/album/", headers=auth_header, params=album_param, json=album_data)
        
        if create_album.status_code == 200:
            assert create_album.json().get("about") == album_data["about"]           
            album_id = create_album.json().get("id")
        else:
            pytest.fail("Album POST method test fail!")
        
        
        # get album
        get_album = requests.get(f"{api_base_url}/api/album/", params=album_param)
        if get_album.status_code == 200:
            assert get_album.json() == [create_album.json()]
        else:
            pytest.fail("Album GET method fail!")
            
        # patch album
        patch_data = {
            "about": "Changed Data"
        }
        
        patch_album = requests.patch(f"{api_base_url}/api/album/{album_id}", headers=auth_header, json=patch_data)
        if patch_album.status_code == 200:
            assert patch_album.json().get("about") == patch_data["about"]
        else:
            pytest.fail("Album PATCH method fail")
        
        
        # delete album
        deleted_album = requests.delete(f"{api_base_url}/api/album/{album_id}", headers=auth_header)
        if deleted_album.status_code == 200:
            assert deleted_album.json().get("message") == "Album deleted"
        else: 
            pytest.fail("Album DELETE method fail")
        
        # delete band
        delete_band = requests.delete(f"{api_base_url}/api/band/{band_id}", headers=auth_header)
        assert delete_band.status_code == 200