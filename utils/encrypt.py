import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def encrpt(password, key):
    public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()

# key是公钥，需要修改成自己的之后再进行加密
key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDfBT25KXp1we9BdINoQTYSWwuwtt09EAQ+e7K7eO3No88LfyXoZ68a0+JyVdV7xNZ8N/oHCRwJojHMjURTB9heHpzi+Cg/MbdmfgfSOuTwjRXp9iJMWFyFDWW/i0l278bF1qLPe9CDqusPxc6XYLgfjRrs45r9LI1Zb/jQXsrPJwIDAQAB'
password = encrpt('sf!@#123', key)
print('password:', password)
