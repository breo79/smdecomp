import pefile
import re

EXE_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\Minecraft2.exe"
pe = pefile.PE(EXE_PATH)
with open(EXE_PATH, 'rb') as f:
    data = f.read()

# Let's search for OpenSSL function names / string constants
openssl_funcs = [
    b'EVP_DecryptInit', b'EVP_DecryptUpdate', b'EVP_DecryptFinal',
    b'EVP_CIPHER_CTX_init', b'EVP_CIPHER_CTX_new', b'EVP_CIPHER_CTX_cleanup',
    b'EVP_CipherInit', b'EVP_CipherUpdate', b'EVP_CipherFinal',
    b'EVP_aes_', b'EVP_bf_', b'EVP_des_', b'EVP_rc4',
    b'BF_set_key', b'BF_encrypt', b'BF_ecb_encrypt', b'BF_cbc_encrypt',
    b'AES_set_decrypt_key', b'AES_decrypt', b'AES_cbc_encrypt'
]

for name in openssl_funcs:
    matches = [m.start() for m in re.finditer(re.escape(name), data)]
    if matches:
        print(f"Found '{name.decode()}': {len(matches)} at {[hex(m) for m in matches]}")
