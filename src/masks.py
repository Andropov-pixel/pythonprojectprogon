import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename="../logs/mask.log",
    filemode="w",
)

logger = logging.getLogger("mask")
def get_mask_card_number(card_number: int) -> str:
    """Принимает на вход номер карты и возвращает ее маску."""
    card_n = str(card_number)
    # mask_card_number = card_n[:4] + " " + card_n[4:6] + "** **** " + card_n[-4:]
    logger.info(f"Card mask: {card_n[:4]} {card_n[4:6]}** **** {card_n[-4:]}")
    return f"{card_n[:4]} {card_n[4:6]}** **** {card_n[-4:]}"


def get_mask_account(account_number: int) -> str:
    """Принимает на вход номер счета и возвращает его маску."""
    account_n = str(account_number)
    # mask_account_number = "**" + account_n[-4:]
    logger.info(f"Account mask: **{account_n[-4:]}")
    return f"**{account_n[-4:]}"