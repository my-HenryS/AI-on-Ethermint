#!/usr/bin/python
import base64
from PIL import Image
from io import BytesIO

import os
from websocket_server import WebsocketServer
import threading
from service.hwrservice import HwrService
from config import Config
import image_utils as U
from web3 import Web3, HTTPProvider
from prpcrypt import prpcrypt
import web
import threading

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        web.seeother('/static/index.html');  # 重定向

# 定义全局锁
counter_lock = threading.Lock()


def __init__(self):
    global counter_lock  # 多线程是共享资源的，使用全局变量


def new_message(client, server, message):
    im = Image.open(BytesIO(base64.b64decode(message)))  # 转换为PIL格式
    valid, image_no = is_valid(im)
    if valid == False:
        print("out of valid request amount today")
        return
    client_dict[image_no] = client
    server.send_message(client, "Client Node : Image received\n")

    results = U.encode_image(im)
    server.send_message(client, "Client Node : Image analyzed\n")

    msg_to_send = ""
    for result in results:
        msg_to_send += ByteToHex(result.dumps())+","
    msg_to_send = msg_to_send[:-1]
    msg_to_send =image_no + "," + msg_to_send

    test_call_service(msg_to_send)

    server.send_message(client, "Client Node : Encoded Image received by Service Node\n")
    server.send_message(client, "Encoded Message : \n" + msg_to_send[300:600]+"......\n")


def ByteToHex( bins ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    return ''.join( [ "%02X" % x for x in bins ] ).strip()


def save_image(image):
    # 存放本地
    local_path = Config.image_save_path
    image_no = HwrService().saveImage(Config.image_save_path)
    image.save(local_path + image_no + Config.image_format)
    return image_no


def save_result(image_no, result):
    HwrService().updateResult(image_no, result)


def is_valid(im):
    if counter_lock.acquire():
        day_cnt = HwrService().queryCntByCurDate()
        if day_cnt < Config.valid_count:
            image_no = save_image(im)
            result = (True, image_no)
        else:
            result = (False, '')
        counter_lock.release()
        return result


def test_call_service(data):

    usr1 = web3.eth.accounts[0]
    usr2 = web3.eth.accounts[1]
    web3.personal.unlockAccount(usr1, '1234')
    web3.eth.sendTransaction({'from': usr1, 'to': usr2, 'value': 1,'data':web3.toHex(data)})


def new_transaction_callback(transaction_hash):
    print("transaction_hash = " + transaction_hash)
    dict_message = web3.eth.getTransaction(transaction_hash)
    if not dict_message['from'] == usr2:
        return
    msg = bytes.decode(crypt.decrypt(web3.toUtf8(dict_message['input']))).split(",")

    result = msg[1]
    img_no = msg[0]
    print("result = " + result)
    save_result(img_no, result)
    client = client_dict[img_no]
    server.send_message(client, "Client Node : Result Received\n")
    server.send_message(client, "The result is : " + result + "\n")

if __name__ == "__main__":

    web3 = Web3(HTTPProvider('http://ethermint-service:8545'))
    usr1 = web3.eth.accounts[0]
    usr2 = web3.eth.accounts[1]

    client_dict = {}

    port = Config.websocket_port
    host = Config.websocket_host
    if not os.path.exists(Config.image_save_path):
        os.makedirs(Config.image_save_path)

    crypt = prpcrypt(Config.key, Config.vi)

    new_transaction_filter = web3.eth.filter('pending')
    new_transaction_filter.watch(new_transaction_callback)

    app = web.application(urls, globals())
    _rest_thread = threading.Thread(target=app.run)
    _rest_thread.setDaemon(True)
    _rest_thread.start()

    server = WebsocketServer(port, host=host)
    server.set_fn_message_received(new_message)
    server.run_forever()





