def check_cnpj_mask(c: str):
    if len(c) == 18:
        nums = [c[:2], c[3:6], c[7:10], c[11:15], c[16:18]]

        if c[2] == "." and c[6] == "." and c[10] == "/" and c[15] == "-":
            for x in nums:
                if not x.isnumeric():
                    return False

            return True

    return False
