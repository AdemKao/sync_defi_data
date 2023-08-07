from web3 import Web3, EthereumTesterProvider

w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))

w3.is_connected()
abi =[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralBase","type":"uint256"},{"internalType":"uint256","name":"totalDebtBase","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsBase","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"}]
pool = w3.eth.contract(abi=abi,address="0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2")
user = "0x8F564c7272177663309F704065fFB59F403d96a1"

#
# totalCollateralBase
#
# uint256
#
# total collateral of the user, in market’s base currency 总抵押价值 usd计价 精度8
#
# totalDebtBase
#
# uint256
#
# total debt of the user, in market’s base currency 总贷款价值 usd计价 精度8
#
# availableBorrowsBase
#
# uint256
#
# borrowing power left of the user, in market’s base currency 剩余可贷款价值 usd计价 精度8
#
# currentLiquidationThreshold
#
# uint256
#
# liquidation threshold of the user
#
# 爆仓门槛（除以10000是百分比）
#
# ltv
#
# uint256
#
# Loan To Value of the user
#
# 最大贷款价值（除以10000是百分比）
#
# healthFactor
#
# uint256
#
# current health factor of the user
#
# 健康数值小于1会被清算（18位精度）
accountData = pool.functions.getUserAccountData(user).call()

abi = [{"inputs":[{"internalType":"contract IPoolAddressesProvider","name":"provider","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"getUserReservesData","outputs":[{"components":[{"internalType":"address","name":"underlyingAsset","type":"address"},{"internalType":"uint256","name":"scaledATokenBalance","type":"uint256"},{"internalType":"bool","name":"usageAsCollateralEnabledOnUser","type":"bool"},{"internalType":"uint256","name":"stableBorrowRate","type":"uint256"},{"internalType":"uint256","name":"scaledVariableDebt","type":"uint256"},{"internalType":"uint256","name":"principalStableDebt","type":"uint256"},{"internalType":"uint256","name":"stableBorrowLastUpdateTimestamp","type":"uint256"}],"internalType":"struct IUiPoolDataProviderV3.UserReserveData[]","name":"","type":"tuple[]"},{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IPoolAddressesProvider","name":"provider","type":"address"}],"name":"getReservesData","outputs":[{"components":[{"internalType":"address","name":"underlyingAsset","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"decimals","type":"uint256"},{"internalType":"uint256","name":"baseLTVasCollateral","type":"uint256"},{"internalType":"uint256","name":"reserveLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"reserveLiquidationBonus","type":"uint256"},{"internalType":"uint256","name":"reserveFactor","type":"uint256"},{"internalType":"bool","name":"usageAsCollateralEnabled","type":"bool"},{"internalType":"bool","name":"borrowingEnabled","type":"bool"},{"internalType":"bool","name":"stableBorrowRateEnabled","type":"bool"},{"internalType":"bool","name":"isActive","type":"bool"},{"internalType":"bool","name":"isFrozen","type":"bool"},{"internalType":"uint128","name":"liquidityIndex","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"liquidityRate","type":"uint128"},{"internalType":"uint128","name":"variableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"stableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint256","name":"availableLiquidity","type":"uint256"},{"internalType":"uint256","name":"totalPrincipalStableDebt","type":"uint256"},{"internalType":"uint256","name":"averageStableRate","type":"uint256"},{"internalType":"uint256","name":"stableDebtLastUpdateTimestamp","type":"uint256"},{"internalType":"uint256","name":"totalScaledVariableDebt","type":"uint256"},{"internalType":"uint256","name":"priceInMarketReferenceCurrency","type":"uint256"},{"internalType":"address","name":"priceOracle","type":"address"},{"internalType":"uint256","name":"variableRateSlope1","type":"uint256"},{"internalType":"uint256","name":"variableRateSlope2","type":"uint256"},{"internalType":"uint256","name":"stableRateSlope1","type":"uint256"},{"internalType":"uint256","name":"stableRateSlope2","type":"uint256"},{"internalType":"uint256","name":"baseStableBorrowRate","type":"uint256"},{"internalType":"uint256","name":"baseVariableBorrowRate","type":"uint256"},{"internalType":"uint256","name":"optimalUsageRatio","type":"uint256"},{"internalType":"bool","name":"isPaused","type":"bool"},{"internalType":"bool","name":"isSiloedBorrowing","type":"bool"},{"internalType":"uint128","name":"accruedToTreasury","type":"uint128"},{"internalType":"uint128","name":"unbacked","type":"uint128"},{"internalType":"uint128","name":"isolationModeTotalDebt","type":"uint128"},{"internalType":"bool","name":"flashLoanEnabled","type":"bool"},{"internalType":"uint256","name":"debtCeiling","type":"uint256"},{"internalType":"uint256","name":"debtCeilingDecimals","type":"uint256"},{"internalType":"uint8","name":"eModeCategoryId","type":"uint8"},{"internalType":"uint256","name":"borrowCap","type":"uint256"},{"internalType":"uint256","name":"supplyCap","type":"uint256"},{"internalType":"uint16","name":"eModeLtv","type":"uint16"},{"internalType":"uint16","name":"eModeLiquidationThreshold","type":"uint16"},{"internalType":"uint16","name":"eModeLiquidationBonus","type":"uint16"},{"internalType":"address","name":"eModePriceSource","type":"address"},{"internalType":"string","name":"eModeLabel","type":"string"},{"internalType":"bool","name":"borrowableInIsolation","type":"bool"}],"internalType":"struct IUiPoolDataProviderV3.AggregatedReserveData[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"marketReferenceCurrencyUnit","type":"uint256"},{"internalType":"int256","name":"marketReferenceCurrencyPriceInUsd","type":"int256"},{"internalType":"int256","name":"networkBaseTokenPriceInUsd","type":"int256"},{"internalType":"uint8","name":"networkBaseTokenPriceDecimals","type":"uint8"}],"internalType":"struct IUiPoolDataProviderV3.BaseCurrencyInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]
UiPoolDataProviderV3 = w3.eth.contract(abi=abi, address="0x91c0eA31b49B69Ea18607702c5d9aC360bf3dE7d")

# underlyingAsset
#
# address
#
# Address of the underlying asset supplied/borrowed 抵押或者结出的资金地址
#
# scaledATokenBalance
#
# uint256
#
# scaled balance of aToken scaledBalance = balance/liquidityIndex
#
# atoken的数量
#
# usageAsCollateralEnabledOnUser
#
# bool
#
# true if supplied asset is enabled to be used as collateral
#
# 是否可以用作抵押品
#
# stableBorrowRate
#
# uint256
#
# Stable rate at which underlying asset is borrowed by the user. 0 ⇒ no debt
#
# 稳定借款利率
#
# scaledVariableDebt
#
# uint256
#
# scaled balance of vToken scaledBalance = balance/liquidityIndex
#
# vtoken的数量 债务token
#
# principalStableDebt
#
# uint256
#
# Principal amount borrowed at stable rate
#
# 稳定利率借出的钱
#
# stableBorrowLastUpdateTimestamp
#
# uint256
#
# unix timestamp of last update on user’s stable borrow position.
#
# 稳定利率下用户借钱最后更新的时间戳
userReservesData = UiPoolDataProviderV3.functions.getUserReservesData("0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e",user).call()

reservesData = UiPoolDataProviderV3.functions.getReservesData("0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e").call()

print("User:", user)
print("Aave V3 Total USD Value:", (accountData[0] - accountData[1]) / 1e8 )
print("Aave V3 Total Collateral USD Value:", accountData[0] / 1e8 )
print("Aave V3 Total Debt USD Value:", accountData[1] / 1e8 )
print("Aave V3 Collateral Assets:")

def first(iterable, default=None):
    for item in iterable:
        return item
    return default


# 多个查询操作, 并聚合数据只为展示原理
# 更优化的方式是通过智能合约一次性查询, 并完成等效于聚合操作的逻辑
for a in userReservesData[0]:
    address = a[0]
    if(a[1]==0): continue
    info = first(x for x in reservesData[0] if x[0]==address)
    print(info[1],':\t', a[1]/10**info[3], '\tUSD Value =',a[1]*info[28]/10**(info[3]+8),'\tasCollateral =',a[2])

print("Aave V3 Debt Assets:")

for a in userReservesData[0]:
    address = a[0]
    if (a[4] == 0): continue
    info = first(x for x in reservesData[0] if x[0] == address)
    print(info[1], ':\t', a[4] / 10 ** info[3], '\tUSD Value =', a[4] * info[28] / 10 ** (info[3] + 8))
# Output Demo
# User: 0x8F564c7272177663309F704065fFB59F403d96a1
# Aave V3 Total USD Value: 145777.85381129
# Aave V3 Total Collateral USD Value: 299994.30233586
# Aave V3 Total Debt USD Value: 154216.44852457
# Aave V3 Collateral Assets:
# Wrapped Ether :  78.79882006611064      USD Value = 148582.61067003736  asCollateral = True
# Wrapped BTC :    4.88537472     USD Value = 149904.22669759687  asCollateral = True
# Aave V3 Debt Assets:
# Wrapped BTC :    0.00556533     USD Value = 170.76816780329528
# USD Coin :       32198.733216   USD Value = 32196.514401294084
# Tether USD :     48011.779223   USD Value = 48009.88275772069
# Curve DAO Token :        87520.68516233844      USD Value = 69754.17249344314





