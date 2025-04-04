import logging
import os

logger = logging.getLogger('masks')
logger.setLevel(logging.INFO)

logger.handlers = []

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

if os.path.exists(log_dir) and not os.path.isdir(log_dir):
    raise FileExistsError(f"Путь {log_dir} существует, но это не папка")
elif not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'masks.log')
handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - masks - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def get_mask_card_number(card_number: int) -> str:
    """Маскирует номер карты (предполагается 16 цифр)."""
    logger.info(f"Начало маскировки номера карты: {card_number}")
    if not isinstance(card_number, int):
        logger.error(f"Номер карты должен быть целым числом, получено: {type(card_number)}")
        raise TypeError("номер карты должен быть целым числом")
    card_str = str(card_number).zfill(16)
    masked_number = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    logger.info(f"Номер карты успешно замаскирован: {masked_number}")
    return masked_number

def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета (предполагается 20 цифр)."""
    logger.info(f"Начало маскировки номера счета: {account_number}")
    if not isinstance(account_number, str):
        logger.error(f"Номер счета должен быть строкой, получено: {type(account_number)}")
        raise TypeError("номер счета должен быть строкой")
    if not account_number.isdigit():
        logger.error(f"Номер счета должен содержать только цифры, получено: {account_number}")
        raise ValueError("номер счета должен содержать только цифры")
    if len(account_number) != 20:
        logger.warning(f"Длина номера счета должна быть 20 символов, получено: {len(account_number)} символов")
    masked_account = f"**{account_number[-4:]}"
    logger.info(f"Номер счета успешно замаскирован: {masked_account}")
    return masked_account