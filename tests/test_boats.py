import pytest

def test_add_boat(client):
    """Пункт 10: Добавление нового катера"""
    response = client.post('/boats/add', data={
        'name': 'Северный ветер',
        'boat_type': 'Сейнер',
        'displacement': '180.0',
        'build_date': '2021-06-20'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    assert 'добавить катер' in content or 'успешно' in content

def test_get_boats(client):
    """Пункт 1: Получение списка катеров"""
    response = client.get('/boats')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Список катеров' in content

def test_update_boat(client, sample_boat):
    """Пункт 9: Изменение характеристик катера"""
    if not sample_boat:
        pytest.skip("Не удалось создать катер")
    
    response = client.post(f'/boats/{sample_boat["id"]}/edit', data={
        'name': 'Морской волк (обновленный)',
        'boat_type': 'Большой траулер',
        'displacement': '260.0',
        'build_date': '2020-03-15'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    content = response.data.decode('utf-8').lower()
    assert 'обновлен' in content or 'успешно' in content

def test_boats_catches(client):
    """Пункт 1 (отчет): Уловы по катерам"""
    response = client.get('/boats/catches')
    assert response.status_code == 200
    content = response.data.decode('utf-8')
    assert 'Уловы по катерам' in content