def format_number(num):
    if num >= 10**6:
        return f"{num/10**6:.2f}M"
    elif num >= 10**3:
        return f"{num/10**3:.2f}k"
    else:
        return f"{num:.2f}"


def find_csymbol_by_address(config, address):
    address_lower = address.lower()
    for key, value in config.items():
        if value["address"].lower() == address_lower:
            return key
    return None
