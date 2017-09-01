#!/usr/bin/python
#coding=utf-8



import logging
import json
import time

from web3 import Web3, HTTPProvider, IPCProvider
from service import analysis
from config import Config
from prpcrypt import prpcrypt
import numpy as np


def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """

    return bytes.fromhex(hexStr)


def test_call_service(data):

    web3.personal.unlockAccount(usr2, '1234')
    web3.eth.sendTransaction({'from': usr2, 'to': usr1, 'value': 1, 'data': web3.toHex(data)})


def new_transaction_callback(transaction_hash):
    dict_message = web3.eth.getTransaction(transaction_hash)
    if not dict_message['from'] == usr1:
        return
    msg = web3.toUtf8(dict_message['input'])
    datas = msg.split(",")
    img_no = datas[0]

    result = ""
    for data in datas[1:]:
        interact_data = np.loads(HexToByte(data))
        result += analysis(interact_data)

    msg_to_send = crypt.encrypt(img_no + "," + result)
    test_call_service(msg_to_send)


if __name__ == "__main__":

    web3 = Web3(HTTPProvider('http://ethermint-service:8545'))
    usr1 = web3.eth.accounts[0]
    usr2 = web3.eth.accounts[1]

    crypt = prpcrypt(Config.key, Config.vi)

    new_transaction_filter = web3.eth.filter('pending')
    new_transaction_filter.watch(new_transaction_callback)

    while True:
        pass


