import pytest

def test_add_catch(client, sample_trip, sample_ground):
    """Пункт 8: Добавление данных о рыбе для рейса и банки"""
    if not sample_trip or not sample_ground:
        pytest.skip("Не удалось создать рейс или банку")
    
    response = client.post('/catches/add', data={
        'trip_id': str(sample_trip['id']),
        'ground_id': str(sample_ground['id']),
        'species_id': '1',  # треска
        'weight': '350.5'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    assert 'успешно' in content or 'добавлен' in content

def test_max_catch_per_species(client):
    """Пункт 3: Топ катеров по улову за период"""
    response = client.post('/reports/max-catch-per-species', data={
        'start_date': '2025-03-01',
        'end_date': '2025-03-31'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Максимальный улов' in content

def test_species_trips(client):
    """Пункт 7: Список сортов рыбы с рейсами"""
    response = client.get('/reports/species-trips')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Сорта рыбы и рейсы' in content

def test_species_ground_catch(client):
    """Пункт 11: Для сорта рыбы и банки список рейсов"""
    response = client.post('/reports/species-ground-catch', data={
        'species_id': '1',
        'ground_id': '1'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Улов по сорту рыбы и банке' in content