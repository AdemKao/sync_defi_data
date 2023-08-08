
'''
function : collect
https://etherscan.io/token/0xc36442b4a4522e871399cd717abdd847ab11fe88#readProxyContract
'''

import os
import time
from dotenv import load_dotenv
from web3 import Web3
import json
from types import SimpleNamespace
from uniswap import UniSwap, UniSwapGraphQL


# current_directory = os.getcwd()
# # print("Current Directory:", current_directory)

# path = current_directory + '/modules/uniswap/config.json'
# with open(path, 'r') as config_file:
#     config_data = json.load(config_file)

# config = SimpleNamespace(**config_data)

# w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
# w3.is_connected()

# # CONST
# MAX = 340282366920938463463374607431768211455

# userAddr = "0x97112D1126D140832AD889e57f0fa46F695Fe67D"
# # tokenId = 544728
# tokenId = 544729

# "https://app.uniswap.org/#/pool/{tokenId}"
# print("User Address : ", userAddr)
# print("User tokenId : ", tokenId)

# contract = w3.eth.contract(
#     abi=config.manager["abi"], address=Web3.to_checksum_address(config.manager["address"]))

# params = {"tokenId": tokenId, "recipient": userAddr,
#           "amount0Max": "0", "amount1Max": "0"}

# # Collect get earn fees
# data = contract.functions.collect(
#     (tokenId, userAddr, MAX, MAX)).call()
# print("contract data: ", data)


userAddr = "0x97112D1126D140832AD889e57f0fa46F695Fe67D"
# # tokenId = 544728
# tokenId = 544729
uniSwap = UniSwap()

# region Singl Test
# print(
#     uniSwap.get_collect_by_id(tokenId, userAddr)
# )
# print(
#     uniSwap.get_ids_by_address(userAddr)
# )
# print('=============START=============')
# start_time = time.time()

# print(
#     uniSwap._get_collects_by_address(userAddr)
# )
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"excute time：{execution_time} s")
# print('=============END=============')
# endregion

print('=============UniSwap Pool START=============')
print('user address: ', userAddr)
start_time = time.time()

# print(
#     uniSwap.get_collects_by_address(userAddr)
# )
print(
    json.dumps(uniSwap.get_collects_by_address(userAddr), indent=4)
)
end_time = time.time()
execution_time = end_time - start_time
print(f"excute time：{execution_time} s")
print('=============UniSwap Pool END=============')


# region UniSwapGraphQL Test
# print('=============UniSwapGraphQL START=============')
# graphQL = UniSwapGraphQL()
# # res = graphQL.query(query)
# res = graphQL.get_ids_by_address(userAddr)

# print(json.dumps(res, indent=4))
# print('=============UniSwapGraphQL END=============')
# endregion

# region Calc Amounts Test
# print('=============Calc Amounts Test=============')

# liquidity = 3491740779210933683336
# sqrt_price_x96 = 620795193149751304125488202
# tick_low = -102780
# tick_high = -97440
# decimal0 = 18
# decimal1 = 18

# data = uniSwap.get_token_amounts(liquidity, sqrt_price_x96,
#                                  tick_low, tick_high, decimal0, decimal1)
# print(data)
# print('=============Calc Amounts END=============')
# endregion
