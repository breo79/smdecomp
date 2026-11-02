import os
import ctypes

# Default DLL location in game folder
DEFAULT_DLL_PATH = r"C:\GOG Games\Minecraft Story Mode - Season Two\oo2core_5_win64.dll"

class OodleDecompressor:
    def __init__(self, dll_path=None):
        if dll_path is None:
            dll_path = DEFAULT_DLL_PATH
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"Oodle DLL not found at: {dll_path}")
        
        self.dll = ctypes.CDLL(dll_path)
        
        # OodleLZ_Decompress(
        #     const void *compBuf, size_t compBufSize,
        #     void *rawBuf, size_t rawLen,
        #     int fuzzSafe, int checkCRC, int verbosity,
        #     void *decBufBase, size_t decBufSize,
        #     void *fpCallback, void *callbackUserData,
        #     void *decoderMemory, size_t decoderMemorySize,
        #     int threadPhase
        # )
        self._decompress = self.dll.OodleLZ_Decompress
        self._decompress.argtypes = [
            ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_void_p, ctypes.c_size_t,
            ctypes.c_int
        ]
        self._decompress.restype = ctypes.c_size_t

    def decompress(self, comp_bytes: bytes, raw_len: int) -> bytes:
        raw_buf = ctypes.create_string_buffer(raw_len)
        res = self._decompress(
            comp_bytes, len(comp_bytes),
            raw_buf, raw_len,
            1, 0, 0,
            None, 0,
            None, None,
            None, 0,
            3
        )
        if res != raw_len:
            raise RuntimeError(f"Oodle decompression failed: expected {raw_len} bytes, got {res}")
        return raw_buf.raw
