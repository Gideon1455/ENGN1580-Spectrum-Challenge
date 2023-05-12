def dec16_to_hex16(value: int) -> str:
    temp = hex(value + 32768)
    temp = '0' * (4 - len(temp)) + temp
    return temp.split('x')[-1]

def hex16_to_dec16(value: str) -> int:
    return int(value, 16) - 32768