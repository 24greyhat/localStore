from Crypto.Cipher import AES
import os
import ast
import hashlib


def encrypt(data, privateKey: str):
    iv = os.urandom(16)
    key = str(privateKey).encode()
    a = AES.new(key, AES.MODE_CBC, iv=iv)
    e = a.encrypt(str(data).encode()*16)
    return iv+e


def decrypt(data, privateKey: str):
    iv = data[0:16]
    data = data[16::]
    a = AES.new(str(privateKey).encode(), AES.MODE_CBC, iv=iv)
    try:
        d = a.decrypt(data).decode()
        return d[0:int(len(d)/16)]
    except Exception:
        return None


class LocalStore:
    def __init__(self, name: str, privateKey: str):
        self.path = name+'.lstore'
        self.pk = hashlib.sha256(str(privateKey).encode()).hexdigest()[16:32]
        if not os.path.exists(self.path):
            with open(self.path, 'wb') as f:
                f.write(encrypt("{}", self.pk))
    
    def load(self)->dict:
        with open(self.path, 'rb') as f:
            r = f.read()
            try:
                r = decrypt(r, self.pk)
                if r:
                    return ast.literal_eval(r)
                else:
                    return None
            except Exception:
                return None


    def dump(self, obj):
        c = self.load()
        r = dict()
        if c:
            r.update(c)
        r.update(obj)

        with open(self.path, 'wb') as f:
            f.write(encrypt(str(r), self.pk))
    
    def remove(self, key):
        r = self.load()
        if key in r:
            r.pop(key)
            with open(self.path, 'wb') as f:
                f.write(encrypt(str(r), self.pk))