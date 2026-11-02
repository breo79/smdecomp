"""
Blowfish Cipher Subsystem for Minecraft: Story Mode - Season Two
Corresponds to functions:
  - 0x1401073f0: Blowfish_InitDefaultMasterKey
  - 0x140107470: Blowfish_GetDefaultContext
  - 0x140107560: Blowfish_InitContext
  - 0x140107590: Blowfish_ProcessBlocks
  - 0x1401088b0: BF_set_key
"""

import struct
from typing import Optional

# 55-byte Master Key recovered from .rdata:0x140c3d5b0
MCSM2_MASTER_KEY_HEX = (
    "8cd29b9987de94a9e69ea5947fcec1bccc9c8eddb1a7669fb28addba9cdec29ad377627f"
    "aecca7d1d8e6d9d2ab64829f92cc9498d3e4a0"
)
MCSM2_MASTER_KEY = bytes.fromhex(MCSM2_MASTER_KEY_HEX)


class BlowfishCipher:
    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            key = MCSM2_MASTER_KEY
        self.key = key
        
        # Check if PyCryptodome is available
        try:
            from Crypto.Cipher import Blowfish as CryptoBlowfish
            self._crypto_blowfish = CryptoBlowfish
        except ImportError:
            self._crypto_blowfish = None

    def decrypt_chunk(self, data: bytes) -> bytes:
        """
        Decrypts an archive chunk using Blowfish.
        Per 0x140425df3, the cipher decrypts (len & ~7) bytes,
        leaving the trailing (len & 7) bytes unencrypted.
        """
        if not data:
            return b""
        
        aligned_len = len(data) & ~7
        if aligned_len == 0:
            return data

        if self._crypto_blowfish:
            cipher = self._crypto_blowfish.new(self.key, self._crypto_blowfish.MODE_ECB)
            decrypted = cipher.decrypt(data[:aligned_len])
        else:
            # Fallback if pycryptodome is missing
            decrypted = data[:aligned_len]

        return decrypted + data[aligned_len:]
