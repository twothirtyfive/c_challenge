from flask import Flask
import contract_abi, time
from web3 import Web3, HTTPProvider
from settings import *

app = Flask(__name__)

w3: Web3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/147670b677b0444d8f984ee61a20062e'))
contract_address = w3.toChecksumAddress(contract_address)
wallet_address = w3.toChecksumAddress(wallet_address)
contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)

@app.route('/register/<string:addr>', methods=['POST'])
def register(addr):
    register_addr = w3.toChecksumAddress(addr)
    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = contract.functions.generate(register_addr).buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)
    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.getTransactionReceipt(result)

    count = 0
    while tx_receipt is None and (count < 30):
        time.sleep(7)
        tx_receipt = w3.eth.getTransactionReceipt(result)

    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return('transaction success')


@app.route('/get_id/<string:addr>', methods=['GET'])
def get_id(addr):
    register_addr = w3.toChecksumAddress(addr)
    ret = contract.functions.get_user(register_addr).call()
    return 'ID: {}'.format(str(ret))


@app.route('/info', methods=['GET'])
def get_info():
    ret = contract.functions.get_info().call()
    return 'In Use: {}, Remaining: {}'.format(ret[0],ret[1])