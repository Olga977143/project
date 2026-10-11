"""Тесты с использованием библиотеки requests и живого Flask-сервера."""
import requests


# --- Доступность ---

def test_homepage_is_available(live_server):
    response = requests.get(live_server, timeout=5)
    assert response.status_code == 200
    assert "Калькулятор" in response.text


def test_homepage_content_type(live_server):
    response = requests.get(live_server, timeout=5)
    assert response.headers["Content-Type"].startswith("text/html")


# --- Реальные POST-запросы ---

def test_requests_addition(live_server):
    response = requests.post(
        live_server,
        data={"num1": "12", "num2": "8", "operation": "add"},
        timeout=5,
    )
    assert response.status_code == 200
    assert "Результат: 20" in response.text


def test_requests_division(live_server):
    response = requests.post(
        live_server,
        data={"num1": "100", "num2": "4", "operation": "div"},
        timeout=5,
    )
    assert "Результат: 25" in response.text


def test_requests_division_by_zero(live_server):
    response = requests.post(
        live_server,
        data={"num1": "5", "num2": "0", "operation": "div"},
        timeout=5,
    )
    assert "Ошибка: деление на ноль" in response.text


# --- Серия запросов подряд ---

def test_multiple_sequential_requests(live_server):
    scenarios = [
        ("1", "1", "add", "2"),
        ("5", "5", "mul", "25"),
        ("9", "3", "div", "3"),
        ("10", "7", "sub", "3"),
    ]
    for num1, num2, op, expected in scenarios:
        response = requests.post(
            live_server,
            data={"num1": num1, "num2": num2, "operation": op},
            timeout=5,
        )
        assert response.status_code == 200
        assert f"Результат: {expected}" in response.text


# --- Ошибки HTTP ---

def test_unknown_route_returns_404(live_server):
    response = requests.get(f"{live_server}/unknown", timeout=5)
    assert response.status_code == 404