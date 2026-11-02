import os
import ctypes

GAME_DIR = r"C:\GOG Games\Minecraft Story Mode - Season Two"
OODLE_PATH = os.path.join(GAME_DIR, "oo2core_5_win64.dll")

oodle = ctypes.cdll.LoadLibrary(OODLE_PATH)
# OodleLZ_Decompress(const void *compBuf, size_t compBufSize, void *rawBuf, size_t rawLen, int fuzzSafe, int checkCRC, int verbosity, void *decBufBase, size_t decBufSize, void *fpCallback, void *callbackUserData, void *decoderMemory, size_t decoderMemorySize, int threadPhase)
OodleLZ_Decompress = oodle.OodleLZ_Decompress
OodleLZ_Decompress.argtypes = [
    ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p,
    ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_size_t, ctypes.c_int
]
OodleLZ_Decompress.restype = ctypes.c_size_t

sample_path = os.path.join(GAME_DIR, "Archives", "MC2_pc_PC_P2_Menu_compressed.ttarch2")
with open(sample_path, 'rb') as f:
    data = f.read()

# Chunk 0 is from offset 36 to 189 (length 153 bytes)
chunk0_comp = data[36:189]
raw_buf = ctypes.create_string_buffer(65536)

decomp_size = OodleLZ_Decompress(
    chunk0_comp, len(chunk0_comp),
    raw_buf, 65536,
    1, 0, 0, None, 0, None, None, None, 0, 0
)

print(f"Decompressed chunk 0 size: {decomp_size}")
if decomp_size > 0:
    decomp_bytes = raw_buf.raw[:decomp_size]
    print(f"First 128 bytes hex: {decomp_bytes[:128].hex()}")
    printable = "".join(chr(b) if 32 <= b < 127 else "." for b in decomp_bytes[:128])
    print(f"First 128 bytes ASCII: {printable}")
