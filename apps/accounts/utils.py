"""accounts utils functions"""

import shortuuid

GENDER = (
    ("MASCULINO", "MASCULINO"),
    ("FEMININO", "FEMININO"),
)

GENDER_DIC = {"MASCULINO": "MASCULINO", "FEMININO": "FEMININO"}

TYPE_USER = (
    ("admin", "admin"),
    ("normal", "normal"),
)


def generate_otp(length=12) -> str:
    """otp code generator"""
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]


def generate_short_id(length=6) -> str:
    """short_id generator"""
    uuid_key = shortuuid.uuid()
    return uuid_key[:length]


def deb(message: str = "") -> None:
    """debug function"""
    print("#" * 100)
    print(message or f"{'Chamou': ^100}")
    print("#" * 100)
