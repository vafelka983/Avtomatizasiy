import pytest

def test_full_scenario(client):
    """Полный сценарий"""
    
    # 1. Создаем катер
    boat_resp = client.post('/boats/add', data={
        'name': 'Интеграционный тест',
        'boat_type': 'Тестовый',
        'displacement': '100.0',
        'build_date': '2024-01-01'
    }, follow_redirects=True)
    
    assert boat_resp.status_code == 200
    content = boat_resp.data.decode('utf-8').lower()
    assert 'успешно' in content or 'добавлен' in content
    
    # 2. Проверяем список катеров
    boats_page = client.get('/boats')
    assert boats_page.status_code == 200
    page_content = boats_page.data.decode('utf-8')
    assert 'Интеграционный тест' in page_content