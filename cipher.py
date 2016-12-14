#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CryptoPlus.Cipher.rijndael import rijndael
import base64
import hashlib

KEY_SIZE = 16
BLOCK_SIZE = 32

PREFIX='aaa'
DATA_PREFIX='bbb'
DATA_AUTH_KEY='ccc'

def encrypt(key, plaintext):
    padded_key = key.ljust(KEY_SIZE, '\0')
    padded_text = plaintext + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * '\0'

    # could also be one of
    #if len(plaintext) % BLOCK_SIZE != 0:
    #    padded_text = plaintext.ljust((len(plaintext) / BLOCK_SIZE) + 1 * BLOCKSIZE), '\0')
    # -OR-
    #padded_text = plaintext.ljust((len(plaintext) + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE)), '\0')

    r = rijndael(padded_key, BLOCK_SIZE)

    ciphertext = ''
    for start in range(0, len(padded_text), BLOCK_SIZE):
        ciphertext += r.encrypt(padded_text[start:start+BLOCK_SIZE])

    encoded = base64.b64encode(ciphertext)

    return encoded


def decrypt(key, encoded):
    padded_key = key.ljust(KEY_SIZE, '\0')

    ciphertext = base64.b64decode(encoded)

    r = rijndael(padded_key, BLOCK_SIZE)

    padded_text = ''
    for start in range(0, len(ciphertext), BLOCK_SIZE):
        padded_text += r.decrypt(ciphertext[start:start+BLOCK_SIZE])

    plaintext = padded_text.split('\x00', 1)[0]

    return plaintext

def md5(str):
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()

def _makeVerify(prefix, d):
    '''
    生成校验串
    '''
    s = base64.encodestring(''.join(chr(ord(a)^ord(b)) for a,b in zip(prefix,d)))
    return s[:8]

def _verify(text):
    '''
    校验数据是否为加密数据
    @param string $text 加密数据字符串
    '''
    l = text[:1]
    if len(text) <= 9+int(l):
        return False
    v = text[1:1+int(l)]
    p = text[1+int(l):1+int(l)+8]
    d = text[int(l)+9:]
    c = _getSecret()
    ve = _makeVerify(c['prefix'], d)
    if(ve == p):
        return {'v':v,'data':d,'c':c}
    return False
    
def _getSecret():
    '''
    返回secret和prefix
    '''
    v = 1
    secret = md5(PREFIX+DATA_AUTH_KEY)
    # self::$data_prefix."|$v|"
    prefix = DATA_PREFIX+'|%s|' % (v,)
    return {'secret':secret, 'prefix':prefix}
    
def qy_encode(text,v=1):
    '''
    加密
    '''
    ve = _verify(text)
    if ve!=False:
        return text
    c = _getSecret()
    encrypted = encrypt(c['secret'], text)
    prefix = _makeVerify(c['prefix'], encrypted)
    return '%s%s%s%s' % (len(str(v)), v, prefix, encrypted)

def qy_decode(text):
    '''
    解密
    '''
    ve = _verify(text)
    if ve==False:
        return text
    c = ve['c']
    return decrypt(c['secret'], ve['data'])
