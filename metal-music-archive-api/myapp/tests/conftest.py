import pytest
from django.contrib.auth import get_user_model
from myapp.models import Band, Album

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )


@pytest.fixture
def band(db):
    """Create a test band."""
    return Band.objects.create(
        name='Metallica',
        genre='Thrash Metal',
        formed_year=1981,
        origin_country='USA'
    )


@pytest.fixture
def band_data():
    """Return valid band data for creating bands."""
    return {
        'name': 'Iron Maiden',
        'genre': 'Heavy Metal',
        'formed_year': 1975,
        'origin_country': 'UK'
    }


@pytest.fixture
def multiple_bands(db):
    """Create multiple test bands."""
    bands = [
        Band.objects.create(
            name='Black Sabbath',
            genre='Heavy Metal',
            formed_year=1968,
            origin_country='UK'
        ),
        Band.objects.create(
            name='Slayer',
            genre='Thrash Metal',
            formed_year=1981,
            origin_country='USA'
        ),
        Band.objects.create(
            name='Megadeth',
            genre='Thrash Metal',
            formed_year=1983,
            origin_country='USA'
        ),
    ]
    return bands


@pytest.fixture
def band_with_albums(db):
    """Create a band with albums."""
    band = Band.objects.create(
        name='Dio',
        genre='Heavy Metal',
        formed_year=1982,
        origin_country='USA'
    )
    Album.objects.create(
        title='Holy Diver',
        about='Classic metal album',
        release_date=1983,
        order_number=1,
        band=band
    )
    Album.objects.create(
        title='The Last in Line',
        about='Second studio album',
        release_date=1984,
        order_number=2,
        band=band
    )
    return band
