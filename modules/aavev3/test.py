
import asyncio
import json
import time
from aavev3 import AaveV3


aaveV3 = AaveV3()

market = "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e"

# userAddr = "0x945d5bcda8dcd9cd8b221fd23cf4b6c0e7e50bd5"
print('=============AaveV3 START=============')
userAddr = "0xD14f076044414C255D2E82cceB1CB00fb1bBA64c"
print('user address: ', userAddr)
start_time = time.time()
# data = aaveV3.public_get_loan_data(market, userAddr)
data = aaveV3.public_get_loan_data(userAddr)

end_time = time.time()
execution_time = end_time - start_time

print('data', json.dumps(data, indent=3))

print(f"excute time：{execution_time} s")
print('=============AaveV3 END=============')


# print('=============AaveV3 SIGLE TEST START=============')
# userAddr = "0xD14f076044414C255D2E82cceB1CB00fb1bBA64c"
# print('user address: ', userAddr)

# print('************loan_data**************')
# start_time = time.time()
# loan_data = aaveV3.private_get_loan_data(market, userAddr)
# merged_addrs = aaveV3.private_merge_tokens_address(loan_data)

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"excute time：{execution_time} s")
# print('**************************')
# print('************tokens_data**************')
# start_time = time.time()
# loop = asyncio.get_event_loop()
# tokens_data = loop.run_until_complete(
#     aaveV3.private_async_get_tokens_info(market, merged_addrs))

# end_time = time.time()
# execution_time = end_time - start_time
# print(f"excute time：{execution_time} s")
# print('**************************')

# print('=============AaveV3 END=============')
