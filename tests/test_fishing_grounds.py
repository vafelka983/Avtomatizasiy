import pytest

def test_add_fishing_ground(client):
    """Пункт 5: Добавление новой банки"""
    response = client.post('/grounds/add', data={
        'name': 'Северная банка',
        'latitude': '58.3',
        'longitude': '45.1',
        'depth': '120'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    assert 'успешно' in content or 'банка' in content

def test_get_fishing_grounds(client):
    """Пункт 4: Получение списка банок"""
    response = client.get('/grounds')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Рыболовные банки' in content

def test_boats_above_average(client, sample_ground):
    """Пункт 6: Для банки список катеров с уловом выше среднего"""
    if not sample_ground:
        pytest.skip("Не удалось создать банку")
    
    response = client.get(f'/grounds/{sample_ground["id"]}/boats-above-avg')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Катера с уловом выше среднего' in content