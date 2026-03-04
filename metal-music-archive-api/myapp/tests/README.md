# Band Module Tests

Bu layihədə Band modulu üçün yazılmış pytest testləri.

## Struktur

```
myapp/tests/
├── __init__.py
├── conftest.py           # Ümumi fixture'lər
├── unit/                 # Unit testlər
│   ├── __init__.py
│   ├── test_band_model.py       # Band model testləri
│   └── test_band_schemas.py     # Band schema testləri
├── api/                  # API testləri
│   ├── __init__.py
│   └── test_band_api.py         # Band API endpoint testləri
└── integration/          # İnteqrasiya testləri
    ├── __init__.py
    └── test_band_integration.py # Band workflow testləri
```

## Test Növləri

### Unit Tests (18 test)
Model və schema səviyyəsində ayrı-ayrı komponentlərin testləri:
- Band model CRUD əməliyyatları
- Band-Album əlaqələri
- Schema validasiyaları
- Pydantic field validator'ları

### API Tests (17 test)
API endpoint'lərin testləri:
- GET /api/band/ - bütün bandları siyahıyamaq
- POST /api/band/ - yeni band yaratmaq (autentifikasiyalı)
- GET /api/band/{id} - konkret band məlumatı
- PATCH /api/band/{id} - band yeniləmək (autentifikasiyalı)
- DELETE /api/band/{id} - band silmək (autentifikasiyalı)

### Integration Tests (7 test)
Tam workflow testləri:
- Tam CRUD əməliyyatları dövrü
- Çoxlu bandların yaradılması və siyahılanması
- Band-Album əlaqələri integration
- Cascade delete testləri
- Autentifikasiya workflow'u

## Testləri İşə Salmaq

### Bütün testlər:
```bash
pytest myapp/tests/ -v
```

### Müəyyən qovluqdakı testlər:
```bash
# Yalnız unit testlər
pytest myapp/tests/unit/ -v

# Yalnız API testlər
pytest myapp/tests/api/ -v

# Yalnız integration testlər
pytest myapp/tests/integration/ -v
```

### Konkret test faylı:
```bash
pytest myapp/tests/unit/test_band_model.py -v
```

### Konkret test funksiyası:
```bash
pytest myapp/tests/unit/test_band_model.py::TestBandModel::test_create_band -v
```

### Coverage ilə:
```bash
pytest myapp/tests/ --cov=myapp --cov-report=html
```

## Fixture'lər

### conftest.py-da mövcud olan fixture'lər:
- `user` - Test istifadəçisi (testuser/testpass123)
- `band` - Test bandı (Metallica)
- `band_data` - Band yaratmaq üçün hazır data
- `multiple_bands` - 3 ədəd test bandı
- `band_with_albums` - Albumları olan band (Dio)

### API testlərində olan fixture'lər:
- `api_client` - Django test client
- `authenticated_client` - JWT token ilə autentifikasiyalı client

## Test Covereage

Cəmi testlər: **42**
- Unit Tests: 18 ✓
- API Tests: 17 ✓  
- Integration Tests: 7 ✓

Status: **100% PASSED** ✓

## Qeydlər

1. Testlər ayrıca test database'də icra olunur
2. JWT autentifikasiya testlərdə `RefreshToken.for_user()` ilə yerinə yetirilir
3. Hər test sonra database rollback olunur (transaction isolation)
4. pytest-django istifadə olunur

## Gələcək İşlər

Digər modular üçün də oxşar testlər yazmaq:
- Album tests (unit, api, integration)
- Track tests (unit, api, integration)
- User/Auth tests
