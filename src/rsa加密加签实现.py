import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, MD5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import json
from copy import deepcopy
from collections import OrderedDict
from Crypto import Random

def rsa_pkcs1_encryptAndSign(thirdPublicKey, privateKey, requestJson):
    # 本例中，要加密的内容为 requestJson["bizContent"]
    # 加签后放在 requestJson["signContent"]
    # 用己方私钥加签（privateKey），第三方公钥加密（thirdPublicKey）　
    bizContent = json.dumps(requestJson["bizContent"])
    if "signContent" in requestJson.keys():
        del requestJson["signContent"]

    # 加密
    rsakey = RSA.importKey(base64.b64decode(thirdPublicKey))
    bizContent = bytes(bizContent, encoding="utf-8")
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    length = len(bizContent)
    default_length = 117
    offset = 0
    res = bytes()
    while length - offset > 0:
        if length - offset > default_length:
            _res = cipher.encrypt(bizContent[offset:offset + default_length])
        else:
            _res = cipher.encrypt(bizContent[offset:])
        offset += default_length
        res += _res
    requestJson["bizContent"] = base64.b64encode(res).decode('utf-8')

    # 加签
    # 这一部分参考双方约定，下方模仿Java中的map方法
    order_request = deepcopy(requestJson)
    linkedmap = OrderedDict()
    linkedkeys = sorted(order_request.keys())
    for _key in linkedkeys:
        linkedmap[_key] = str(order_request[_key])
    
    sign_request = "{"
    for key, value in linkedmap.items():
        _k_v = "{}={}, ".format(key, value)
        sign_request += _k_v  
    sign_request = sign_request[:-2] + "}"
    
    rsaprivatekey = RSA.importKey(base64.b64decode(bytes(privateKey, encoding='utf-8')))
    signer = Signature_pkcs1_v1_5.new(rsaprivatekey)
    digest = MD5.new(bytes(sign_request, encoding='utf-8'))
    sign = base64.b64encode(signer.sign(digest))

    requestJson["signContent"] = sign.decode('utf-8')
    return requestJson