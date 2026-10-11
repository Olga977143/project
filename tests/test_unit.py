"""Простые модульные тесты функции calculate()."""
import pytest

from app import calculate


# --- Базовые операции ---

def test_add():
    assert calculate("2", "3", "add") == "5"


def test_sub():
    assert calculate("10", "4", "sub") == "6"


def test_mul():
    assert calculate("6", "7", "mul") == "42"


def test_div():
    assert calculate("10", "4", "div") == "2.5"


# --- Граничные случаи ---

def test_add_floats():
    assert calculate("1.5", "2.25", "add") == "3.75"


def test_mul_by_zero():
    assert calculate("123", "0", "mul") == "0"


def test_add_negatives():
    assert calculate("-5", "-3", "add") == "-8"


# --- Ошибки ---

def test_div_by_zero():
    assert calculate("10", "0", "div") == "Ошибка: деление на ноль"


def test_non_numeric_input():
    assert calculate("abc", "3", "add") == "Ошибка: введите корректные числа"


def test_unknown_operation():
    assert calculate("5", "3", "pow") == "Ошибка: неизвестная операция"


# --- Параметризация: один тест — много случаев ---

@pytest.mark.parametrize(
    "num1,num2,op,expected",
    [
        ("1", "1", "add", "2"),
        ("5", "3", "sub", "2"),
        ("4", "5", "mul", "20"),
        ("8", "4", "div", "2"),
        ("0", "0", "mul", "0"),
        ("100", "0", "sub", "100"),
        ("1e2", "1e2", "add", "200"),
    ],
)
def test_calculate_parametrized(num1, num2, op, expected):
    assert calculate(num1, num2, op) == expected