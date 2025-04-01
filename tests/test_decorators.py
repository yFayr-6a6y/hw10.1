import pytest
import logging
import functools
import sys


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            # Настраиваем логирование
            logger = logging.getLogger(func_name)
            logger.setLevel(logging.INFO)

            # Удаляем все существующие обработчики, чтобы избежать дублирования
            logger.handlers = []

            # Если filename указан, пишем в файл
            if filename:
                handler = logging.FileHandler(filename)
            else:
                # Иначе пишем в stdout
                handler = logging.StreamHandler(sys.stdout)

            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logger.addHandler(handler)

            logger.info(f"Функция '{func_name}' начата")

            try:
                result = func(*args, **kwargs)
                logger.info(f"Функция '{func_name}' окончена, результат: {result}")
                return result
            except Exception as e:
                # Настраиваем логирование для ошибок
                logger.setLevel(logging.ERROR)
                logger.error(
                    f"Ошибка в функции '{func_name}' Ошибка: {type(e).__name__}. Вводные данные: {args}, {kwargs}")
                raise
            finally:
                # Удаляем обработчик, чтобы не мешать другим тестам
                logger.handlers = []

        return wrapper

    return decorator


def test_logsuccess_console(capsys):
    @log()
    def add(x, y):
        return x + y

    assert add(2, 3) == 5
    captured = capsys.readouterr()
    output = captured.out
    assert "Функция 'add' начата" in output
    assert "Функция 'add' окончена, результат: 5" in output


def test_logerror_console(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
    captured = capsys.readouterr()
    output = captured.out
    assert "Функция 'divide' начата" in output
    assert "Ошибка в функции 'divide' Ошибка: ZeroDivisionError" in output
    assert "Функция 'divide' окончена" not in output


def test_logpreserves_function_name():
    @log()
    def greet():
        pass

    assert greet.__name__ == "greet"