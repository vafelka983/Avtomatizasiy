import pytest

def test_add_trip(client, sample_boat):
    """Пункт 2: Добавление выхода в море с командой"""
    if not sample_boat:
        pytest.skip("Не удалось создать катер")
    
    response = client.post('/trips/add', data={
        'boat_id': str(sample_boat['id']),
        'departure_date': '2025-04-01T10:00',
        'return_date': '2025-04-15T18:00',
        'crew-0-full_name': 'Алексей Иванов',
        'crew-0-position': 'капитан',
        'crew-0-address': 'ул. Портовая 10',
        'crew-1-full_name': 'Дмитрий Козлов',
        'crew-1-position': 'старшина',
        'crew-1-address': 'ул. Океанская 7'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    assert 'успешно' in content or 'рейс' in content

def test_trips_list(client):
    """Список рейсов"""
    response = client.get('/trips')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Список рейсов' in content

def test_trip_detail(client, sample_trip):
    """Детали рейса"""
    if not sample_trip:
        pytest.skip("Не удалось создать рейс")
    
    response = client.get(f'/trips/{sample_trip["id"]}')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Детали рейса' in content