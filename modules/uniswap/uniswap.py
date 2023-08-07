
import asyncio
import math
import requests
import os
from dotenv import load_dotenv
from web3 import Web3
import json
from types import SimpleNamespace


class UniSwap:

    def __init__(self) -> None:
        current_directory = os.getcwd()
        path = current_directory + '/modules/uniswap/config.json'
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)

        w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        w3.is_connected()
        self.config = SimpleNamespace(**config_data)
        self.contract = w3.eth.contract(
            abi=self.config.manager["abi"], address=Web3.to_checksum_address(self.config.manager["address"]))

        self.MAX = 340282366920938463463374607431768211455
        self.Q96 = 2 ** 96

        self.graph = UniSwapGraphQL()

    def generate_Dto(self, rewards, balances_data, graphOb):
        ethPriceUSD = graphOb["bundles"][0]["ethPriceUSD"]
        positions = graphOb["positions"]
        Dto = []
        for index, reward in enumerate(rewards):
            token0 = positions[index]["token0"]
            token1 = positions[index]["token1"]
            balance = balances_data[index]
            # if (reward[0] == 0 & reward[1] == 0):
            #     continue
            _dto = {
                "id": index + 1,
                "tokenId": positions[index]["id"],
                # "liquidity": positions[index]["liquidity"],
                # "tickUpper": positions[index]["tickUpper"],
                # "tickLower": positions[index]["tickLower"],
                "balances": [
                    {
                        "id": 1,
                        "address": token0["id"],
                        "name":token0["name"],
                        "symbol":token0["symbol"],
                        "decimals":token0["decimals"],
                        "amounts":balance[0],
                        "amounts_format":balance[2],
                        "amountsUsd":'{:.18f}'.format(float(balance[2])*float(ethPriceUSD)),
                    },
                    {
                        "id": 2,
                        "address": token1["id"],
                        "name":token1["name"],
                        "symbol":token1["symbol"],
                        "decimals":token1["decimals"],
                        "amounts":balance[1],
                        "amounts_format":balance[3],
                        "amountsUsd":'{:.18f}'.format(float(balance[3])*float(ethPriceUSD)),
                    }
                ],
                "rewards": [
                    {
                        "id": 1,
                        "address": token0["id"],
                        "name":token0["name"],
                        "symbol":token0["symbol"],
                        "decimals":token0["decimals"],
                        "amounts":reward[0],
                        "amounts_format":'{:.18f}'.format(float(reward[0])/10**int(token0["decimals"])),
                        "amountsUsd":'{:.18f}'.format(float(reward[0])*float(token0["derivedETH"])*float(ethPriceUSD)/10**int(token0["decimals"])),
                        "priceUsd":'{:.18f}'.format(float(token0["derivedETH"])*float(ethPriceUSD))
                    },
                    {
                        "id": 2,
                        "address": token1["id"],
                        "name":token1["name"],
                        "symbol":token1["symbol"],
                        "decimals":token1["decimals"],
                        "amounts":reward[1],
                        "amounts_format":'{:.18f}'.format(float(reward[1])/10**int(token1["decimals"])),
                        "amountsUsd":'{:.18f}'.format(float(reward[1])*float(token1["derivedETH"])*float(ethPriceUSD)/10**int(token1["decimals"])),
                        "priceUsd":'{:.18f}'.format(float(token1["derivedETH"])*float(ethPriceUSD))
                    }
                ],
                "tokens": [
                    {
                        "id": 1,
                        "address": token0["id"],
                        "name":token0["name"],
                        "symbol":token0["symbol"],
                        "decimals":token0["decimals"],
                        "priceUsd":'{:.18f}'.format(float(token0["derivedETH"])*float(ethPriceUSD))
                    },
                    {
                        "id": 2,
                        "address": token1["id"],
                        "name":token1["name"],
                        "symbol":token1["symbol"],
                        "decimals":token1["decimals"],
                        "priceUsd":'{:.18f}'.format(float(token1["derivedETH"])*float(ethPriceUSD))
                    }
                ],
                "ethPriceUSD": ethPriceUSD
            }
            Dto.append(_dto)

        return Dto

    def get_ids_by_address(self, address):
        return self.graph.get_ids_by_address(address)

    async def async_get_collect_by_id(self, id, userAddr):
        # Collect get earn fees
        data = self.contract.functions.collect(
            (id, userAddr, self.MAX, self.MAX)).call()
        return data

    async def async_get_collects_by_address(self, userAddr):
        collected_data = []
        graphOb = self.get_ids_by_address(userAddr)
        # for nft in nfts:
        #     collected_data.append(
        #         asyncio.run(self.get_collect_by_id(int(nft["id"]), userAddr)))

        # return collected_data
        tasks = [self.async_get_collect_by_id(
            int(position["id"]), userAddr) for position in graphOb["positions"]]
        collected_data = await asyncio.gather(*tasks)
        balances_data = self.get_tokens_balances(graphOb["positions"])
        return self.generate_Dto(collected_data, balances_data, graphOb)
        # return collected_data

    def get_tokens_balances(self, positions):
        balances = []
        for position in positions:
            liquidity = position["liquidity"]
            sqrt_price_x96 = position["tickLower"]["pool"]["sqrtPrice"]
            tick_low = position["tickLower"]["tickIdx"]
            tick_high = position["tickUpper"]["tickIdx"]
            decimal0 = position["token0"]["decimals"]
            decimal1 = position["token1"]["decimals"]
            balances.append(self.get_token_amounts(
                liquidity, sqrt_price_x96, tick_low, tick_high, decimal0, decimal1))
        return balances

    # For Out Side
    def get_collects_by_address(self, userAddr):
        loop = asyncio.get_event_loop()
        collected_data = loop.run_until_complete(
            self.async_get_collects_by_address(userAddr))
        return collected_data

    def _get_collect_by_id(self, id, userAddr):
        # Collect get earn fees
        data = self.contract.functions.collect(
            (id, userAddr, self.MAX, self.MAX)).call()
        return data

    def _get_collects_by_address(self, userAddr):
        collected_data = []
        nfts = self.get_ids_by_address(userAddr)
        for nft in nfts:
            collected_data.append(
                self._get_collect_by_id(int(nft["id"]), userAddr))

        return collected_data

    # TODO
    def get_stake_by_address(self, userAddr):
        return

    def get_tick_at_sqrt_price(self, sqrt_price_x96):
        tick = math.floor(
            math.log((sqrt_price_x96 / self.Q96) ** 2) / math.log(1.0001))
        return tick

    def get_token_amounts(self, liquidity, sqrt_price_x96, tick_low, tick_high, decimal0, decimal1):
        liquidity = float(liquidity)
        sqrt_price_x96 = float(sqrt_price_x96)
        tick_low = float(tick_low)
        tick_high = float(tick_high)
        decimal0 = int(decimal0)
        decimal1 = int(decimal1)
        sqrt_ratio_a = math.sqrt(1.0001 ** tick_low)
        sqrt_ratio_b = math.sqrt(1.0001 ** tick_high)
        current_tick = self.get_tick_at_sqrt_price(sqrt_price_x96)
        sqrt_price = sqrt_price_x96 / self.Q96
        amount0 = 0
        amount1 = 0

        if current_tick < tick_low:
            amount0 = math.floor(
                liquidity * ((sqrt_ratio_b - sqrt_ratio_a) / (sqrt_ratio_a * sqrt_ratio_b)))
        elif current_tick >= tick_high:
            amount1 = math.floor(liquidity * (sqrt_ratio_b - sqrt_ratio_a))
        elif tick_low <= current_tick < tick_high:
            amount0 = math.floor(
                liquidity * ((sqrt_ratio_b - sqrt_price) / (sqrt_price * sqrt_ratio_b)))
            amount1 = math.floor(liquidity * (sqrt_price - sqrt_ratio_a))

        amount0_human = round(amount0 / (10 ** decimal0), decimal0)
        amount1_human = round(amount1 / (10 ** decimal1), decimal1)

        # print("Amount Token0 in lowest decimal:", amount0)
        # print("Amount Token1 in lowest decimal:", amount1)
        # print("Amount Token0:", amount0_human)
        # print("Amount Token1:", amount1_human)
        return [amount0, amount1, amount0_human, amount1_human]


class UniSwapGraphQL:
    def __init__(self):
        self.url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

    def get_ids_by_address(self, address):
        content = f'''
        {{
          positions(where:{{owner:"{address}"
          # id:544728,
          liquidity_not:0,
          token0_not_in:["0xcb50350ab555ed5d56265e096288536e8cac41eb",
                          "0x72e4f9f808c49a2a61de9c5896298920dc4eeea9",
                          "0x3d806324b6df5af3c1a81acba14a8a62fe6d643f"]
          }}){{
            id,
            liquidity,
  	        tickLower{{
                tickIdx
                pool {{
                    id
                    liquidity
                    sqrtPrice
                }}
            }}
            tickUpper{{
                tickIdx
                pool {{
                    id
                    liquidity
                    sqrtPrice
                }}
            }}
            token0 {{
                id
                name
                symbol
                decimals
                derivedETH
            }}
            token1 {{
                id
                name
                symbol
                decimals
                derivedETH
            }}
          }}
          bundles(first: 1){{
            ethPriceUSD
          }}
        }}
        '''
        return self._query(content)["data"]

    def _query(self, query):
        response = requests.post(self.url, json={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            return {"errMsg": response.text, "code": response.status_code}
