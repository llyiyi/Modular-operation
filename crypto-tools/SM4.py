# S盒以及S盒变换
def Sbox(word):
    SboxTable = [
        0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
        0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
        0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
        0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
        0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
        0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
        0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
        0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
        0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
        0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
        0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
        0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
        0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
        0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
        0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
        0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
    ]
    return (SboxTable[word >> 24] << 24) | (SboxTable[(word >> 16) & 0xFF] << 16) | (SboxTable[(word >> 8) & 0xFF] << 8) | SboxTable[word & 0xFF]


#系统参数FK
FK = [0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]


# 固定参数CK生成函数
def generate_CK():
    CK = []
    for i in range(32):
        CKi=0
        for j in range(4):
            CKi |= (4 * i + j) * 7 % 256 << (8 * (3 - j))
        CK.append(CKi)
    return CK


# 固定参数CK
CK = generate_CK()


# 循环左移
def left_rotate(value, n):
    return ((value << n) | (value >> (32 - n))) & 0xFFFFFFFF


# 线性变换L1和L2
def L1(X):
    return X ^ left_rotate(X, 2) ^ left_rotate(X, 10) ^ left_rotate(X, 18) ^ left_rotate(X, 24)

def L2(X):
    return X ^ left_rotate(X, 13) ^ left_rotate(X, 23)


# 反序变换R
def R(a, b, c, d):
    return [d.to_bytes(4, 'big'), c.to_bytes(4, 'big'), b.to_bytes(4, 'big'), a.to_bytes(4, 'big')]


# 密钥扩展算法
def key_expansion(key):
    key = key.encode('utf-8')
    rk = [0] * 32
    K = [int.from_bytes(key[i:i + 4], 'big') for i in range(0, 16, 4)] + [0] * 32
    K[0] = K[0] ^ FK[0]
    K[1] = K[1] ^ FK[1]
    K[2] = K[2] ^ FK[2]
    K[3] = K[3] ^ FK[3]
    for i in range(32):
        K[i + 4] = K[i] ^ (L2(Sbox(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ CK[i])))
        rk[i] = K[i + 4]

    return rk


# 加密算法
def sm4_encrypt_block(plain_text, rk):
    plain_text = plain_text.encode('utf-8')
    X = [int.from_bytes(plain_text[i:i + 4], 'big') for i in range(0, 16, 4)] + [0] * 32
    for i in range(32):
        X[i+4] = X[i] ^ (L1(Sbox(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rk[i])))
    return b''.join(R(X[32], X[33], X[34], X[35]))


# 解密算法
def sm4_decrypt_block(cipher_text, rk):
    X = [int.from_bytes(cipher_text[i:i + 4], 'big') for i in range(0, 16, 4)] + [0] * 32
    for i in range(32):
        X[i+4] = X[i] ^ (L1(Sbox(X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rk[31-i])))
    return b''.join(R(X[32], X[33], X[34], X[35]))


# 加密和解密函数
def sm4_encrypt(plain_text, key):
    rk = key_expansion(key)
    num_blocks = len(plain_text) // 16 
    if len(plain_text) % 16 != 0:
        num_blocks += 1
        plain_text = plain_text + '\x00' * (16 - len(plain_text) % 16)
    encrypted_blocks = []
    for i in range(num_blocks):
        block = plain_text[i * 16:(i + 1) * 16]
        encrypted_block = sm4_encrypt_block(block, rk)
        encrypted_blocks.append(encrypted_block)
    return b''.join(encrypted_blocks)

def sm4_decrypt(cipher_text, key):
    rk = key_expansion(key)
    num_blocks = len(cipher_text) // 16
    decrypted_blocks = []
    for i in range(num_blocks):
        block = cipher_text[i * 16:(i + 1) * 16]
        decrypted_block = sm4_decrypt_block(block, rk)
        decrypted_blocks.append(decrypted_block)
    return b''.join(decrypted_blocks)



# 加解密测试
key = "1234567890123456"
plain_text = "HELLO,WORLD!Welcome to my SM4 crypto"
cipher_text = sm4_encrypt(plain_text, key)
decrypted_text = sm4_decrypt(cipher_text, key)

print("Original data:", plain_text)
print("Encrypted data:", cipher_text)
print("Decrypted data:", decrypted_text.decode('utf-8'))