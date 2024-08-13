import logging

logger = logging.getLogger('mask')
file_handler = logging.FileHandler('logs/mask.log')
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')


def get_mask_card_number(card_number: int) -> str:
    """Принимает на вход номер карты и возвращает ее маску."""
    card_n = str(card_number)
    # mask_card_number = card_n[:4] + " " + card_n[4:6]
    # + "** **** " + card_n[-4:]
    logger.info(f"Card mask:"
                f" {card_n[:4]} " f"" f"" f"{card_n[4:6]}"
                f"** ****" f" {card_n[-4:]}")
    return f"{card_n[:4]} {card_n[4:6]}** ****" f" {card_n[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Принимает на вход номер счета и возвращает его маску."""
    account_n = str(account_number)
    # mask_account_number = "**" + account_n[-4:]
    logger.info(f"Account mask: **{account_n[-4:]}")
    return f"**{account_n[-4:]}"
