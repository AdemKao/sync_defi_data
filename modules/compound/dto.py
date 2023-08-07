import json
import os

from utils import format_number, find_csymbol_by_address


class LoanData:
    def __init__(self, user, ratio, collAddr, borrowAddr, collAmounts, borrowAmounts):
        self.user = user
        self.ratio = ratio
        self.collAddr = collAddr
        self.borrowAddr = borrowAddr
        self.collAmounts = collAmounts
        self.borrowAmounts = borrowAmounts


def transform_loan_data(loanData):
    ZERO_ADDR = "0x0000000000000000000000000000000000000000"
    current_directory = os.getcwd()
    # print("Current Directory:", current_directory)
    config_path = current_directory + '/modules/compound/tokenConfig.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    loan = LoanData(*loanData)
    loan.collAddr = [addr for addr in loan.collAddr if addr != ZERO_ADDR]
    loan.borrowAddr = [addr for addr in loan.borrowAddr if addr != ZERO_ADDR]
    loan.collAmounts = [amount for amount in loan.collAmounts if amount != 0]
    loan.borrowAmounts = [
        amount for amount in loan.borrowAmounts if amount != 0]

    coll_data = []
    borrow_data = []

    for i in range(len(loan.collAddr)):
        csymbol = find_csymbol_by_address(config, loan.collAddr[i])

        coll_data.append({
            "cAddr": loan.collAddr[i],
            "cDecimals": "",
            "cSymbol": csymbol,
            "cAmounts_$": str(loan.collAmounts[i]),
            "cAmountsUsd": format_number(int(loan.collAmounts[i])/10**18),
            "addr": "",
            "decimals": "",
            "amounts_$": "0"
        })

    for i in range(len(loan.borrowAddr)):
        symbol = find_csymbol_by_address(config, loan.borrowAddr[i])

        borrow_data.append({
            "cAddr": "",
            "cDecimals": "",
            "cAmounts_$": "0",
            "addr": loan.borrowAddr[i],
            "decimals": "",
            "symbol": symbol,
            "amounts_$": str(loan.borrowAmounts[i]),
            "amountsUsd": format_number(int(loan.borrowAmounts[i])/10**18)
        })

    result = {
        "user": loan.user,
        "coll": coll_data,
        "borrow": borrow_data,
        "raw": loan
    }

    return result


def serialize_loan_data(loanData):
    def default(obj):
        if isinstance(obj, LoanData):
            return {
                "user": obj.user,
                "ratio": obj.ratio,
                "collAddr": obj.collAddr,
                "borrowAddr": obj.borrowAddr,
                "collAmounts": obj.collAmounts,
                "borrowAmounts": obj.borrowAmounts
            }
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    return json.dumps(loanData, default=default, indent=4)
