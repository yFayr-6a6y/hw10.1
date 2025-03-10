import logging
import functools

def log(filename=None):
    """
      Декоратор для логирования вызовов функций, их результатов и возникающих исключений.

      Args:
          filename (str, optional): Имя файла для записи логов. Если не указано, логи выводятся в консоль.

      Returns:
          callable: Декоратор, который оборачивает функцию и добавляет логирование.
      """
    def decorator(func):
        """
               Внутренний декоратор, выполняющий логирование.

               Args:
                   func (callable): Функция, которую необходимо залогировать.

               Returns:
                   callable: Обернутая функция с добавленным логированием.
               """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
                        Обертка для функции, выполняющая логирование до и после ее вызова.

                        Args:
                            *args: Позиционные аргументы функции.
                            **kwargs: Именованные аргументы функции.

                        Returns:
                            любой: Результат вызова функции.

                        Raises:
                            Exception: Если в функции происходит исключение, оно логируется и перевыбрасывается.
                        """
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

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

@log()
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Не может быть нулем")
    return a / b

my_function(1, 2)
divide(4, 2)
divide(5, 0)