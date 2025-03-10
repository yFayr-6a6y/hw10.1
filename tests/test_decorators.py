import pytest
import logging
import functools



def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info(f"Функция '{func_name}' начата")

            try:
                result = func(*args, **kwargs)
                logging.info(f"Функция '{func_name}' окончена, результат: {result}")
                return result
            except Exception as e:
                logging.basicConfig(filename=filename, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.error(f"Ошибка в функции '{func_name}' Ошибка: {type(e).__name__}. Вводные данные: {args}, {kwargs}")
                raise
        return wrapper
    return decorator


def test_logsuccess_console(captured_output):
    @log
    def add(x, y): return x + y
    assert add(2, 3) == 5
    output = captured_output.getvalue()
    assert "Функция 'add' начата" in output
    assert "Функция 'add' окончена, результат: 5" in output

def test_logerror_console(captured_output):
    @log
    def divide(x, y): return x / y
    with pytest.raises(ZeroDivisionError): divide(5, 0)
    output = captured_output.getvalue()
    assert "Функция 'divide' начата" in output
    assert "Ошибка в функции 'divide' Ошибка: ZeroDivisionError" in output
    assert "Функция 'divide' окончена" not in output

def test_logpreserves_function_name():
    @log
    def greet(): pass
    assert greet.__name__ == "greet"