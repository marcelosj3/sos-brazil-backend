import re

from sos_brazil.exceptions import InvalidFormatException


def check_cnpj_mask(cnpj: str):
    pattern = "^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$"

    if not re.findall(pattern, cnpj):
        raise InvalidFormatException(
            {
                "error": "Invalid CNPJ format.",
                "expected_format": "XX.XXX.XXX/XXXX-XX",
            }
        )

    return True
