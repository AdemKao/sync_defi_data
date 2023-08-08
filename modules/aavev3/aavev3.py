
import asyncio
import json
from dotenv import load_dotenv
import os
from types import SimpleNamespace
from web3 import Web3
from moralis import evm_api

load_dotenv()


class AaveV3:

    def __init__(self) -> None:
        self.zero_address = "0x0000000000000000000000000000000000000000"
        self.defi_saver = DefiSaver()
        self.erc20 = Erc20()
        self.market = "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e"

    # region LoanData
    '''
        struct LoanData {
            address user;
            uint128 ratio;
            uint256 eMode;
            address[] collAddr;
            address[] borrowAddr;
            uint256[] collAmounts;
            uint256[] borrowStableAmounts;
            uint256[] borrowVariableAmounts;
            // emode category data
            uint16 ltv;
            uint16 liquidationThreshold;
            uint16 liquidationBonus;
            address priceSource;
            string label;
        }
    '''
    # endregion

    def private_merge_tokens_address(self, loan_data):
        coll_set = set(addr.lower() for addr in loan_data["collAddr"])
        borrow_set = set(addr.lower() for addr in loan_data["borrowAddr"])
        merged_addresses = list(coll_set.union(borrow_set))
        return merged_addresses

    def private_convert_loan_data_to_dto(self, raw_data):
        return {
            "user": raw_data[0],
            "ratio": raw_data[1],
            "eMode": raw_data[2],
            "collAddr":  [addr.lower() for addr in raw_data[3] if addr != self.zero_address],
            # "collAddr": raw_data[3],
            "borrowAddr": [addr.lower() for addr in raw_data[4] if addr != self.zero_address],
            # "borrowAddr": raw_data[4],
            "collAmounts": [amount for amount in raw_data[5] if amount != 0],
            "borrowStableAmounts": [amount for amount in raw_data[6] if amount != 0],
            "borrowVariableAmounts": [amount for amount in raw_data[7] if amount != 0],
            "ltv": raw_data[8],
            "liquidationThreshold": raw_data[9],
            "liquidationBonus": raw_data[10],
            "priceSource": raw_data[11],
            "label": raw_data[12]
        }

    def private_convert_token_data_to_dto(self, tokens_data, tokens_addr, loan_tokens_data):
        saver_decimals = 8
        for index, addr in enumerate(tokens_addr):
            ob = {"priceUsd": '{:.18f}'.format(
                float(loan_tokens_data[index])/10**saver_decimals)}
            tokens_data[addr.lower()].update(ob)
        return tokens_data

    def private_convert_laon_datas(self, data_addrs, data_amounts, tokens_data):
        dtos = []
        for index, addr in enumerate(data_addrs):
            token_data = tokens_data[addr]
            amountsUsd = float(data_amounts[index])/10**8
            amounts_format = amountsUsd / float(token_data["priceUsd"])
            amounts = amounts_format*10**float(token_data["decimals"])
            dtos.append({
                "id": index+1,
                **token_data,
                "amounts": '{:.0f}'.format(amounts),
                "amounts_format": '{:.18f}'.format(amounts_format),
                "amountsUsd": '{:.18f}'.format(amountsUsd)
            })
        return dtos

    # region //TODO
    # def private_convert_user_balances(self, raw_data, tokens):
    #     saver_decimals =6
    #     tokens_dict = {}
    #     for index,data in enumerate(raw_data):
    #         key = tokens[index].lower()
    #         tokens_dict[key] = {
    #             ""
    #         }
    #     return tokens_dict
    # endregion

    def private_generate_dto(self, loan_data, tokens_data):
        collects = self.private_convert_laon_datas(
            loan_data["collAddr"], loan_data["collAmounts"], tokens_data)
        borrows = self.private_convert_laon_datas(
            loan_data["borrowAddr"], loan_data["borrowVariableAmounts"], tokens_data)
        return {
            "user": loan_data["user"],
            "collects": collects,
            "borrows": borrows,
            "tokens": list(tokens_data.values())
            # ** loan_data,
        }

    def private_get_loan_data(self, market, user_addr):
        market = Web3.to_checksum_address(market)
        user_addr = Web3.to_checksum_address(user_addr)
        raw_data = self.defi_saver.public_get_loan_data(market, user_addr)
        return self.private_convert_loan_data_to_dto(raw_data)

    def private_get_loan_datas(self, market, user_addrs):
        return

    def private_get_token_info(self, token_addr):
        return ''

    async def private_async_get_loan_tokens_price(self, market, merged_addresses):
        tokens_price = self.defi_saver.public_get_prices(
            market, merged_addresses)
        return tokens_price

    async def private_async_get_tokens_data(self, tokens_addr):
        return self.erc20.public_get_tokens_info(tokens_addr)

    async def private_async_get_tokens_info(self, market, tokens_addr):
        tasks = [self.private_async_get_tokens_data(tokens_addr),
                 self.private_async_get_loan_tokens_price(
            market, tokens_addr)]
        tasks_results = await asyncio.gather(*tasks)
        # tokens_data = self.erc20.public_get_tokens_info(tokens_addr)
        # loan_tokens_data = self.private_get_loan_tokens_price(
        #     market, tokens_addr)
        tokens_data = tasks_results[0]
        loan_tokens_data = tasks_results[1]
        return self.private_convert_token_data_to_dto(tokens_data, tokens_addr, loan_tokens_data)

    def private_get_user_balances(self, market, user, tokens):
        raw_data = self.defi_saver.public_get_user_tokens_balance(
            market, user, tokens)
        # return self.private_convert_user_balances(raw_data, tokens)
        return raw_data

    def public_get_loan_data(self, user_addr):
        market = self.market
        loan_data = self.private_get_loan_data(market, user_addr)
        merged_addrs = self.private_merge_tokens_address(loan_data)
        # usr_balances = self.private_get_user_balances(
        #     market, user_addr, merged_addrs)
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        tokens_data = loop.run_until_complete(
            self.private_async_get_tokens_info(market, merged_addrs))

        return self.private_generate_dto(loan_data, tokens_data)


class Erc20:
    def __init__(self) -> None:
        current_directory = os.getcwd()
        path = current_directory + '/modules/aavev3/config.json'
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)
        self.config = SimpleNamespace(**config_data)

        path = current_directory + '/token_config.json'
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)
        self.token_config = config_data

        self.w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        self.w3.is_connected()
        self.abi = self.config.erc20["abi"]
        self.moralis = Moralis()

    def private_convert_moralis_token_info(self, token):
        return {
            "address": token["address"],
            "name": token["name"],
            "symbol": token["symbol"],
            "decimals": token["decimals"]
        }

    def private_convert_moralis_tokens_info(self, tokens):
        token_dict = {}
        for index, token in enumerate(tokens):
            token_dict[token["address"].lower(
            )] = {"id": index+1, **self.private_convert_moralis_token_info(token)}
        return token_dict

    def public_get_token_info(self, address):
        address = Web3.to_checksum_address(address)
        contract = self.w3.eth.contract(abi=self.abi, address=address)
        return {
            "address": address.lower(),
            "name": contract.functions.name().call(),
            "symbol": contract.functions.symbol().call(),
            "decimals": contract.functions.decimals().call(),
            # "name": result[0],
            # "symbol": result[1],
            # "decimals": result[2],
        }

    def public_get_token_info_by_config(self, address):
        if address.lower() in self.token_config:
            return self.token_config[address]
        else:
            return self.public_get_token_info(address)

    def public_get_tokens_info_by_moralis(self, addresses):
        tokens_info = self.moralis.public_get_tokens_meta(addresses)
        return self.private_convert_moralis_tokens_info(tokens_info)

    def public_get_tokens_info(self, addresses):
        tokens_dict = {}
        for index, addr in enumerate(addresses):
            # token_info = self.public_get_token_info(addr)
            # TODO call from DB or Moralis
            token_info = self.public_get_token_info_by_config(addr)
            tokens_dict[addr] = {"id": index+1,
                                 ** token_info}

        # # get info from moralis api
        # tokens_dict = self.public_get_tokens_info_by_moralis(addresses)
        return tokens_dict


class DefiSaver:
    def __init__(self) -> None:
        current_directory = os.getcwd()
        path = current_directory + '/modules/aavev3/config.json'
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)

        w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
        w3.is_connected()
        self.config = SimpleNamespace(**config_data)
        self.contract = w3.eth.contract(
            abi=self.config.aave_v3_view["abi"], address=Web3.to_checksum_address(self.config.aave_v3_view["address"]))

    def public_get_loan_data(self, market, user_addr):
        market = Web3.to_checksum_address(market)
        user_addr = Web3.to_checksum_address(user_addr)
        raw_data = self.contract.functions.getLoanData(
            market, user_addr).call()
        return raw_data

    def public_get_prices(self, market, addresses):
        addresses = [Web3.to_checksum_address(addr) for addr in addresses]
        raw_data = self.contract.functions.getPrices(
            market, addresses).call()
        return raw_data

    def public_get_user_tokens_balance(self, market, user, tokens):
        tokens = [Web3.to_checksum_address(addr) for addr in tokens]
        user = Web3.to_checksum_address(user)
        return self.contract.functions.getTokenBalances(
            market, user, tokens).call()


class Moralis:
    def __init__(self) -> None:
        self.tokens_meta_url = "https://deep-index.moralis.io/api/v2/erc20/metadata"
        self.api_key = os.getenv("MORALIS_API_KEY")

    def public_get_tokens_meta(self, addresses):
        params = {
            "chain": "eth",
            "addresses": addresses
        }

        result = evm_api.token.get_token_metadata(
            api_key=self.api_key, params=params)
        return result
