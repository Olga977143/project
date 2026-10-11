"""Простые интеграционные тесты Flask через test_client."""


# --- GET / ---

def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_contains_form(client):
    html = client.get("/").get_data(as_text=True)
    assert "<form" in html
    assert 'name="num1"' in html
    assert 'name="num2"' in html
    assert 'name="operation"' in html


def test_index_has_no_result_on_first_load(client):
    html = client.get("/").get_data(as_text=True)
    assert "Результат" not in html


# --- POST / : успешные операции ---

def test_post_addition(client):
    response = client.post(
        "/", data={"num1": "5", "num2": "3", "operation": "add"}
    )
    assert response.status_code == 200
    assert "Результат: 8" in response.get_data(as_text=True)


def test_post_subtraction(client):
    response = client.post(
        "/", data={"num1": "10", "num2": "4", "operation": "sub"}
    )
    assert "Результат: 6" in response.get_data(as_text=True)


def test_post_multiplication(client):
    response = client.post(
        "/", data={"num1": "6", "num2": "7", "operation": "mul"}
    )
    assert "Результат: 42" in response.get_data(as_text=True)


def test_post_division(client):
    response = client.post(
        "/", data={"num1": "10", "num2": "4", "operation": "div"}
    )
    assert "Результат: 2.5" in response.get_data(as_text=True)


# --- POST / : ошибки ---

def test_post_division_by_zero(client):
    response = client.post(
        "/", data={"num1": "10", "num2": "0", "operation": "div"}
    )
    assert "Ошибка: деление на ноль" in response.get_data(as_text=True)


def test_post_non_numeric(client):
    response = client.post(
        "/", data={"num1": "abc", "num2": "3", "operation": "add"}
    )
    assert "Ошибка: введите корректные числа" in response.get_data(as_text=True)


# --- Сохранение значений в форме ---

def test_form_values_are_preserved(client):
    html = client.post(
        "/", data={"num1": "42", "num2": "8", "operation": "mul"}
    ).get_data(as_text=True)
    assert 'value="42"' in html
    assert 'value="8"' in html
    assert 'value="mul" selected' in html


# --- HTTP-методы ---

def test_put_not_allowed(client):
    assert client.put("/").status_code == 405


def test_unknown_route_returns_404(client):
    assert client.get("/nope").status_code == 404