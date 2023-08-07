import os
import time
from dotenv import load_dotenv
from web3 import Web3
import json
from types import SimpleNamespace
from dto import LoanData, transform_loan_data, serialize_loan_data

current_directory = os.getcwd()
# print("Current Directory:", current_directory)

path = current_directory + '/modules/compound/config.json'
with open(path, 'r') as config_file:
    config_data = json.load(config_file)


config = SimpleNamespace(**config_data)


# load_dotenv()

# infura_id = os.environ.get("INFURA_PROJECT_ID")
# eth_rpc_url = os.environ.get("ETH_RPC_URL")


# rpc_url = eth_rpc_url +  infura_id
# print("rpc_url:",rpc_url)

# w3 = Web3(Web3.HTTPProvider(rpc_url))

w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
w3.is_connected()

userAddr = "0xCB1096E77d6eAb734ffCEced1Fcd2D35EE6b8d15"
ZERO_ADDR = "0x0000000000000000000000000000000000000000"
print("User Address : ", userAddr)

# region roll
# 1. balanceOf : the wallet balance  of cToken
# 2. balanceOfUnderlying : the wallet support to compoundV2 balance
# 3. decimals : the token decimals
# endregion


# region cETH
cEthContract = w3.eth.contract(
    abi=config.cEthAbi, address=Web3.to_checksum_address(config.cEth["address"]))

data = cEthContract.functions.balanceOf(userAddr).call()

print('=============START=============')
start_time = time.time()

# decimals = cEthContract.functions.decimals().call()
decimals = 8
print("cEthContract decimals: ", decimals)
data = cEthContract.functions.balanceOf(userAddr).call()
print("cEthContract balanceOf: ", data, data / 10 ** decimals)
data = cEthContract.functions.balanceOfUnderlying(userAddr).call()
print("cEthContract Underlying(Supply token): ", data, data/1e18)

end_time = time.time()
execution_time = end_time - start_time
print(f"excute time：{execution_time} s")
print('=============END=============')

# endregion

# region cERC - Bat

cErcContract = w3.eth.contract(
    abi=config.cErc20Abi, address=Web3.to_checksum_address(config.cBat["address"]))

print('=============START=============')
decimals = cErcContract.functions.decimals().call()
print("cErcContract decimals: ", decimals)
data = cErcContract.functions.balanceOf(userAddr).call()
print("cErcContract balanceOf: ", data, data / 10 ** decimals)
data = cErcContract.functions.balanceOfUnderlying(userAddr).call()
token_decimals = config.bat["decimals"]
print("cErcContract Underlying(Supply token): ",
      data, data / 10 ** token_decimals)


print('=============END=============')
print('=============Borrow=============')
cErcContract = w3.eth.contract(
    abi=config.cErc20Abi, address=Web3.to_checksum_address(config.cUsdc["address"]))
data = cErcContract.functions.borrowBalanceCurrent(userAddr).call()
print("cErcContract Borrow: ", data)

print('=============END=============')
# endregion


# region DEFI SAVER CONTRACT
'''
contract : defisaver.json
'''

print('=============DEFI SAVER CONTRACT============')

path = current_directory + '/modules/compound/defisaver.json'
with open(path, 'r') as config_file:
    config_data = json.load(config_file)

config = SimpleNamespace(**config_data)

print('*************COMP V2 START************')
start_time = time.time()
comV2Contract = w3.eth.contract(
    abi=config.compView["abi"], address=Web3.to_checksum_address(config.compView["address"]))
loanData = comV2Contract.functions.getLoanData(userAddr).call()
# struct LoanData {
#     address user;
#     uint128 ratio;
#     address[] collAddr;
#     address[] borrowAddr;
#     uint[] collAmounts;
#     uint[] borrowAmounts;
# }

# print('loanData', loanData)
# region format

transformed_data = transform_loan_data(loanData)
loan_json = serialize_loan_data(transformed_data)
print('loan', transformed_data)
# print('loan', loan_json)
end_time = time.time()
execution_time = end_time - start_time
print(f"excute time：{execution_time} s")
print('*************END****************')

# endregion

collAddr = loanData[2]
borrowsAddr = loanData[3]
print('*****************************')
# print('collAddr', collAddr)
print('*****************************')
# print('borrowsAddr', borrowsAddr)
print('*****************************')

# region struct

#  struct TokenInfoFull {
#         address underlyingTokenAddress;
#         uint supplyRate;
#         uint borrowRate;
#         uint exchangeRate;
#         uint marketLiquidity;
#         uint totalSupply;
#         uint totalBorrow;
#         uint collateralFactor;
#         uint price;
#         uint compBorrowSpeeds;
#         uint compSupplySpeeds;
#         uint borrowCap;
#         bool canMint;
#         bool canBorrow;
#     }

# struct TokenInfo {
#     address cTokenAddress;
#     address underlyingTokenAddress;
#     uint collateralFactor;
#     uint price;
# }
# endregion


filtered_list = [address for address in borrowsAddr if address != ZERO_ADDR]
collsInfo = comV2Contract.functions.getFullTokensInfo(filtered_list).call()
# print('collsInfo', collsInfo)
print('*****************************')
print('*****************************')
filtered_list = [address for address in borrowsAddr if address != ZERO_ADDR]
# borrowsInfo = comV2Contract.functions.getFullTokensInfo(filtered_list).call()
borrowsInfo = comV2Contract.functions.getTokensInfo(filtered_list).call()
print('borrowsInfo', borrowsInfo)
cUsdcInfo = comV2Contract.functions.getTokensInfo(
    [Web3.to_checksum_address('0x39aa39c021dfbae8fac545936693ac917d5e7563')]).call()
print('cUsdcInfo', cUsdcInfo)
cEthInfo = comV2Contract.functions.getTokensInfo(
    [Web3.to_checksum_address('0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5')]).call()
print('cEthInfo', cEthInfo)
cUniInfo = comV2Contract.functions.getTokensInfo(
    [Web3.to_checksum_address("0x35A18000230DA775CAc24873d00Ff85BccdeD550")]).call()
print('cUniInfo', cUniInfo)

# # getTokensInfo(cToken[])
# testInfo = comV2Contract.functions.getTokensInfo(
#     ["0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E"]).call()
# print('testInfo', testInfo)
print('*************COMP V2 END************')


print('=============END============')

# endregion
